import unittest
import json

from modules.main.controller import MainController


def test_index():
    main_controller = MainController()
    result = main_controller.index()
    assert result == {'message': 'Hello, World!'}
