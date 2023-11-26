import os
import shutil
import tempfile
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from cpmonitor.models import City


class CleanupImagesTest(TestCase):
    base_path = None
    images_path = None
    uploads_path = None

    @classmethod
    def setUpClass(cls):
        cls.base_path = tempfile.mkdtemp()
        cls.images_path = os.path.join(cls.base_path, "images")
        cls.uploads_path = os.path.join(cls.images_path, "uploads")

        cls.env_patcher = patch.dict(
            os.environ,
            {
                "BASE_PATH": cls.base_path,
                "IMAGES_PATH": cls.images_path,
                "UPLOADS_PATH": cls.uploads_path,
            },
        )
        cls.env_patcher.start()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        shutil.rmtree(cls.base_path, True)

        cls.env_patcher.stop()

    def setUp(self):
        super().setUp()

        os.mkdir(self.images_path)
        os.mkdir(self.uploads_path)

        self.assertTrue(os.path.isdir(self.base_path))
        self.assertTrue(os.path.isdir(self.uploads_path))
        self.assertTrue(len(os.listdir(self.uploads_path)) == 0)

        self.assertEqual(os.environ["BASE_PATH"], self.base_path)
        self.assertEqual(os.environ["IMAGES_PATH"], self.images_path)
        self.assertEqual(os.environ["UPLOADS_PATH"], self.uploads_path)

    def tearDown(self):
        super().tearDown()

        shutil.rmtree(self.images_path, True)

        self.assertFalse(os.path.isdir(self.uploads_path))
        self.assertTrue(os.path.isdir(self.base_path))

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

    def test_when_no_images_exist_in_images_path_then_do_not_delete_anything(self):
        output = StringIO()
        call_command("cleanupimages", stdout=output)

        self.assertIn("No images found to clean up", output.getvalue())

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
