import os
import shutil
import tempfile
from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings

from cpmonitor.models import City


class CleanupImagesTest(TestCase):
    base_path = tempfile.mkdtemp()
    images_path = os.path.join(base_path, "images")
    uploads_path = os.path.join(images_path, "uploads")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        shutil.rmtree(cls.base_path, True)

    @override_settings(BASE_DIR=base_path, MEDIA_ROOT=images_path)
    def setUp(self):
        super().setUp()

        os.makedirs(self.images_path, exist_ok=True)
        os.makedirs(self.uploads_path, exist_ok=True)

        self.assertTrue(os.path.isdir(self.base_path))
        self.assertTrue(os.path.isdir(self.uploads_path))
        self.assertTrue(len(os.listdir(self.uploads_path)) == 0)

        self.assertEqual(settings.BASE_DIR, self.base_path)
        self.assertEqual(settings.MEDIA_ROOT, self.images_path)

    def tearDown(self):
        super().tearDown()

        shutil.rmtree(self.images_path, True)

        self.assertFalse(os.path.isdir(self.uploads_path))
        self.assertTrue(os.path.isdir(self.base_path))

    @override_settings(BASE_DIR=base_path, MEDIA_ROOT=images_path)
    def test_when_dry_run_then_do_not_delete_orphan_images(self):
        orphan_image = self._create_orphan_image()

        output = StringIO()
        call_command("cleanupimages", "--dry", stdout=output)

        self.assertIn(
            "Dry run: '1' images will be cleaned up in directory '%s'"
            % self.uploads_path,
            output.getvalue(),
        )
        self.assertTrue(os.path.isfile(orphan_image))

    @override_settings(BASE_DIR=base_path, MEDIA_ROOT=images_path)
    def test_when_no_images_exist_in_images_path_then_do_not_delete_anything(self):
        output = StringIO()
        call_command("cleanupimages", stdout=output)

        self.assertIn("No images found to clean up", output.getvalue())

    @override_settings(BASE_DIR=base_path, MEDIA_ROOT=images_path)
    def test_when_orphan_and_referenced_image_exist_then_only_delete_orphan_image(self):
        orphan_image = self._create_orphan_image()
        referenced_image = self._create_referenced_image("test.png")
        self.persist_model_referencing_to_image("test.png")

        output = StringIO()
        call_command("cleanupimages", stdout=output)

        self.assertIn(
            "Cleaned up '1' images in directory '%s'" % self.uploads_path,
            output.getvalue(),
        )
        self.assertIn(orphan_image, output.getvalue())
        self.assertFalse(os.path.isfile(orphan_image))
        self.assertTrue(os.path.isfile(referenced_image))

    @override_settings(BASE_DIR=base_path, MEDIA_ROOT=images_path)
    def test_when_only_referenced_image_exists_then_do_not_delete_it(self):
        referenced_image = self._create_referenced_image("test.png")
        self.persist_model_referencing_to_image("test.png")

        output = StringIO()
        call_command("cleanupimages", stdout=output)

        self.assertIn("No images found to clean up", output.getvalue())
        self.assertTrue(os.path.isfile(referenced_image))

    def _create_orphan_image(self) -> str:
        image_path = os.path.join(self.uploads_path, "orphan.png")
        open(image_path, "x").close()
        self.assertTrue(os.path.isfile(image_path))

        return image_path

    def _create_referenced_image(self, image_name) -> str:
        image_path = os.path.join(self.uploads_path, image_name)
        open(image_path, "x").close()
        self.assertTrue(os.path.isfile(image_path))

        return image_path

    def persist_model_referencing_to_image(self, image_name):
        City.objects.create(
            description="Test-Bild: ![%s](images/uploads/%s)" % (image_name, image_name)
        )
