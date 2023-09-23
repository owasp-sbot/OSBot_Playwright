from osbot_playwright.playwright.Playwright_Chrome_Browser import Playwright_Chrome_Browser


class API_Playwright:

    def __init__(self, headless=True):
        self.headless                  : bool                      = headless
        self.playwright_browser_chrome : Playwright_Chrome_Browser = None

    #@cache_on_self
    def browser(self) -> Playwright_Chrome_Browser:
        if self.playwright_browser_chrome is None:
            self.playwright_browser_chrome = Playwright_Chrome_Browser(headless=self.headless)
            self.playwright_browser_chrome.setup()
        return self.playwright_browser_chrome

    def browser_close(self):
        if self.playwright_browser_chrome:
            return self.playwright_browser_chrome.stop_process()

    def page(self):
        pages = self.pages()
        if pages:
            return pages[0]
        return self.new_page()

    def pages(self):
        return self.browser().pages()

    # def goto(self, url):
    #     page = self.page()
    #     return page.goto(url)

    def new_page(self):
        browser = self.browser()
        if browser:
            return browser.new_page()


    # def url(self):
    #     page = self.page()
    #     return page.url


    #
    # def close(self):
    #     self.page.close()
    #     self.browser.close()
