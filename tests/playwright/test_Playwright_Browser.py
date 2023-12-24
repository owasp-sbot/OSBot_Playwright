from asyncio import unix_events
from unittest import TestCase

from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Misc import obj_info
from playwright.sync_api import Playwright, BrowserType

from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser


class test_Playwright_Browser(TestCase):

    def setUp(self):
        self.playwright_browser = Playwright_Browser()

    def tearDown(self):
        self.playwright_browser.stop()

    def test__init__(self):
        assert self.playwright_browser.headless is True

    def test_event_loop(self):
        def create_and_stop():
            assert self.playwright_browser.event_loop() is None
            assert self.playwright_browser.playwright() is not None # this will create the event loop
            event_loop = self.playwright_browser.event_loop()
            assert type(event_loop) is unix_events._UnixSelectorEventLoop
            assert event_loop.is_running() is True
            assert event_loop.is_closed () is False
            assert event_loop.slow_callback_duration == 0.1

            assert self.playwright_browser.stop() is True
            assert event_loop.is_running       () is False
            assert event_loop.is_closed        () is True

        create_and_stop()                   # try this twice to make sure we can start, stop and start
        create_and_stop()                   # the main playwright event loop


    def test_playwright(self):
        print()
        with Duration(prefix='playwright'):
            playwright = self.playwright_browser.playwright()
            assert type(playwright) is Playwright

        obj_info(playwright, value_width=512)

        assert len(playwright.devices  ) > 100
        assert type(playwright.chromium) is BrowserType
        assert type(playwright.firefox ) is BrowserType
        assert type(playwright.webkit  ) is BrowserType

        assert file_exists(playwright.chromium.executable_path) is True
        assert file_exists(playwright.firefox .executable_path) is False        # todo add support for Firefox
        assert file_exists(playwright.webkit  .executable_path) is False        # todo add support for WebKit




    def test_playwright_context_manager(self):
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


