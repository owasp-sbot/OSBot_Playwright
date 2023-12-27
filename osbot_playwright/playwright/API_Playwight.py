from playwright.sync_api import Browser
from osbot_playwright.playwright.Playwright_Page import Playwright_Page


class API_Playwright:

    def __init__(self, headless=True):
        self.headless                  = headless
        self.logger                    = None


    def browser(self) -> Browser:
        raise Exception('browser() not implemented')




    # def goto(self, url):
    #     page = self.page()
    #     return page.goto(url)


    # def url(self):
    #     page = self.page()
    #     return page.url


    #
    # def close(self):
    #     self.page.close()
    #     self.browser.close()
