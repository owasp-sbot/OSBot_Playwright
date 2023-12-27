from asyncio import unix_events
from unittest import TestCase
from unittest.mock import patch

import pytest
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Misc import obj_info
from playwright.sync_api import Playwright, BrowserType, Page, Error, BrowserContext

from osbot_playwright.playwright.API_Playwight import API_Playwright
from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Install import SUPORTTED_BROWSERS
from osbot_playwright.playwright.Playwright_Page import Playwright_Page


class test_Playwright_Browser(TestCase):
    headless                  : bool
    api_playwright            : API_Playwright
    playwright_browser        : Playwright_Browser
    playwright_browser_chrome : Playwright_Browser__Chrome

    @classmethod
    def setUpClass(cls) -> None:
        cls.headless = True
        cls.playwright_browser_chrome = Playwright_Browser__Chrome(headless=cls.headless)
        cls.playwright_browser        = cls.playwright_browser_chrome.playwright_browser()
        cls.api_playwright            = cls.playwright_browser_chrome.api_playwright()


    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.playwright_browser_chrome.stop_playwright_and_process() is True

    def test_browser_via_cdp(self):
        assert self.playwright_browser.browser_via_cdp(browser_name=None, endpoint_url=None) is None

    def test_browser_type(self):
        for browser in SUPORTTED_BROWSERS:
            assert type(self.playwright_browser.browser_type(browser)) is BrowserType
        assert self.playwright_browser.browser_type('aaa') is None

    def test_contexts_close_all(self):
        with self.playwright_browser as _:
            assert len(_.contexts()     ) == 1
            assert len(_.pages()        ) == 0
            assert type(_.new_page()    ) == Playwright_Page
            assert len(_.pages()        ) == 1
            assert type(_.context_new() ) == BrowserContext
            assert len(_.contexts()     ) == 2

            assert _.contexts_close_all() == 2
            assert len(_.pages()        ) == 0
            assert len(_.contexts()     ) == 0

            # simulate when close_context raises an exception
            with patch.object(_, 'context_close', side_effect=Error("Test exception")):
                _.contexts_close_all()

        assert self.playwright_browser_chrome.restart() is True         # need to restart since after closing all contexts, creating a new one throws an error (saying that the browser has been closed)
        assert len(self.playwright_browser.contexts())  == 1
        assert len(self.playwright_browser.pages())     == 0
            #_.restart_process()

    def test_context_new(self):
        with self.playwright_browser as _:
            assert len(_.contexts()) == 1
            kwargs = dict( viewport                 = None ,
                           screen                   = None ,
                           extra_http_headers       = None ,
                           java_script_enabled      = None ,
                           record_har_path          = None ,
                           record_har_omit_content  = None ,
                           record_har_url_filter    = None ,
                           record_har_mode          = None ,
                           record_har_content       = None ,
                           record_video_dir         = None ,
                           record_video_size        = None ,
                           base_url                 = None )
            new_context = _.context_new(**kwargs)
            assert len(_.contexts()) == 2
            new_context.close()
            assert len(_.contexts()) == 1

    def test_event_loop(self):
        def create_and_stop():
            event_loop = self.playwright_browser.event_loop()
            assert type(event_loop) is unix_events._UnixSelectorEventLoop
            assert event_loop.is_running() is True
            assert event_loop.is_closed () is False
            assert event_loop.slow_callback_duration == 0.1

            assert self.playwright_browser.stop() is True
            assert event_loop.is_running       () is False
            assert event_loop.is_closed        () is True

            assert self.playwright_browser.event_loop() is None
            assert self.playwright_browser.playwright() is not None  # this will create the event loop
            assert self.playwright_browser.event_loop() is not None


        assert self.playwright_browser.playwright() is not None  # this will create the event loop

        create_and_stop()                   # try this twice to make sure we can start, stop and start
        create_and_stop()                   # the main playwright event loop

        assert self.playwright_browser_chrome.restart() is True         # todo: figure out why we need to restart it here
        page = self.playwright_browser.new_page()                       #       without the restart, we get an error saying that the eventloop is closed (which feels like the wrong message)
        assert type(page) is Playwright_Page
        assert page.close() is True



    def test_playwright(self):
        #print()

        playwright = self.playwright_browser.playwright()
        assert type(playwright) is Playwright

        #obj_info(playwright, value_width=512)

        assert len(playwright.devices  ) > 100
        assert type(playwright.chromium) is BrowserType
        assert type(playwright.firefox ) is BrowserType
        assert type(playwright.webkit  ) is BrowserType

        assert file_exists(playwright.chromium.executable_path) is True
        assert file_exists(playwright.firefox .executable_path) is False        # todo add support for Firefox
        assert file_exists(playwright.webkit  .executable_path) is False        # todo add support for WebKit



    def test_new_page(self):
        assert len(self.playwright_browser.pages()) == 0
        page = self.playwright_browser.new_page()
        assert len(self.playwright_browser.pages()) == 1
        assert type(page)                           is Playwright_Page
        assert page.url      ()                     == 'about:blank'
        assert self.playwright_browser.page().page  == page.page
        assert page.is_closed()                     is False
        assert page.close    ()                     is True
        assert page.is_closed()                     is True
        assert len(self.playwright_browser.pages()) == 0

    def test_page(self):
        assert len(self.playwright_browser.pages()) == 0
        target_url     = 'https://www.google.com/404'
        expected_title = 'Error 404 (Not Found)!!1'
        page = self.playwright_browser.page()
        assert len(self.playwright_browser.pages()) == 1
        assert type(page)                           is Playwright_Page
        assert page.url      ()                     == 'about:blank'
        assert page.open     (target_url).url       == target_url
        assert page.url      ()                     == target_url
        assert page.html     ().title()             == expected_title
        assert page.is_closed()                     is False
        assert self.playwright_browser.page().page  == page.page
        assert page.close    ()                     is True
        assert page.is_closed()                     is True
        assert len(self.playwright_browser.pages()) == 0


    def test_playwright_context_manager(self):
        self.playwright_browser.stop()
        playwright_context_manager = self.playwright_browser.playwright_context_manager()
        assert playwright_context_manager._exit_was_called  is False
        assert playwright_context_manager._own_loop         is False
        assert playwright_context_manager._watcher          is None


        playwright = playwright_context_manager.start()

        assert playwright_context_manager._exit_was_called  is False
        assert playwright_context_manager._own_loop         is True
        assert playwright_context_manager._watcher          is None

        playwright.stop()

        assert playwright_context_manager._exit_was_called is True
        assert playwright_context_manager._own_loop        is True
        assert playwright_context_manager._watcher         is None
