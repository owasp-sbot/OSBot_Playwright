from playwright.sync_api import sync_playwright

class Playwright_Browser:

    def __init__(self, headless=True):
        self.headless    = headless
        self.__playwright = None

    def browser_chrome(self):               # todo refactor into separate class
        return self.playwright().chromium

    def browser_firefox(self):              # todo refactor into separate class
        return self.playwright().firefox

    def event_loop(self):
        if self.__playwright:
            return self.__playwright._loop

    def playwright(self):
        if self.__playwright is None:
            self.__playwright = self.playwright_context_manager().start()
        return self.__playwright

    def playwright_context_manager(self):
        return sync_playwright()

    def stop(self):
        if self.__playwright:
            self.__playwright.stop()
            self.__playwright = None
            return True
        return False