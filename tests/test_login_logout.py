import os
import pytest
import dotenv
import logging
from utils.filepath import FilePath
from pages.pageactions import PageActions
from playwright.sync_api import expect

dotenv.load_dotenv()

URL = os.getenv('URL')
VISUAL_USER = os.getenv('VISUAL_USER')
PASSWD = os.getenv('PASSWD')

file_path = FilePath()


@pytest.fixture(scope="module")
def browser_context(browser):
    """
Fixture to set up a browser page and login session for each test module.

- Creates a new Playwright browser page.
- Initializes a PageActions instance with the page as input.

Yields a dictionary containing the web_page and login_session objects.

- Closes the browser page after each test.
"""
    web_page = browser.new_page()
    login_session = PageActions(web_page) # pass the page context as input

    yield {
        'web_page' : web_page,
        'login_session': login_session
    }
    # Close the browser entity after each test
    web_page.close()

def test_home_page(browser_context, request):
    """
Test to verify the presence of the "Swag Labs" header on the home page.

- Accesses the web page from the browser context.
- Navigates to the application URL using `web_page.goto(URL)`.
- Uses `expect` to verify the visibility of the "Swag Labs" header element.
- Logs an informational message for capturing a screenshot of the home page.
- Takes a screenshot of the web page using `web_page.screenshot` and saves it with a unique name.
"""
    web_page = browser_context["web_page"]
    web_page.goto(URL)
    expect(web_page.get_by_text('Swag Labs')).to_be_visible()
    logging.info('Swag Labs Header Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)


def test_login(browser_context, request):
    """
Test to verify successful login and presence of the "Products" title after login.

- Accesses the web page and login session from the browser context.
- Performs login using `login_session.login(VISUAL_USER, PASSWD)`.
- Uses `expect` to verify the visibility of the "Products" title element after login.
- Logs an informational message for capturing a screenshot of the product page.
- Takes a screenshot of the web page using `web_page.screenshot` and saves it with a unique name.
"""
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]
    login_session.login(VISUAL_USER, PASSWD)
    expect(web_page.locator("//span[@class='title' and contains(text(), 'Products')]")).to_be_visible()
    logging.info('Products Title Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)

def test_logout(browser_context, request):
    """
Test to verify the presence of the login button after a successful logout.

- Accesses the web page and login session from the browser context.
- Performs logout using `login_session.logout()`.
- Uses `expect` to verify the visibility of the login button element.
- Logs an informational message for capturing a screenshot of the login page.
- Takes a screenshot of the web page using `web_page.screenshot` and saves it with a unique name.
"""
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]
    login_session.logout()
    expect(web_page.get_by_role('button')).to_be_visible()
    logging.info('Login button found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)