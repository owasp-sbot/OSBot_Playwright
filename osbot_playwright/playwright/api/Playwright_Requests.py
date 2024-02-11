from osbot_utils.utils.Json import json_load_file, json_save_file
from osbot_utils.utils.Objects import obj_info


class Playwright_Requests:

    def __init__(self):
        self.requests = []
        self.frames   = []
        self.routes   = []

    def capture_frame(self, frame):
        frame = { 'name' : frame.name,
                  'url'  : frame.url }
        self.frames.append(frame)

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

    def capture_route(self, route, request ):
        #self.routes.append({'route' : route, 'request': request})
        self.routes.append(route)
        if False:
            route.abort()               # todo add support for blocking requests
        else:
            route.continue_()

    def load_from(self, path):
        self.requests = json_load_file(path)
        return self

    def save_to(self, path=None):
        return json_save_file(python_object=self.requests, path=path)


    # todo: add support for also capturing console messages
    # def handle_console_message(msg):
    #         obj_info(msg)
    #         # You can filter out messages by type (msg.type) or text content (msg.text)
    #         if "Autofocus processing was blocked" in msg.text:
    #             return True # Ignore this specific message
    #         # if "Permissions policy violation" in msg.text:
    #         #     return
    #
    #         print('----', msg.text)
    #
    #     raw_page.on("console", handle_console_message)