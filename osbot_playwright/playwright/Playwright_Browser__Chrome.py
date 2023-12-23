from osbot_playwright.playwright.Playwright_Browser import Playwright_Browser


class Playwright_Browser__Chrome(Playwright_Browser):

    def __init__(self):
        super().__init__()

    def chromium(self):
        return self.playwright().chromium

    def chromium_exe_path(self):
        return self.chromium().executable_path

    def download_to_folder(self, folder):
        return self.chromium().install(browser_path=folder)
