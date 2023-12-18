from osbot_utils.utils.Json import json_load_file, json_save_file


class Playwright_Requests:

    def __init__(self):
        self.requests = []

    def capture_request(self, request):
        request = { 'frame'          : {'name': request.frame.name,
                                         'url': request.frame.url  } ,
                    'headers'        : request.headers              ,
                    'method'         : request.method               ,
                    'post_data'      : request.post_data            ,
                    'post_data_json' : request.post_data_json       ,
                    'redirected_from': request.redirected_from      ,
                    'redirected_to'  : request.redirected_to        ,
                    'resource_type'  : request.resource_type        ,
                    'timing'         : request.timing               ,
                    'url'            : request.url                  }
        self.requests.append(request)

    def load_from(self, path):
        self.requests = json_load_file(path)
        return self

    def save_to(self, path=None):
        return json_save_file(python_object=self.requests, path=path)