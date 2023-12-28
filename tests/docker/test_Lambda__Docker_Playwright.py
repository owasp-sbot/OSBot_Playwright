from unittest import TestCase

import requests
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint

from osbot_playwright.docker.Build__Docker_Playwright import Build__Docker_Playwright
from osbot_playwright.docker.Lambda__Docker_Playwright import Lambda__Docker_Playwright


class test_Lambda__Docker_Playwright(TestCase):

    def setUp(self):
        self.lambda_docker = Lambda__Docker_Playwright()

    def test_create_lambda(self):
        delete_existing = True
        wait_for_active = True
        lambda_function = self.lambda_docker.lambda_function()
        with Duration(prefix='create lambda:'):
            create_result   = self.lambda_docker.create_lambda(delete_existing=delete_existing, wait_for_active=wait_for_active)

            pprint(create_result)

            assert lambda_function.exists() is True

            lambda_info     = lambda_function.info()
            if delete_existing is True:
                assert create_result.get('create_result').get('status') == 'ok'
            assert lambda_info.get('Configuration').get('State') == 'Active'

        with Duration(prefix='invoke lambda 1st:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda!!!!!"}'

        with Duration(prefix='invoke lambda 2nd:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda!!!!!"}'

        with Duration(prefix='invoke lambda 3rd:'):
            invoke_result   = lambda_function.invoke()
            assert invoke_result.get('body') == '{"message":"Hello from docked_playwright lambda!!!!!"}'

    def test_create_lambda_function_url(self):
        result       = self.lambda_docker.create_lambda_function_url()

        function_url = result.get('FunctionUrl')
        assert result.get('AuthType'   ) == 'NONE'
        assert result.get('FunctionArn') == self.lambda_docker.deploy_lambda.lambda_function().function_arn()
        assert result.get('InvokeMode' ) == 'BUFFERED'
        assert function_url.endswith('.lambda-url.eu-west-2.on.aws/')

        assert requests.get(function_url).json() == {'message': 'Hello from docked_playwright lambda!!!!!'}


    # def test_image_architecture(self):
    #     result = self.lambda_docker.create_image_ecr.ecr.client().describe_images(repositoryName='osbot_playwright', imageIds=[{'imageTag': 'latest'}])
    #     #result = self.lambda_docker.create_image_ecr.docker_image.info()
    #     pprint(result)

    def test_execute_lambda(self):
        result = self.lambda_docker.execute_lambda()
        assert result.get('body') == '{"message":"Hello from docked_playwright lambda!!!!!"}'

    def test_update_lambda_function(self):
        #pprint(self.build_deploy.lambda_function().info())
        result = self.lambda_docker.update_lambda_function()
        assert result.get('State') == 'Active'


    # def test_invoke_fast_api__docs(self):
    #     payload = {'path': 'docs'}
    #     result = self.lambda_docker.execute_lambda(payload=payload)
    #     pprint(result)

    #def test_invoke_lambda_shell(self):

        # aws_lambda = self.lambda_docker.lambda_function()
        # from osbot_aws.apis.shell.Shell_Client import Shell_Client
        # lambda_client = Shell_Client(aws_lambda)
        #
        # pprint(lambda_client.ping())

    # def test_z_aws_publish(self):
    #     #build_result = self.build_docker.build_docker_image()       # make sure the image is built
    #     #assert build_result.get('status') == 'ok'
    #
    #     result          = self.lambda_docker.create_image_ecr.push_image()
    #     auth_result     = result.get('auth_result')
    #     push_json_lines = result.get('push_json_lines')
    #     assert auth_result.get('Status') ==     'Login Succeeded'
    #     assert 'errorDetail'             not in push_json_lines