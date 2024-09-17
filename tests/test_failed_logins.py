import os
import pytest
import dotenv
import logging
from pages.webpage import WebPage
from pages.pageactions import PageActions
from utils.filepath import FilePath
from playwright.sync_api import sync_playwright, expect


dotenv.load_dotenv()

URL = os.getenv('URL')
INVALID_USER = os.getenv('INVALID_USER')
LOCKED_USER = os.getenv("LOCKED_USER")
INVALID_PASSWD = os.getenv('INVALID_PASSWD')
VALID_PASSWD = os.getenv("PASSWD")

file_path = FilePath()

@pytest.fixture(scope="module")
def browser_context():
    web_page = WebPage()
    login_session = PageActions(web_page.page) # pass the page context as input

    yield {
        'web_page' : web_page,
        'login_session': login_session
    }
    # Close the browser entity after each test
    web_page.close_browser()



def test_land_in_home_page(browser_context):
    web_page = browser_context["web_page"]
    web_page.go_to_page(URL)
    logging.info("Landed in Homepage")


def test_failed_login(browser_context, request):
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]

    login_session.login(INVALID_USER, INVALID_PASSWD)
    expect(web_page.page.get_by_role('button', name='Epic sadface: Username and password do not match any user in this service'))

    logging.info('Failed Login Captured')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.page.screenshot(path=file_name)

def test_locked_user(browser_context, request):
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]

    login_session.login(LOCKED_USER, VALID_PASSWD)
    expect(web_page.page.get_by_role('button', name='Epic sadface: Sorry, this user has been locked out.'))

    logging.info('Locked User Detected')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.page.screenshot(path=file_name)