from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from starlette.responses import HTMLResponse, StreamingResponse

from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes

ROUTES_METHODS__PLAYWRIGHT = ['code'            ,'html'            , 'screenshot'            ]
ROUTES_PATHS__PLAYWRIGHT   = ['/playwright/code','/playwright/html', '/playwright/screenshot']

class CodeData(BaseModel):
    auth_key: str
    code    : str


class Routes__Playwright(Fast_API_Routes):

    def __init__(self,app):
        super().__init__(app, 'playwright')


    def add_route_code(self):
        @self.router.post('/code')
        def code(code_data: CodeData):
            return code_data

    # def code(self, code):
    #     return code

    def html(self, url):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
                page    = browser.new_page()
                page.goto(url)
                html_content = page.content()
                return HTMLResponse(content=html_content, status_code=200)
        except Exception as error:
            return f'{error}'

    def screenshot(self, url):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
                page = browser.new_page()
                page.goto(url)
                screenshot_bytes = page.screenshot(full_page=True)
                return StreamingResponse(content=iter([screenshot_bytes]), media_type="image/png")
        except Exception as error:
            return f'{error}'

    def setup_routes(self, router=None):
        self.add_route_code()
        #self.add_route_post(self.code     )
        self.add_route_get(self.html      )
        self.add_route_get(self.screenshot)

