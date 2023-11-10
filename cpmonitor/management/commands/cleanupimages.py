import os
import re

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models as DjangoModels

APP_NAME = __package__.split(".")[0]
BASE_PATH = os.environ.get("BASE_PATH")
IMAGES_PATH = os.environ.get("IMAGES_PATH")


class Command(BaseCommand):
    help = "Cleans up orphan images that are no longer used but are still linked in Markdown or file fields"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            action="store_true",
            help="Do not clean up images but output a list of images which will be cleaned up",
        )

    def handle(self, *args, **options):
        is_dry_run = options["dry"]

        try:
            orphan_images = self.resolve_orphan_images()
        except Exception as exception:
            raise CommandError("Error occurred by cleaning up images: %s" % exception)

        if is_dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    "Dry run: '%d' images will be cleaned up in directory '%s': '%s'"
                    % (
                        len(orphan_images),
                        os.path.abspath(IMAGES_PATH),
                        orphan_images,
                    )
                )
            )

            return

        for orphan_image in orphan_images:
            os.remove(orphan_image)

        if len(orphan_images):
            self.stdout.write(
                self.style.SUCCESS(
                    "Cleaned up '%d' images in directory '%s': '%s'"
                    % (
                        len(orphan_images),
                        os.path.abspath(IMAGES_PATH),
                        orphan_images,
                    )
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("No images found to clean up"))

    def resolve_orphan_images(self) -> list[str]:
        referenced_images = self._fetch_referenced_images()
        saved_images = self.resolve_saved_images()

        orphan_images = []
        for saved_image in saved_images:
            if saved_image not in referenced_images:
                orphan_images.append(saved_image)

        return orphan_images

    def _fetch_referenced_images(self) -> list[str]:
        text_field_images = self._resolve_image_paths_from_text_fields()
        file_field_images = self._resolve_image_paths_from_file_fields()
        distinct_images = list(dict.fromkeys(text_field_images + file_field_images))

        return distinct_images

    def _resolve_image_paths_from_text_fields(self) -> list[str]:
        relative_paths = []

        for model_class in apps.get_models():
            models = model_class.objects.all()

            for field in model_class._meta.fields:
                if self._is_domain_text_field(field):
                    relative_paths += self._extract_file_paths_from_models(
                        field, models
                    )

        absolute_paths = []
        base_path = os.path.abspath(BASE_PATH)

        for relative_path in relative_paths:
            absolute_paths.append(os.path.join(base_path, relative_path.strip("/")))

        return absolute_paths

    def _is_domain_text_field(self, field) -> bool:
        return self._is_domain_model(field) and isinstance(
            field, DjangoModels.TextField
        )

    def _is_domain_model(self, field) -> bool:
        return field.model._meta.app_label == APP_NAME

    def _extract_file_paths_from_models(self, field, models) -> list[str]:
        file_paths = []
        field_values = self._extract_values_from_models(field, models)

        for field_value in field_values:
            if self._contains_text_field_file_path(field, field_value):
                file_paths += self._extract_text_field_file_paths(field_value)
            elif self._contains_file_field_file_path(field, field_value):
                file_paths += self._extract_file_field_file_path(field_value)

        return file_paths

    def _extract_values_from_models(self, field, models) -> list[str]:
        field_values = []

        for model in models:
            field_value = self._extract_value(field, model)

            if field_value:
                field_values.append(field_value)

        return field_values

    def _extract_value(self, field, model) -> str:
        field_value = field.value_from_object(model)

        if self._is_path_object(field_value):
            return field_value.path
        else:
            return field_value

    def _is_path_object(self, field_value) -> bool:
        return not isinstance(field_value, str)

    def _contains_text_field_file_path(self, field, field_value) -> bool:
        if not self._is_domain_text_field(field):
            return False

        return len(self._extract_text_field_file_paths(field_value)) > 0

    def _extract_text_field_file_paths(self, field_value) -> list[str]:
        real_file_paths = []
        potential_file_paths = re.findall(
            r"!\[[^\]]*\]\((?P<file_path>.*?)\s*\)", field_value
        )

        for file_path in potential_file_paths:
            if not self._is_url(file_path):
                real_file_paths.append(file_path)

        return real_file_paths

    def _is_url(self, value) -> bool:
        validate_url = URLValidator()

        try:
            validate_url(value)
        except ValidationError:
            return False

        return True

    def _contains_file_field_file_path(self, field, field_value) -> bool:
        if not self._is_domain_file_field(field):
            return False

        return len(self._extract_file_field_file_path(field_value)) > 0

    def _is_domain_file_field(self, field) -> bool:
        return self._is_domain_model(field) and isinstance(
            field, DjangoModels.FileField
        )

    def _extract_file_field_file_path(self, field_value) -> list[str]:
        return re.findall(r"".join(["^.*", IMAGES_PATH, ".*$"]), field_value)

    def _resolve_image_paths_from_file_fields(self) -> list[str]:
        file_paths = []

        for model_class in apps.get_models():
            models = model_class.objects.all()

            for field in model_class._meta.fields:
                if self._is_domain_file_field(field):
                    file_paths += self._extract_file_paths_from_models(field, models)

        return file_paths

    def resolve_saved_images(self) -> list[str]:
        saved_images = []

        for sub_directory, _, images in os.walk(IMAGES_PATH):
            for image in images:
                if self._is_ignored(image, sub_directory):
                    continue

                relative_path = os.path.join(sub_directory, image)
                saved_images.append(os.path.abspath(relative_path))

        return saved_images

    def _is_ignored(self, image, sub_directory) -> bool:
        return ".gitkeep" in image or "test_database_uploads" in sub_directory
