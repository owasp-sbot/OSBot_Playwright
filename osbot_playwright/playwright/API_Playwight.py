from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from playwright.sync_api import Browser

from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Chrome_Browser import Playwright_Chrome_Browser
from osbot_playwright.playwright.Playwright_Page import Playwright_Page


class API_Playwright:

    def __init__(self, headless=True):
        self.headless                  = headless
        self.playwright_browser_chrome =  Playwright_Browser__Chrome()

    #@cache_on_self
    # def browser(self) -> Playwright_Chrome_Browser:
    #     if self.playwright_browser_chrome is None:
    #         self.playwright_browser_chrome = Playwright_Chrome_Browser(headless=self.headless)
    #         self.playwright_browser_chrome.setup()
    #     return self.playwright_browser_chrome

    @cache_on_self
    def browser(self) -> Browser :
        return self.playwright_browser_chrome.browser()

    def browser_close(self):
        return self.playwright_browser_chrome.stop_playwright_and_process()

    def page(self):
        pages = self.pages()
        if pages:
            return pages[0]
        return self.new_page()

    def pages(self):
        return self.browser().contexts[0].pages

    # def goto(self, url):
    #     page = self.page()
    #     return page.goto(url)

    def new_page(self):
        browser = self.browser()
        if browser:
            context = browser.contexts[0]
            page = context.new_page()
            return Playwright_Page(context=context, page=page)


    # def url(self):
    #     page = self.page()
    #     return page.url


    #
    # def close(self):
    #     self.page.close()
    #     self.browser.close()
