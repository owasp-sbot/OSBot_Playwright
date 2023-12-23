from pprint import pprint
from unittest import TestCase

from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Process import Playwright_Process


class test_Playwright_Browser__Chrome(TestCase):
    def setUp(self):
        self.playwright_browser_chrome = Playwright_Browser__Chrome()

    def test__init__(self):
        assert True

    def test_download_to_folder(self):
        pass
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




