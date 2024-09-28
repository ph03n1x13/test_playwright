class PageActions:
    """
    This class provides methods for interacting with a web page, https://www.saucedemo.com/, using Playwright.

    It takes a Playwright browser page instance as an argument during initialization.

    Attributes:
        page (playwright.page): The Playwright browser page instance.
    """

    def __init__(self, page):
        """
        Initializes the PageActions instance with a Playwright browser page.

        Args:
            page (playwright.page): The Playwright browser page instance.
        """
        self.page = page

    def login(self, user_name: str, passwd: str):
        """
        Logs in to a web page using the provided username and password.

        Args:
            user_name (str): The username to use for login.
            passwd (str): The password to use for login.
        """
        self.page.get_by_placeholder("Username").click()
        self.page.get_by_placeholder("Username").fill(user_name)
        self.page.get_by_placeholder("Password").click()
        self.page.get_by_placeholder("Password").fill(passwd)
        self.page.get_by_role("button", name="Login").click()

    def logout(self):
        """
        Logs out of the currently accessed web page.
        """
        self.page.get_by_role("button", name='Open Menu').click()
        self.page.locator("//a[@id='logout_sidebar_link']").click()