import os
import platform


def current_os():
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'macOS'          # fix this one since Darwin is an odd name
    return os_name              # usually: Linux or Windows

def in_mac():
    return current_os() == 'macOS'

def in_linux():
    return current_os() == 'Linux'

def in_windows():
    return current_os() == 'Windows'

def in_github_actions():
    return os.getenv('GITHUB_ACTIONS') == 'true'