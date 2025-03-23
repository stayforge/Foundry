import unittest
import json

from modules.site.controller import siteController


def test_index():
    site_controller = siteController()
    result = site_controller.index()
    assert result == {'message': 'Hello, World!'}
