from unittest import TestCase
from unittest.mock import patch, MagicMock

import playwright
import pytest
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Json import json_parse
from osbot_utils.utils.Misc import wait_for, list_set
from osbot_utils.utils.Python_Logger import logger_info
from playwright.sync_api import BrowserType, Browser, BrowserContext, Error

from osbot_playwright.playwright.Playwright_Chrome_Browser import Playwright_Chrome_Browser
from osbot_playwright.playwright.Playwright_Page import Playwright_Page
from playwright.sync_api import Page

@pytest.mark.skip('refactor these methods to use API_Playwright')
class test_Playwright_Chrome_Browser(TestCase):
    headless                  : bool
    playwright_chrome_browser : Playwright_Chrome_Browser           # so that we don't get a warning in the @classmethod(s)

    # this method is called only once for this class

    # this method is called on every test method in this class

    # the variables defined in the @setupClass are available here as well
    def setUp(self):
        browser = self.playwright_chrome_browser.browser()
        assert  type(browser) == Browser

    def test_browser(self):
        with self.playwright_chrome_browser as _:
            assert type(_.browser()) == Browser
            page = _.browser().new_page()               # open a new page and check that all is good
            assert page.url == 'about:blank'
            #url = 'https://www.google.com/'            # was quite slow (couple seconds)
            url = _.url_browser_debug_page_json()
            page.goto(url)
            assert page.url == url
            page.close()



    def test_browser_connect_to_existing_process(self):
        with self.playwright_chrome_browser as _:
            assert type(_.browser()) == Browser
            _._browser = None
            assert _.browser_connect_to_existing_process() is True
            assert _._browser == _.browser()
            assert type(_.browser()) == Browser

            # simulate when self.process_running() returns False
            with patch.object(_, 'process_running', return_value=False):
                with patch.object(_.logger, 'error', new_callable=MagicMock) as mock_logger_error:
                    result = _.browser_connect_to_existing_process()
                    assert result is False
                    mock_logger_error.assert_called_once_with("No existing process found to connect to")

            # simulate when browser_connect_over_cdp raises an exception
            with patch.object(_, 'browser_connect_over_cdp', side_effect=Exception("Test exception")):
                with patch.object(_.logger, 'error', new_callable=MagicMock) as mock_logger_error:
                    result = _.browser_connect_to_existing_process()
                    assert result is False
                    mock_logger_error.assert_called_once_with("[Playwright_Chrome] in browser_connect: Test exception")

    def test_chromium(self):
        assert type(self.playwright_chrome_browser.chromium()) == BrowserType

    def test_chromium_exe_path(self):
        chromium_exe_path = self.playwright_chrome_browser.chromium_exe_path()
        assert file_exists(chromium_exe_path)

                      # we need to do this since deleting the last context seems to prevent new ones from being created

    def test_contexts(self):
        with self.playwright_chrome_browser as _:
            assert len(_.contexts()) >0
            for context in _.contexts():
                assert type(context) == BrowserContext
            pprint(_.contexts())
            with patch.object(_, 'browser', return_value=None):
                assert _.contexts() == []




    def test_new_page(self):
        page = self.playwright_chrome_browser.new_page()
        assert type(page) == Playwright_Page

    def test_pages(self):
        with self.playwright_chrome_browser as _:
            original_pages  = _.pages()
            new_page        = _.new_page().page
            current_pages   = _.pages()

            assert len(current_pages) == len(original_pages) +1 # todo: fix test below
            #assert new_page in current_pages

            # page = _.page(page_index=len(current_pages)-1)
            # assert page == new_page
            # assert page.url == 'about:blank'
            #
            # url = _.url_browser_debug_page_json()
            # page.goto(url)
            # assert page.url == url

            #page.close()

    # with cache_on_function this cannot be tested this way
    # def test_playwright(self):
    #     with pytest.raises(Exception) as exc_info:
    #         Playwright_Chrome_Browser().playwright()
    #
    #     assert str(exc_info.value) == "Cannot create playwright instance while asyncio event loop is running"

    def test_process_id(self):
        process_id = self.playwright_chrome_browser.process_id()
        assert process_id is not None

    def test_process_details(self):
        with self.playwright_chrome_browser as _:
            process_details = _.process_details()
            assert process_details.get('process_id') == _.process_id()
            assert process_details.get('status'    ) == _.process_status()

            # confirm return value when there is an exception
            with patch.object(_, 'load_process_details', return_value={'process_id': 9999}):
                assert _.process_details() == {}
