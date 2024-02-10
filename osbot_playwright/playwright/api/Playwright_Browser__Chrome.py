from osbot_utils.utils.Misc import random_port
from osbot_playwright.playwright.api.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.api.Playwright_CLI     import Playwright_CLI
from osbot_playwright.playwright.api.Playwright_Install import Playwright_Install
from osbot_playwright.playwright.api.Playwright_Process import Playwright_Process

CHROME_BROWSER_NAME   = 'chromium'
DEFAULT_HOST_ENDPOINT = 'http://localhost'


# todo: handle better the case when the browser is updated and the FILE_NAME_BROWSER_DETAILS is out of date
#       in that case run:
#            self.playwright_browser_chrome.playwright_install.browsers_details(reset_data=True)
class Playwright_Browser__Chrome(Playwright_Browser):

    def __init__(self, port=None, headless=True):
        super().__init__()
        self._browser           = None
        self.debug_port         = port or random_port()
        self.headless           = headless
        self.browser_name       = CHROME_BROWSER_NAME
        self.playwright_install = Playwright_Install()
        self.browser_details    = self.playwright_install.browser_details(self.browser_name)
        self.browser_exec_path  = self.browser_details.get('executable_path')
        self.playwright_process = Playwright_Process(browser_path=self.browser_exec_path, debug_port=self.debug_port, headless=self.headless)
        self.playwright_cli     = Playwright_CLI()
        self.playwright_cli.set_os_env_for_browsers_path()

    def playwright_browser(self) -> Playwright_Browser:         # to help with code complete
        return self

    def browser(self):
        if self._browser is None:
            if self.browser_process__start_if_needed() is False:
                raise Exception('Browser process not started/found')
            endpoint_url = self.endpoint_url()
            self._browser = self.browser_via_cdp(browser_name=self.browser_name, endpoint_url=endpoint_url)
        return self._browser

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

    def restart(self):
        self._browser = None
        return self.playwright_process.restart_process()