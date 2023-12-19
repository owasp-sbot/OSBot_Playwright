from unittest import TestCase

from osbot_utils.testing.Trace_Call import trace_calls
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Python_Logger           import logger_info

from osbot_playwright.playwright.API_Playwight import API_Playwright
from osbot_playwright.playwright.Playwright_Chrome_Browser import Playwright_Chrome_Browser
from osbot_playwright.playwright.Playwright_Page import Playwright_Page

class test_API_Playwright(TestCase):
    headless       : bool
    api_playwright : API_Playwright

    @classmethod
    def setUpClass(cls) -> None:
        cls.headless = True
        cls.log_info = logger_info()
        cls.api_playwright = API_Playwright(headless=cls.headless)

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.api_playwright.browser_close() is True

    def test_browser(self):
        assert type(self.api_playwright.browser()) is Playwright_Chrome_Browser

    def test_new_page(self):
        page = self.api_playwright.new_page()
        assert type(page) is Playwright_Page
        assert page.url()  == 'about:blank'
        pprint(page.close())
        pprint(page.close())

    # @sync
    # async def test_page(self):
    #     page = await self.api_playwright.page()
    #     assert type(page) is Page
    #     assert str(page)  == "<Page url='about:blank'>"
    #
    # def test_url(self):
    #     assert self.api_playwright.url() == 'about:blank'
    #
    # @sync
    # async def test_connect_over(self):
    #     playwright = await async_playwright().start()
    #     browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    #     page = await browser.new_page()
    #     pprint(page.url)
    #
    #     await page.goto("https://www.google.com/404")
    #
    #     aa = 13
    #
    #     # return
    #     # self.log_info("before sync_playwright")
    #     # from playwright.sync_api import sync_playwright
    #     # with sync_playwright() as playwright:
    #     #     self.log_info("in with sync_playwright")
    #     #     browser = playwright.chromium.launch()
    #     #     self.log_info("got browser")
    #     #     context = browser.new_context()
    #     #     self.log_info("got context")
    #     #     page = context.new_page()
    #     #     self.log_info("got new page")
    #     #     page.goto("https://google.com")
    #     #     self.log_info("opened google.com")
    #     #     self.log_info("saving screenshot")
    #     #     content = page.content()
    #     #     html = page.inner_html("*")
    #     #     text = page.inner_text("*")
    #     #     self.log_info(f"got page content with size {len(content)}")
    #     #     self.log_info(f"got page html with size {len(html)}")
    #     #     self.log_info(f"got page text with size {len(text)}")
    #     #     page.screenshot(path="/tmp/browser_screenshot.png")
    #     #     self.log_info("saved screenshot")
    #     #     browser.close()
    #     #     self.log_info("brower closed")
    #
    # @sync
    # async def test_connect_over(self):
    #     playwright = await async_playwright().start()
    #     browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    #     default_context = browser.contexts[0]
    #     page            = default_context.pages[0]
    #     #page = await browser.new_page()
    #     #await default_context.new_page()
    #     #await page.goto("https://www.google.com")
    #     #pprint(page.url)
    #
    # # page.goto("https://www.google.com")
    # # page.goto("https://www.google.com")
    # # page.fill('textarea[name="q"]', 'owasp')
    # # page.press('textarea[name="q"]', 'Enter')
    # # page.wait_for_load_state('networkidle')
    #
    # # links = page.query_selector_all('a')
    # # for link in links:
    # #     url = link.get_attribute('href')
    # #     if url:
    # #         print(url)
    #
    # # print()
    # # #pprint(page.query_selector_all('textarea[name="q"]'))
    # # inputs = page.query_selector_all('textarea')
    # #
    # # for input_element in inputs:
    # #     # Get the value of the input element
    # #     value = input_element.input_value()
    # #     print(f"Input value: {value}")
    # #
    # #     # Get the type of the input element
    # #     input_type = input_element.get_attribute('type')
    # #     print(f"Input type: {input_type}")
    # # path="/tmp/browser_screenshot.png"
    # # pprint(len(page.screenshot(type='jpeg', quality=0, path=path)))
    #
    # # pprint(self.playwright_chrome_browser.page())
    #     # context = self.playwright_chrome_browser.context().new_page()
    #     # for page in self.playwright_chrome_browser.pages():
    #     #     page.bring_to_front()
    #     #     wait_for(1)
    #     #page.goto('http://news.bbc.co.uk')
    #     #page.close()
    #     # browser.new_page()
    #     # return
