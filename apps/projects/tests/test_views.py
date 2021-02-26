import tempfile

from django.shortcuts import reverse
from rest_framework import status

from apps.core.utils.test import APITestCase
from apps.core.utils.test.factories import TagFactory, ProjectFactory
from apps.projects.models import Tag, Project


class TagViewsetTests(APITestCase):
    """Tests for the tag viewset"""

    def setUp(self):
        self.factory = TagFactory()

    @staticmethod
    def get_tag_url(tag: Tag):
        return reverse('tag-detail', args=(tag.pk,))
    
    @property
    def tag_list_url(self):
        return reverse('tag-list')

    def test_get_tag_succeeds(self):
        """Test retrieving a specific tag succeeds"""
        tag = self.factory.tag()
        url = self.get_tag_url(tag)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertStrictAllIn(('id', 'name', 'color'), res.data)

    def test_list_tag_succeeds(self):
        tag1 = self.factory.tag()
        tag2 = self.factory.tag()
        res = self.client.get(self.tag_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_unauthorized_methods(self):
        """Test that methods that should not be authorized really are not"""
        url = self.tag_list_url
        specific_url = self.get_tag_url(self.factory.tag())
        self.assertEqual(self.client.post(url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(specific_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.put(specific_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectViewsetTests(APITestCase):
    """Tests for the project viewset"""
    def setUp(self):
        self.factory = ProjectFactory()

    @property
    def project_list_url(self) -> str:
        return reverse('project-list')

    @staticmethod
    def get_project_url(project: Project) -> str:
        return reverse('project-detail', args=(project.pk,))

    def test_get_project_returns_200(self):
        """Test that retrieving a project is successful"""
        project = self.factory.project()
        res = self.client.get(self.get_project_url(project))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_project_response_structure(self):
        """Test that retrieving a project returns the correct data shape"""
        project = self.factory.project()
        res = self.client.get(self.get_project_url(project))
        expected = {'id', 'title', 'description', 'link', 'gallery', 'thumbnail', 'tags'}
        self.assertStrictAllIn(expected, res.data)

        self.assertStrictAllIn(res.data['gallery'], {'id', 'pictures'})
        self.assertIsInstance(res.data['gallery']['pictures'], list)
        self.assertStrictAllIn({'id', 'name', 'placeholder', 'image'}, res.data['gallery']['pictures'][0])

        self.assertIsInstance(res.data['tags'], list)
        self.assertStrictAllIn({'id', 'name', 'color'}, res.data['tags'][0])

    def test_get_project_list_succeeds(self):
        """Test that listing projects succeeds"""
        project1 = self.factory.project()
        project2 = self.factory.project()
        res = self.client.get(self.project_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertStrictAllIn({'id', 'href', 'title', 'description', 'link', 'thumbnail', 'tags'}, res.data[0])

    def test_unauthorized_methods(self):
        """Test that methods that should not be authorized really are not"""
        url = self.project_list_url
        specific_url = self.get_project_url(self.factory.project())
        self.assertEqual(self.client.post(url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(specific_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.put(specific_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
