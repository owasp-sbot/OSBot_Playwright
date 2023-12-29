from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_playwright.playwright.fastapi.Fast_API_Playwright import Fast_API_Playwright


class test_Fast_API_Playwright(TestCase):

    def setUp(self):
        self.fast_api = Fast_API_Playwright()

    def test__init__(self):
        assert self.fast_api.enable_cors is False

    def test_routes(self):
        routes = self.fast_api.routes_paths()
        assert routes == ['/', '/aaa']