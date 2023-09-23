from unittest import TestCase

from osbot_utils.utils.Misc import random_text
from playwright.sync_api import Response

from osbot_playwright.playwright.API_Playwight import API_Playwright
from osbot_playwright.playwright.Playwright_Page import Playwright_Page


class test_Playwright_Page(TestCase):
    headless        : bool
    api_playwright  : API_Playwright
    #playwright_page : Playwright_Page

    @classmethod
    def setUpClass(cls) -> None:
        cls.headless = True
        cls.api_playwright = API_Playwright(headless=cls.headless)
        cls.page           = cls.api_playwright.new_page()

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.api_playwright.browser_close() is True
        cls.page.close()


    def test_ctor(self):
        assert type(self.page) == Playwright_Page


    def test_open(self):
        url = 'https://www.google.com/' + random_text()
        assert type(self.page.open(url)) == Response
        assert self.page.url() == url

    def test_goto(self):
        url      = 'https://www.google.com/'

        raw_page = self.page.page
        #assert str(raw_page)             == "<Page url='about:blank'>"

        response = self.page.goto(url)
        request  = response.request
        assert type(response)            == Response
        assert response.ok               == True
        assert response.status           == 200
        assert response.status_text      == ''
        assert response.url              == url


        assert response.frame.page       == raw_page

        assert str(response.frame.page)  == "<Page url='https://www.google.com/'>"
        assert request.url               == url
        assert request.failure           is None
        assert request.frame.url         == url
        assert request.frame.page        == response.frame.page
        assert request.method            == 'GET'
        assert request.post_data         is None
        assert request.redirected_from   is None
        assert request.resource_type     == 'document'
        #assert list_set(request.headers)  == ['upgrade-insecure-requests', 'user-agent']
