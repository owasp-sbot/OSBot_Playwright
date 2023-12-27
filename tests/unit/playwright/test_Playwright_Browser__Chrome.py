from pprint import pprint
from unittest import TestCase

import pytest
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Files import file_exists, folder_exists, current_temp_folder
from osbot_utils.utils.Misc import list_set, obj_info, obj_data
from playwright.sync_api import BrowserType, Browser, BrowserContext

from osbot_playwright._extra_methdos_osbot import in_mac, in_linux
from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Process import Playwright_Process


class test_Playwright_Browser__Chrome(TestCase):
    playwright_browser_chrome : Playwright_Browser__Chrome

    @classmethod
    def setUpClass(cls):
        cls.playwright_browser_chrome = Playwright_Browser__Chrome()

    @classmethod
    def tearDownClass(cls):
        assert cls.playwright_browser_chrome.stop_playwright_and_process() is True

    def test__init__(self):
        with self.playwright_browser_chrome as _:
            assert isinstance(_, Playwright_Browser__Chrome)
            assert isinstance(_, Playwright_Browser        )
            assert isinstance(_, object                    )
            assert _.headless     is True
            assert isinstance(_.playwright_process, Playwright_Process)

    def test__install(self):
        assert self.playwright_browser_chrome.install() is True

    def test__process(self):
        process_details = self.playwright_browser_chrome.process()
        assert list_set(process_details) == ['created_at', 'debug_port', 'headless', 'process_args', 'process_id', 'reuse_browser', 'status', 'url']
        if in_mac():
            assert process_details.get('status') == 'running'
        if in_linux():
            assert process_details.get('status') == 'sleeping'          # in linux (at least in GH actions) the process is in a sleeping state (i.e. waiting for network connections)

    def test_browser(self):
        browser = self.playwright_browser_chrome.browser()
        assert type(browser            )     is Browser
        assert type(browser.contexts[0])     is BrowserContext
        assert list_set(obj_data(browser) )  == ['browser_type','contexts', 'version']
        assert browser.browser_type.name     == 'chromium'
        assert len(browser.contexts)         == 1

    # def test_chromium(self):
    #     assert type(self.playwright_browser_chrome.chromium()) is BrowserType
    #
    # def test_chromium_exe_path(self):
    #     chromium_exe_path = self.playwright_browser_chrome.chromium_exe_path()
    #     assert chromium_exe_path.startswith(current_temp_folder())
    #     assert file_exists(self.playwright_browser_chrome.chromium_exe_path()) is True

    def test_is_installed(self):
        assert self.playwright_browser_chrome.is_installed() is True


        # path = '/tmp/chromium_download'
        # from playwright.sync_api import sync_playwright
        # with sync_playwright() as p:
        #     p.chromium.install()
        #result = self.playwright_browser_chrome.download_to_folder(path)
        #pprint(result)

        # chrome_path = "/tmp/p-browsers/chromium-1091/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
        # port = 9999
        # headless = False
        # playwright_process = Playwright_Process(browser_path=chrome_path, debug_port=port, headless=headless)
        # pprint(playwright_process.stop_process())
        # pprint(playwright_process.start_process())
        # debug_url = playwright_process.url_browser_debug_page()
        # playwright_browser_chrome = Playwright_Browser__Chrome()
        # chromium                  = playwright_browser_chrome.chromium()
        # browser = chromium.connect_over_cdp(debug_url)
        # print()
        # #page = browser.contexts[0].new_page()
        # page = browser.contexts[0].pages[0]
        # page.goto("https://www.google.com/404")
        # print(page.content())


@pytest.mark.skip('only for local debugging')
class test_Playwright_Browser__Chrome__Not_Headless(TestCase):

    def setUp(self):
        self.headless   = False
        self.debug_port = 22222
        self.playwright_browser__chrome = Playwright_Browser__Chrome(port=self.debug_port, headless=self.headless)
        self.process_details            = self.playwright_browser__chrome.process()

    def test__init__(self):
        with self.playwright_browser__chrome as _:
            assert _.headless     is False
            assert _.debug_port   == self.debug_port
            #assert _.reuse_browser is True
            assert self.process_details.get('debug_port') == self.debug_port
            assert self.process_details.get('headless'  ) == self.headless

    def test_browser(self):
        with self.playwright_browser__chrome as _:
            assert type(_.browser()) == Browser
            page = _.page()
            page.open('https://news.bbc.co.uk')
            #pprint(len(page.page.query_selector_all('a')))
            #page = _.browser().new_page()               # open a new page and check that all is good
            #assert page.url == 'about:blank'
            #url = _.url_browser_debug_page_json()
            #page.goto(url)
            #assert page.url == url
            #page.close()

