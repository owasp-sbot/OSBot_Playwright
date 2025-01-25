import os

from osbot_utils.utils.Env import load_dotenv

from osbot_fast_api.utils.http_shell.Http_Shell__Server import ENV__HTTP_SHELL_AUTH_KEY
from osbot_utils.utils.Dev import pprint

import osbot_playwright
from osbot_aws.deploy.Deploy_Lambda                          import Deploy_Lambda
from osbot_aws.helpers.Create_Image_ECR                      import Create_Image_ECR
from osbot_utils.testing.Duration                            import Duration
from osbot_utils.utils.Files                                 import  path_combine
from osbot_playwright.docker.images.osbot_playwright.handler import run


class Lambda__Docker_Playwright:

    def __init__(self):
        self.image_name       = 'osbot_playwright'
        self.path_images      = path_combine(osbot_playwright.path, 'docker/images')
        self.create_image_ecr =  Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)
        self.deploy_lambda    =  Deploy_Lambda(run)

    def api_docker(self):
        return self.create_image_ecr.api_docker

    def auth_key_lambda_shell(self):
        load_dotenv()
        return os.environ.get(ENV__HTTP_SHELL_AUTH_KEY)

    def create_lambda(self, delete_existing=False, wait_for_active=False):
        with Duration(prefix='[create_lambda] | delete and create:'):
            try:
                # image_architecture = self.image_architecture()                  # im OSX this will be 'arm64' (for M1 chips)
                # if image_architecture == 'amd64':                               # in Linux this will be 'amd64'
                #     image_architecture = 'x86_64'                               # handled the case where in lambda functions the amd64 architecture is called x86_64
                image_architecture = 'x86_64'                                     # for now only support building the docker image in GH which means that the image is 'x86_64'
                lambda_function              = self.lambda_function()
                lambda_function.image_uri    = self.image_uri()
                lambda_function.architecture = image_architecture
                lambda_function.memory       = 5092

                lambda_function.set_env_variable(ENV__HTTP_SHELL_AUTH_KEY, self.auth_key_lambda_shell())

                print('#'*100)
                print(f'image_architecture: {image_architecture}')

                if delete_existing:
                    lambda_function.delete()
                create_result = lambda_function.create()
                pprint(create_result)
                if wait_for_active:
                    with Duration(prefix='[create_lambda] | wait for active:'):
                        lambda_function.wait_for_state_active(max_wait_count=80)
                function_url = self.create_lambda_function_url()
                return dict(create_result=create_result, function_url=function_url)
            except Exception as error:
                return {"status": "error", "error": error}

    def create_lambda_function_url(self):
        lambda_           = self.lambda_function()
        lambda_.function_url_delete()                           # due to the bug in AWS it is better to delete and recreate it
        lambda_.function_url_create_with_public_access()
        return lambda_.function_url_info()

    def image_architecture(self):
        return self.create_image_ecr.docker_image.architecture()

    def execute_lambda(self,payload=None):
        lambda_function = self.lambda_function()
        result = lambda_function.invoke(payload=payload)
        return result

    def lambda_function(self):
        return self.deploy_lambda.lambda_function()

    def image_uri(self):
        return f"{self.repository()}:latest"

    def path_docker_playwright(self):
        return path_combine(osbot_playwright.path,'docker/images/osbot_playwright')

    def path_dockerfile(self):
        return f'{self.path_docker_playwright()}/dockerfile'

    def repository(self):
        return self.create_image_ecr.image_repository()

    def update_lambda_function(self):
        lambda_ = self.lambda_function()
        return lambda_.update_lambda_image_uri(self.image_uri())

    def url_shell_server(self):
        function_url = self.lambda_function().function_url()
        if function_url:
            return function_url + 'shell-server'

    # def build_docker_image(self):
    #     return self.build_docker_image()



    # def create_lambda_function(self, delete_existing=True, wait_for_active=True):
    #     return self.create_lambda(delete_existing=delete_existing, wait_for_active=wait_for_active)

    # def update_lambda_function(self, wait_for_update=True):
    #     result = self.update_lambda_function()
    #     if wait_for_update is False:
    #         return result.get('LastUpdateStatus')
    #     return self.lambda_function().wait_for_function_update_to_complete(wait_time=1)        # this takes a while so make the interval to be 1 sec before checks


    # def rebuild_and_publish(self):
    #     build_result   = self.build_docker_image()
    #     publish_result = self.publish_docker_image()
    #     update_result  = self.update_lambda_function()
    #     return dict(build_result=build_result, publish_result=publish_result, update_result=update_result)