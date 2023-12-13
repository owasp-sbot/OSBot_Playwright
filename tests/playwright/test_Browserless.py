from unittest import TestCase

from playwright.sync_api import Browser
from osbot_playwright.playwright.API_Browserless import API_Browserless
from osbot_playwright.playwright.Playwright_Page import Playwright_Page



class test_API_Browserless(TestCase):
    api_browserless : API_Browserless()
    browser         : Browser

    @classmethod
    def setUpClass(cls):
        cls.api_browserless = API_Browserless()
        cls.browser         = cls.api_browserless.browser()

        assert type(cls.browser) is Browser

    def test_api_key(self):
        assert type(self.api_browserless.auth_key()) is str

    def test_browser(self):
        assert type(self.browser) == Browser


    def test_context(self):
        context = self.browser.contexts[0]

        assert len(self.browser.contexts)         == 1
        assert len(context.pages)                 == 1
        assert len (self.api_browserless.pages()) == 1
        assert context.pages[0].url == 'about:blank'
        assert self.api_browserless.pages()[0].page    == context.pages[0]
        assert self.api_browserless.pages()[0].context == context

    def test_new_page(self):
        assert len(self.api_browserless.pages()) == 1
        page  = self.api_browserless.new_page()
        pages = self.api_browserless.pages()
        assert type(page) == Playwright_Page
        assert len(pages) == 2
        assert pages[1].page == page.page
        assert page.url() == 'about:blank'
        target = 'https://www.google.com/404'
        page.open(target)
        assert page.url() == target
        assert page.html().title() == 'Error 404 (Not Found)!!1'
        assert page.html().tags__text('ins') == ['That’s an error.', 'That’s all we know.']
        assert 'Google' in page.html_raw()
        page.close()
        assert len(self.api_browserless.pages()) == 1

    def test_pages(self):
        pages = self.api_browserless.pages()
        assert len(pages) == 1
        assert pages[0].page == self.api_browserless.page().page


    def test_wss_url(self):
        assert self.api_browserless.wss_url() == f'wss://chrome.browserless.io?token={self.api_browserless.auth_key()}'
