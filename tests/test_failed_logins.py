import os
import pytest
import dotenv
import logging
from utils.filepath import FilePath
from pages.pageactions import PageActions
from playwright.sync_api import  expect


dotenv.load_dotenv()

URL = os.getenv('URL')
INVALID_USER = os.getenv('INVALID_USER')
LOCKED_USER = os.getenv("LOCKED_USER")
INVALID_PASSWD = os.getenv('INVALID_PASSWD')
VALID_PASSWD = os.getenv("PASSWD")

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
    login_session = PageActions(web_page)

    yield {
        'web_page': web_page,
        'login_session': login_session
    }

    web_page.close()


def test_land_in_home_page(browser_context):
    """
    Test to verify successful landing on the application homepage.

    - Accesses the web page from the browser context.
    - Navigates to the application URL using `web_page.goto(URL)`.
    - Logs an informational message indicating successful landing.
    """
    web_page = browser_context["web_page"]
    web_page.goto(URL)
    logging.info("Landed in Homepage")


def test_failed_login(browser_context, request):
    """
    Test to verify failed login with invalid credentials.

    - Accesses the web page and login session from the browser context.
    - Attempts login using `login_session.login(INVALID_USER, INVALID_PASSWD)`.
    - Uses `expect` to verify the presence of an error message indicating invalid credentials.
    - Logs an informational message for capturing a screenshot of the failed login attempt.
    - Takes a screenshot of the web page using `web_page.screenshot` and saves it with a unique name.
    """
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]

    login_session.login(INVALID_USER, INVALID_PASSWD)
    expect(web_page.get_by_role('button', name='Epic sadface: Username and password do not match any user in this service'))

    logging.info('Failed Login Captured')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)


def test_locked_user(browser_context, request):
    """
    Test to verify behavior for a locked user attempting login.

    - Accesses the web page and login session from the browser context.
    - Attempts login using `login_session.login(LOCKED_USER, VALID_PASSWD)`.
    - Uses `expect` to verify the presence of an error message indicating a locked user.
    - Logs an informational message for capturing a screenshot of the locked user message.
    - Takes a screenshot of the web page using `web_page.screenshot` and saves it with a unique name.
    """
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]

    login_session.login(LOCKED_USER, VALID_PASSWD)
    expect(web_page.get_by_role('button', name='Epic sadface: Sorry, this user has been locked out.'))

    logging.info('Locked User Detected')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)