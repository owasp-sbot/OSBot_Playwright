from unittest                                       import TestCase
from osbot_utils.utils.Files                        import folder_exists, parent_folder, current_temp_folder
from osbot_utils.utils.Misc                         import list_set
from osbot_playwright.playwright.Playwright_Install import Playwright_Install, SUPORTTED_BROWSERS


class test_Playwright_Install(TestCase):

    def setUp(self) -> None:
        self.playwright_install = Playwright_Install()

    def test_browser_details(self):
        browsers_details = self.playwright_install.browsers_details()
        assert list_set(browsers_details) == SUPORTTED_BROWSERS
        for browser_name in SUPORTTED_BROWSERS:
            browser_details = browsers_details.get(browser_name)
            assert list_set(browser_details) == ['download_url', 'executable_paths', 'install_location', 'installed', 'version']
            if browser_details.get('installed'):
                assert folder_exists(browser_details.get('install_location')) is True


    def test_browsers_executable_paths(self):
        executable_paths = self.playwright_install.browsers_executable_paths()
        assert list_set(executable_paths) == SUPORTTED_BROWSERS
        for browser_name in SUPORTTED_BROWSERS:
            assert browser_name   in executable_paths[browser_name]

    def test_path_browsers(self):
        path_browsers = self.playwright_install.path_browsers()
        assert folder_exists(path_browsers) is True
        assert parent_folder(path_browsers) == current_temp_folder()