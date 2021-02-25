from typing import Iterable, Any, Union, Container

from rest_framework.test import APITestCase as DefaultAPITestCase


class APITestCase(DefaultAPITestCase):
    """Testcase class containing utility methods"""

    def assertAllIn(self, members: Iterable[Any], container: Union[Iterable[Any], Container[Any]],
                    msg: Any = ...) -> None:
        """Asserts that all elements are in the container"""
        for element in members:
            self.assertIn(element, container, msg)

    def assertDictMatchesAttrs(self, _dict: dict, _object: object, msg: Any = ...) -> None:
        """Asserts all dictionary values match an object's attributes"""
        for key in _dict.keys():
            self.assertEqual(_dict[key], getattr(_object, key))
