class Playwright_Page:

    def __init__(self, browser, context, page):
        self.browser = browser
        self.context = context
        self.page    = page

    def url(self):
        return self.page.url

    def close(self):
        return self.page.close()

    def goto(self, *args, **kwargs):
        return self.page.goto(*args, **kwargs)

    def open(self, url):
        return self.goto(url)