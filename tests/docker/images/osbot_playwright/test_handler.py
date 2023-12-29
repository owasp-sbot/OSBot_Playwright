from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_playwright.docker.images.osbot_playwright.handler import run


class test_handler(TestCase):

    def test_run(self):
        pprint(run)