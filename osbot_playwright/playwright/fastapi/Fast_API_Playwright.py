from osbot_fast_api.api.Fast_API import Fast_API
from osbot_utils.utils.Misc import list_set


class Fast_API_Playwright(Fast_API):
    def __init__(self):
        super().__init__()

    def setup_routes(self):
        print('adding more routes')

        @self.app().get('/aaa')
        def aaa():
            return 42
