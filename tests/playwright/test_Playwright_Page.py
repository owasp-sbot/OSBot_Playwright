from unittest import TestCase

import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_text, obj_info
from playwright.sync_api import Response

from osbot_playwright.playwright.API_Playwight import API_Playwright
from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Page import Playwright_Page


class test_Playwright_Page(TestCase):
    headless                 : bool
    api_playwright           : API_Playwright
    playwright_browser_chrome: Playwright_Browser__Chrome
    #page            : Playwright_Page

    @classmethod
    def setUpClass(cls) -> None:
        cls.headless = True
        cls.playwright_browser_chrome = Playwright_Browser__Chrome(headless=cls.headless)
        cls.api_playwright            = cls.playwright_browser_chrome.api_playwright()

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.playwright_browser_chrome.stop_playwright_and_process() is True

    def test_ctor(self):
        assert self.headless                is True
        assert self.api_playwright.headless is True

    def test_open(self):
        page = self.api_playwright.new_page()
        url = 'https://www.google.com/' + random_text()
        assert type(page.open(url)) == Response
        assert page.url() == url
        assert page.close() is True


    def test_goto(self):
        page     = self.api_playwright.new_page()
        url      = 'https://httpbin.org/get'
        raw_page = page.page

        assert str(raw_page)             == "<Page url='about:blank'>"
        assert page.url()                == 'about:blank'

        response = page.goto(url)
        assert page.close() is True

        request  = response.request
        assert type(response)            == Response
        assert response.ok               == True
        assert response.status           == 200
        assert response.status_text      == ''
        assert response.url              == url
        assert response.frame.page       == raw_page
        assert str(response.frame.page)  == f"<Page url='{url}'>"
        assert request.url               == url
        assert request.failure           is None
        assert request.frame.url         == url
        assert request.frame.page        == response.frame.page
        assert request.method            == 'GET'
        assert request.post_data         is None
        assert request.redirected_from   is None
        assert request.resource_type     == 'document'
        assert page.close() is True
