from osbot_utils.utils.Python_Logger import Python_Logger
from playwright.sync_api import sync_playwright, Browser,Error

from osbot_playwright.playwright.api.Playwright_Page import Playwright_Page


class Playwright_Browser:

    def __init__(self):
        self.__playwright = None
        self.logger = Python_Logger().setup()

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    def browser(self) -> Browser:
        raise Exception('browser() not implemented')

    #@cache_on_self                                         # todo: see if this is needed
    def browser_via_cdp(self, browser_name, endpoint_url):
        browser_type = self.browser_type(browser_name)
        if browser_type:
            return browser_type.connect_over_cdp(endpoint_url)

    def browser_type(self, browser_name):
        if browser_name and hasattr(self.playwright(), browser_name):
            return getattr(self.playwright(), browser_name)

    def contexts_close_all(self):
        contexts_closed = 0
        #pages_closed = 0
        contexts = self.contexts() or []
        for context in contexts:
            # for page in context.pages:
            #     self.logger.info(f"Closing page: {page}")
            #     self.close_page(page)
            #     # page.close()
            #     pages_closed += 1
            contexts_closed += 1
            try:
                self.context_close(context)     # todo: understand better the cases when this exception is thrown
            except Error as error:             # for the cases where the context has already been closed
                print(error)
                continue

        #message = f"Closed {pages_closed} pages and {contexts_closed} contexts"
        message = f"Closed {contexts_closed} contexts"
        self.logger.info(message)
        return contexts_closed

    def context_new(self, **kwargs):
        return self.browser().new_context(**kwargs)

    def context_close(self, context):
        context.close()

    def context(self, index=0):
        contexts = self.contexts()
        if contexts and len(contexts) > index:
            return contexts[index]

    def event_loop(self):
        if self.__playwright:
            return self.__playwright._loop

    def event_loop_closed(self):
        event_loop = self.event_loop()
        return event_loop is None or event_loop._closed is True

    def contexts(self):                                     # todo: add support for Playwright_Context
        if self.browser():
            return self.browser().contexts
        return []

    def page(self, context_index=0, page_index=0):
        pages = self.pages(context_index=context_index)
        if pages and len(pages) > page_index:
            return pages[page_index]
        return self.new_page()

    def pages(self, context_index=0):
        pages = []
        context = self.context(index=context_index)
        if context:
            for page in context.pages:
                pages.append(Playwright_Page(context=context, page=page))
        return pages

    def page_close(self, page):
        page.close()


    def playwright(self):
        if self.__playwright is None:
            self.__playwright = self.playwright_context_manager().start()
        return self.__playwright

    def playwright_context_manager(self):
        return sync_playwright()

    def new_page(self, context_index=0):
        context = self.context(index=context_index)
        if context:
            page = context.new_page()
            return Playwright_Page(context=context, page=page)

    def stop(self):
        if self.__playwright:
            self.__playwright.stop()
            self.__playwright = None
            return True
        return False