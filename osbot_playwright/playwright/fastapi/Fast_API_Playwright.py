from osbot_fast_api.api.Fast_API import Fast_API
from osbot_utils.utils.Misc import list_set

from osbot_playwright.playwright.fastapi.Routes__Playwright import Routes__Playwright


class Fast_API_Playwright(Fast_API):
    def __init__(self):
        super().__init__()

    def setup_routes(self, app=None):
        self.add_routes(Routes__Playwright)
        self.add_shell_server()


