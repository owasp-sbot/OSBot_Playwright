import os

import requests
from dotenv                                         import load_dotenv
from osbot_playwright.playwright.Playwright_Page    import Playwright_Page
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from playwright.sync_api                            import sync_playwright

class API_Browserless:

    def __init__(self):
        self.current_page = None

    def __enter__(self):
        self.current_page = self.new_page()
        return self.current_page

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current_page.close()



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

    # todo move to separate class that is focused on these extra features provided by serverless

    def content(self, target):
        return self.requests_post('content', target).text

    def pdf(self, target,width=1024, height=1024):
        payload  =  { "url"      : target,
                     "options"   : { "printBackground": True, "displayHeaderFooter": True},
                     "viewport"  : { "width": width , "height": height} ,
                      "gotoOptions": {"waitUntil": "networkidle2" },
                      #"waitFor" : 15000
                      }
        url      = f"https://chrome.browserless.io/pdf?token={self.auth_key()}"
        response = requests.post(url=url, json=payload)
        return response.content

    def pdf_html(self, html ,width=1024, height=1024):
        payload  =  { "html"      : html,
                     "options"   : { "printBackground": True, "displayHeaderFooter": True},
                     "viewport"  : { "width": width , "height": height} ,
                      "gotoOptions": {"waitUntil": "networkidle0" },
                      #"waitFor" : 15000
                      }
        url      = f"https://chrome.browserless.io/pdf?token={self.auth_key()}"
        response = requests.post(url=url, json=payload)
        return response.content

    def screenshot(self, target, full_page=True, quality=75, type='jpeg', width=1024, height=1024):
        payload  =  { "url"      : target,
                      "options"   : { "fullPage": full_page, "quality": quality, "type": type},
                      "viewport"  : { "width": width , "height": height} ,
                      #"gotoOptions": {"waitUntil": "networkidle2" },
                      }
        url      = f"https://chrome.browserless.io/screenshot?token={self.auth_key()}"
        response = requests.post(url=url, json=payload)
        return response.content



    def stats(self, target):
        payload  =  {"url": target}
        url      = f"https://chrome.browserless.io/stats?token={self.auth_key()}"
        response = requests.post(url=url, json=payload)
        return response.json()

    def requests_get(self, function):
        url      = f"https://chrome.browserless.io/{function}?token={self.auth_key()}"
        response = requests.get(url=url)
        return response

    def requests_post(self, function, target):
        payload  =  {"url": target}
        url      = f"https://chrome.browserless.io/{function}?token={self.auth_key()}"
        response = requests.post(url=url, json=payload)
        return response