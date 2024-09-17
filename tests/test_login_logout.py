import os
import pytest
import dotenv
import logging
from pages.webpage import WebPage
from pages.pageactions import PageActions
from utils.filepath import FilePath
from playwright.sync_api import expect

dotenv.load_dotenv()

URL = os.getenv('URL')
VISUAL_USER = os.getenv('VISUAL_USER')
PASSWD = os.getenv('PASSWD')

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

def test_home_page(browser_context, request):
    web_page = browser_context["web_page"]
    web_page.go_to_page(URL)
    expect(web_page.page.get_by_text('Swag Labs')).to_be_visible()
    logging.info('Swag Labs Header Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.page.screenshot(path=file_name)


def test_login(browser_context, request):
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]
    login_session.login(VISUAL_USER, PASSWD)
    expect(web_page.page.locator("//span[@class='title' and contains(text(), 'Products')]")).to_be_visible()
    logging.info('Products Title Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.page.screenshot(path=file_name)

def test_logout(browser_context, request):
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]
    login_session.logout()
    expect(web_page.page.get_by_role('button')).to_be_visible()
    logging.info('Login button found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.page.screenshot(path=file_name)