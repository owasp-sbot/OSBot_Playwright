import os

from osbot_utils.utils.Env import load_dotenv

from osbot_playwright.playwright.api.Playwright_Browser import Playwright_Browser
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self

class API_Browserless(Playwright_Browser):

    def __init__(self):
        super().__init__()
        self.current_page = None
        #self.playwright   =  None

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
        #self.playwright = sync_playwright().start()
        #return self.playwright.chromium.connect_over_cdp(self.wss_url())
        return self.browser_via_cdp(browser_name='chromium', endpoint_url=self.wss_url())

    def close(self):
        self.playwright().stop()

    def wss_url(self):
        return f'wss://chrome.browserless.io?token={self.auth_key()}'

    # todo move to separate class that is focused on these extra features provided by serverless

    # def content(self, target):
    #     return self.requests_post('content', target).text
    #
    # def pdf(self, target,width=1024, height=1024):
    #     payload  =  { "url"      : target,
    #                  "options"   : { "printBackground": True, "displayHeaderFooter": True},
    #                  "viewport"  : { "width": width , "height": height} ,
    #                   "gotoOptions": {"waitUntil": "networkidle2" },
    #                   #"waitFor" : 15000
    #                   }
    #     url      = f"https://chrome.browserless.io/pdf?token={self.auth_key()}"
    #     response = requests.post(url=url, json=payload)
    #     return response.content
    #
    # def pdf_html(self, html ,width=1024, height=1024):
    #     payload  =  { "html"      : html,
    #                  "options"   : { "printBackground": True, "displayHeaderFooter": True},
    #                  "viewport"  : { "width": width , "height": height} ,
    #                   "gotoOptions": {"waitUntil": "networkidle0" },
    #                   #"waitFor" : 15000
    #                   }
    #     url      = f"https://chrome.browserless.io/pdf?token={self.auth_key()}"
    #     response = requests.post(url=url, json=payload)
    #     return response.content
    #
    # def screenshot(self, target, full_page=True, quality=75, type='jpeg', width=1024, height=1024):
    #     payload  =  { "url"      : target,
    #                   "options"   : { "fullPage": full_page, "quality": quality, "type": type},
    #                   "viewport"  : { "width": width , "height": height} ,
    #                   #"gotoOptions": {"waitUntil": "networkidle2" },
    #                   }
    #     url      = f"https://chrome.browserless.io/screenshot?token={self.auth_key()}"
    #     response = requests.post(url=url, json=payload)
    #     return response.content
    #
    # def stats(self, target):
    #     payload  =  {"url": target}
    #     url      = f"https://chrome.browserless.io/stats?token={self.auth_key()}"
    #     response = requests.post(url=url, json=payload)
    #     return response.json()
    #
    # def requests_get(self, function):
    #     url      = f"https://chrome.browserless.io/{function}?token={self.auth_key()}"
    #     response = requests.get(url=url)
    #     return response
    #
    # def requests_post(self, function, target):
    #     payload  =  {"url": target}
    #     url      = f"https://chrome.browserless.io/{function}?token={self.auth_key()}"
    #     response = requests.post(url=url, json=payload)
    #     return response