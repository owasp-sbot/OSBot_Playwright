from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Http import GET_json
from osbot_utils.utils.Misc import random_port

from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.Playwright_CLI     import Playwright_CLI
from osbot_playwright.playwright.Playwright_Install import Playwright_Install
from osbot_playwright.playwright.Playwright_Process import Playwright_Process

CHROME_BROWSER_NAME   = 'chromium'
DEFAULT_HOST_ENDPOINT = 'http://localhost'

class Playwright_Browser__Chrome(Playwright_Browser):

    def __init__(self, port=None, headless=True):
        super().__init__()
        self.debug_port         = port or random_port()
        self.headless           = headless
        self.browser_name       = CHROME_BROWSER_NAME
        self.playwright_install = Playwright_Install()
        self.browser_details    = self.playwright_install.browser_details(self.browser_name)
        self.browser_exec_path  = self.browser_details.get('executable_path')
        self.playwright_process = Playwright_Process(browser_path=self.browser_exec_path, debug_port=self.debug_port, headless=self.headless)
        self.playwright_cli     = Playwright_CLI()
        self.playwright_cli.set_os_env_for_browsers_path()

    # def chromium(self):
    #     return self.playwright().chromium

    # def chromium_exe_path(self):
    #     return self.chromium().executable_path

    @cache_on_self
    def browser(self):
        if self.browser_process__start_if_needed() is False:
            raise Exception('Browser process not started/found')
        endpoint_url = self.endpoint_url()
        return self.browser_via_cdp(browser_name=self.browser_name, endpoint_url=endpoint_url)

    def browser_process__start_if_needed(self):
        return self.process() != {}

    def endpoint_url(self):
        return f'{DEFAULT_HOST_ENDPOINT}:{self.debug_port}'

    def install(self):
        return self.playwright_cli.install__chrome()

    def is_installed(self):
        return self.playwright_cli.browser_installed__chrome()

    def process(self):
        if self.playwright_process.process_running() is False:
            self.playwright_process.start_process()
        return self.playwright_process.process_details()

    def stop_playwright_and_process(self):
        self.stop()
        self.playwright_process.stop_process()
        result = (self              .event_loop_closed() is True and
                  self.playwright_process.process_running  () is False)
        return result