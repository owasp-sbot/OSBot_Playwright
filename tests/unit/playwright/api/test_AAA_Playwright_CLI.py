from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import parent_folder, file_exists, files_list, files_find, files_recursive
from osbot_utils.utils.Misc import list_set

from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI, VERSION_PLAYWRIGHT


class test_AAA_Playwright_CLI(TestCase):            # todo: fix the need to use AAA to make sure this is the first class to execute (making sure that chrome is installed

    def setUp(self):
        self.playwright_cli = Playwright_CLI()

    def test__install__chrome(self):                                # add extra _ to name, so that this executes first (and installed Chromium locally)
        assert self.playwright_cli.install__chrome() is True

    def test_browser_installed__chrome(self):
        result = self.playwright_cli.browser_installed__chrome()
        assert type(result) is bool

    def test_dry_run(self):
        result = self.playwright_cli.dry_run()
        stdout = result.get('stdout')
        assert result.get('runParams') == ['playwright', 'install', '--dry-run']
        assert result.get('status'   ) == 'ok'
        assert result.get('stderr'   ) == ''
        assert 'browser: chromium '    in stdout
        assert 'browser: firefox '     in stdout
        assert 'browser: webkit '      in stdout

    def test_help(self):
        result = self.playwright_cli.help()
        assert 'Usage: playwright [options] [command]\n'in result

    def test_executable_path__chrome(self):
        executable_path      = self.playwright_cli.executable_path__chrome()
        assert file_exists(executable_path)

    def test_executable_version__chrome(self):
        version = self.playwright_cli.executable_version__chrome()
        assert version.startswith('Chromium')

    def test_install_details__chrome(self):
        install_details = self.playwright_cli.install_details__chrome()
        assert list_set(install_details) == ['download_fallback_1', 'download_fallback_2',
                                             'download_url', 'install_location', 'version']
        #assert install_details.get('browser').startswith('chromium')
        assert parent_folder(install_details.get('install_location')) ==  self.playwright_cli.path_browsers()

    def test_invoke_raw(self):
        result = self.playwright_cli.invoke_raw('help')
        assert list_set(result) == ['cwd', 'error', 'kwargs', 'runParams', 'status', 'stderr', 'stdout']
        assert result.get('status'   ) == 'ok'
        assert result.get('runParams') == ['playwright', 'help']
        assert result.get('stderr'   ) == ''
        assert result.get('stdout'   ).startswith('Usage: playwright [options] [command]')

    def test_version(self):
        assert self.playwright_cli.version() == VERSION_PLAYWRIGHT