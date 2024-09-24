class WebPage:

    def __init__(self, browser_context):
        self.page = browser_context.new_page()


    def go_to_page(self, url: str):
        self.page.goto(url)


    def close_browser(self):
        self.page.close() # close the webpage context
                