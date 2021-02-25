from unittest.mock import patch

from django.test import TestCase
from apps.projects.models import PathAndRename


class PathAndRenameTests(TestCase):
    """Tests for the path_and_rename function used for renaming pictures"""

    def test_rename_file(self):
        """Test renaming a file"""
        filename = "cute_doge.jpg"
        renamer = PathAndRename("images/")
        uuid_overwrite = "9087assd9f87"
        with patch('apps.projects.models.uuid.uuid4', return_value=uuid_overwrite):
            new_path = renamer(None, filename)
            self.assertEqual(new_path, f'images/{uuid_overwrite}.jpg')
