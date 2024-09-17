class PageActions:
    def __init__(self, page): # take a playwright browser instance for inheritance
        self.page = page

    def login(self, user_name: str, passwd: str):
        self.page.get_by_placeholder("Username").click()
        self.page.get_by_placeholder("Username").fill(user_name)
        self.page.get_by_placeholder("Password").click()
        self.page.get_by_placeholder("Password").fill(passwd)
        self.page.get_by_role("button", name="Login").click()


    def logout(self):
        self.page.get_by_role("button", name='Open Menu').click()
        self.page.locator("//a[@id='logout_sidebar_link']").click()
