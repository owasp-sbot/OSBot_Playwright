from playwright.sync_api import sync_playwright

class Playwright_Browser:

    def __init__(self):
        self.__playwright = None

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    def browser_via_cdp(self, browser_name, endpoint_url):
        browser_type = self.browser_type(browser_name)
        if browser_type:
            return browser_type.connect_over_cdp(endpoint_url)

    def browser_type(self, browser_name):
        if browser_name and hasattr(self.playwright(), browser_name):
            return getattr(self.playwright(), browser_name)

    def event_loop(self):
        if self.__playwright:
            return self.__playwright._loop

    def event_loop_closed(self):
        event_loop = self.event_loop()
        return event_loop is None or event_loop._closed is True

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