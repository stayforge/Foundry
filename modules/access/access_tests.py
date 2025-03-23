import unittest
import json

from app.modules.access.controller import AccessController


def test_index():
    access_controller = AccessController()
    result = access_controller.index()
    assert result == {'message': 'Hello, World!'}
