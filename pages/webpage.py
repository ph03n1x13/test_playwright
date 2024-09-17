from playwright.sync_api import sync_playwright


class WebPage:

    def __init__(self):
        # Start Playwright in synchronized mode
        self.playwright = sync_playwright().start()
        self.browser_context = self.playwright.chromium.launch(headless=False)
        self.trace_context = self.browser_context.new_context()
        self.page = self.browser_context.new_page()


    def go_to_page(self, url: str):
        self.page.goto(url)


    def close_browser(self):
        self.page.close() # close the webpage context
        self.playwright.stop() # finally stop the Playwright engine