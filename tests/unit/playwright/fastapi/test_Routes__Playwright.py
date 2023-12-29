from unittest import TestCase

from fastapi import FastAPI
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import obj_info

from osbot_playwright.playwright.fastapi.Routes__Playwright import Routes__Playwright, ROUTES_PATHS__PLAYWRIGHT, \
    ROUTES_METHODS__PLAYWRIGHT


class test_Routes__Playwright(TestCase):

    def setUp(self):
        self.app =  FastAPI()
        self.routes_playwright = Routes__Playwright(self.app)

    def test_html(self):
        url    = 'https://httpbin.org/get'
        result = self.routes_playwright.html(url)
        pprint(result)

    def test_screenshot(self):
        #png_signature      = b'\x89PNG\r\n\x1A\n'
        url                = 'https://httpbin.org/get'
        streaming_response = self.routes_playwright.screenshot(url)

        assert streaming_response.charset       == "utf-8"
        assert streaming_response.media_type    == "image/png"
        assert streaming_response.status_code   == 200
        assert dict(streaming_response.headers) == {'content-type': 'image/png'}





    def test_routes_paths(self):
        assert self.routes_playwright.routes_methods() == ROUTES_METHODS__PLAYWRIGHT
