from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Http import GET_json
from osbot_utils.utils.Misc import random_port

from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.Playwright_CLI import Playwright_CLI
from osbot_playwright.playwright.Playwright_Process import Playwright_Process


class Playwright_Browser__Chrome(Playwright_Browser):

    def __init__(self):
        super().__init__()
        self.playwright_cli     = Playwright_CLI()
        self.playwright_cli.set_os_env_for_browsers_path()

    def chromium(self):
        return self.playwright().chromium

    def chromium_exe_path(self):
        return self.chromium().executable_path

    def browser(self):
        endpoint = self.process().get('url')
        browser = self.chromium().connect_over_cdp(endpoint_url=endpoint)
        return browser

    def install(self):
        return self.playwright_cli.install__chrome()

    def is_installed(self):
        return self.playwright_cli.browser_installed__chrome()

    def playwright_process(self):
        return Playwright_Process(browser_path=self.chromium_exe_path(), headless=self.headless)

    def process(self):
        playwright_process = self.playwright_process()
        if playwright_process.process_running() is False:
            playwright_process.start_process()
        return playwright_process.process_details()

    def stop_playwright_and_process(self):
        playwright_process = self.playwright_process()
        self.stop()
        playwright_process.stop_process()
        result = (self              .event_loop_closed() is True and
                  playwright_process.process_running  () is False)
        return result

    # def ws_endpoint(self):
    #     return self.playwright_cli.url_browser_debug_page()
