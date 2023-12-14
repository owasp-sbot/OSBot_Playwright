from unittest import TestCase

import pytest
from playwright.sync_api import Browser
from osbot_playwright.playwright.API_Browserless import API_Browserless
from osbot_playwright.playwright.Playwright_Page import Playwright_Page
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_create_from_bytes, file_exists, file_delete, file_create
from osbot_utils.utils.Json import json_save_file
from osbot_utils.utils.Misc import wait_for
from osbot_utils.utils.Str import str_safe


class test_API_Browserless(TestCase):
    api_browserless : API_Browserless()
    browser         : Browser

    @classmethod
    def setUpClass(cls):
        cls.api_browserless = API_Browserless()
        cls.browser         = cls.api_browserless.browser()

        assert type(cls.browser) is Browser

    def test_api_key(self):
        assert type(self.api_browserless.auth_key()) is str

    def test_browser(self):
        assert type(self.browser) == Browser


    def test_context(self):
        context = self.browser.contexts[0]

        assert len(self.browser.contexts)         == 1
        assert len(context.pages)                 == 1
        assert len (self.api_browserless.pages()) == 1
        assert context.pages[0].url == 'about:blank'
        assert self.api_browserless.pages()[0].page    == context.pages[0]
        assert self.api_browserless.pages()[0].context == context

    def test_new_page(self):
        assert len(self.api_browserless.pages()) == 1
        page  = self.api_browserless.new_page()
        pages = self.api_browserless.pages()
        assert type(page) == Playwright_Page
        assert len(pages) == 2
        assert pages[1].page == page.page
        assert page.url() == 'about:blank'
        target = 'https://www.google.com/404'
        page.open(target)
        assert page.url() == target
        assert page.html().title() == 'Error 404 (Not Found)!!1'
        assert page.html().tags__text('ins') == ['That’s an error.', 'That’s all we know.']
        assert 'Google' in page.html_raw()
        page.close()
        assert len(self.api_browserless.pages()) == 1

    def test_page_capture_requests(self):
        assert len(self.api_browserless.pages()) == 1
        page = self.api_browserless.new_page()
        assert len(page.captured_requests) == 0
        page.capture_requests()
        page.open('https://www.google.com')
        assert len(page.captured_requests) > 10
        page.close()
        assert len(self.api_browserless.pages()) == 1

    def test_pages(self):
        pages = self.api_browserless.pages()
        assert len(pages) == 1
        assert pages[0].page == self.api_browserless.page().page


    def test_wss_url(self):
        assert self.api_browserless.wss_url() == f'wss://chrome.browserless.io?token={self.api_browserless.auth_key()}'


    @pytest.mark.skip('refactor into main api_browserless class and support for controlling where the file is saved')
    def test_trace(self):
        assert len(self.api_browserless.pages()) == 1
        with self.api_browserless as page:
            context = self.api_browserless.context()
            context.tracing.start(screenshots=True, snapshots=True) # other options: name=name, title=title, sources=sources,
            page.goto("https://www.google.com")
            context.tracing.stop(path="trace.zip")
            pprint(page.url())
        assert len(self.api_browserless.pages()) == 1




    #########
    # extra browserless features

    # def test_content(self):
    #     url_target = 'https://www.google.com/'
    #     file_target = f'/tmp/browserless_content__{str_safe(url_target)}.json'
    #     stats  = self.api_browserless.content(url_target)
    #     json_save_file(stats, file_target)
    #     pprint(stats)

    def test_pdf(self):
        url_target = 'https://www.google.com'
        file_target = f'/tmp/browserless_screenshot__{str_safe(url_target)}.pdf'
        file_delete(file_target)
        bytes  = self.api_browserless.pdf(url_target, width=1248)
        if len(bytes) < 1000:
            pprint(bytes)
        else:
            file_create_from_bytes(file_target, bytes)
            pprint(f'saved pdf to: {file_target} with {len(bytes)} bytes')
        assert file_exists(file_target)

    def test_pdf_html(self):
        html = self.html_bootstrap()
        file_target = f'/tmp/browserless_screenshot__html.pdf'
        file_create(file_target+'.html', html)
        file_delete(file_target)
        bytes  = self.api_browserless.pdf_html(html, width=2248)
        if len(bytes) < 1000:
            pprint(bytes)
        else:
            file_create_from_bytes(file_target, bytes)
            pprint(f'saved pdf to: {file_target} with {len(bytes)} bytes')
        assert file_exists(file_target)

    def test_screenshot(self):
        url_target = 'https://www.google.com'
        file_target = f'/tmp/browserless_screenshot__{str_safe(url_target)}.png'
        file_delete(file_target)
        bytes  = self.api_browserless.screenshot(url_target, width=1248)
        if len(bytes) < 1000:
            pprint(bytes)
        else:
            file_create_from_bytes(file_target, bytes)
            pprint(f'saved screenshot to: {file_target} with {len(bytes)} bytes')
        assert file_exists(file_target)




    # def test_stats(self):
    #     url_target = 'https://www.google.com'
    #     file_target = f'/tmp/browserless_stats__{str_safe(url_target)}.json'
    #     stats  = self.api_browserless.stats(url_target)
    #     json_save_file(stats, file_target)
    #     pprint(stats)
    #     #pprint(stats)

    # # experiment to try to load all images from a page
    # def test_page__screenshot(self):
    #     count = 0
    #     def handle_request(request):
    #         nonlocal count
    #         count += 1
    #         print(count,"A request was made:", request.url)
    #         # Check if the request resource type is image
    #         #if request.resource_type == "image":
    #         #    image_urls.append(request.url)
    #
    #
    #     url_target = 'https://thehackernews.com/'
    #     file_target = f'/tmp/browserless_screenshot__{str_safe(url_target)}.png'
    #     page = self.api_browserless.page()
    #     page.page.set_viewport_size({"width": 1024, "height": 4080});
    #
    #     page.page.on("requestfinished", handle_request)
    #
    #
    #     page.open(url_target)
    #
    #     payload = {"path": file_target,
    #                "full_page": True,
    #                "quality": 5,
    #                "type": "jpeg",
    #                #"viewport": {"width": 1224, "height": 1512},
    #                #"gotoOptions": {"waitUntil": "networkidle2"},
    #                }
    #
    #     #wait_for(10)
    #     bytes = page.screenshot(**payload)
    #
    #     pprint(f'saved screenshot to: {file_target} with {len(bytes)} bytes')

    def html_bootstrap(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simple Bootstrap Page</title>  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
</head>
<body>

  <!-- Navigation -->
  <nav class="navbar navbar-expand navbar-dark bg-primary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">MySite</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Features</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Pricing</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">About</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <div class="p-5 mb-4 bg-light rounded-3">
    <div class="container-fluid py-5">
      <h1 class="display-5 fw-bold">Welcome to MySite</h1>
      <p class="col-md-8 fs-4">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content.</p>
      <button class="btn btn-primary btn-lg" type="button">Learn more</button>
    </div>
  </div>

  <!-- Footer -->
  <footer class="bg-light text-center text-lg-start">
    <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
      © 2023 MySite:
      <a class="text-dark" href="https://mysite.com/">mysite.com</a>
    </div>
  </footer>
</body>
</html>
"""