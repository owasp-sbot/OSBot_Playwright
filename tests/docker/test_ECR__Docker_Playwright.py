from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_playwright.docker.ECR__Docker_Playwright import ECR__Docker_Playwright


class test_ECR__Docker_Playwright(TestCase):

    def setUp(self):
        self.ecr_docker = ECR__Docker_Playwright()

    def test_ecr_setup(self):
        result = self.ecr_docker.ecr_setup()
        assert result is True

    def test_publish_docker_image(self):
        result = self.ecr_docker.publish_docker_image()
        pprint(result)