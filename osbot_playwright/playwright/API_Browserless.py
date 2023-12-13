import os
from dotenv import load_dotenv
from osbot_playwright.playwright.Playwright_Page import Playwright_Page
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from playwright.sync_api import sync_playwright

class API_Browserless:

    def __init__(self):
        pass

    @cache_on_self
    def auth_key(self):
        load_dotenv()
        return os.getenv('BROWSERLESS__API_KEY')

    @cache_on_self
    def browser(self):
        return sync_playwright().start().chromium.connect_over_cdp(self.wss_url())

    def context(self, index=0):
        contexts = self.contexts()
        if contexts and len(contexts) > index:
            return contexts[index]

    def contexts(self):
        return self.browser().contexts

    def new_page(self, context_index=0):
        context = self.context(index=context_index)
        if context:
            page = context.new_page()
            return Playwright_Page(context=context, page=page)

    def pages(self, context_index=0):
        pages = []
        context = self.context(index=context_index)
        if context:
            for page in context.pages:
                pages.append(Playwright_Page(context=context, page=page))
        return pages

    def page(self, context_index=0, page_index=0):
        pages = self.pages(context_index=context_index)
        if pages and len(pages) > page_index:
            return pages[page_index]

    def wss_url(self):
        return f'wss://chrome.browserless.io?token={self.auth_key()}'