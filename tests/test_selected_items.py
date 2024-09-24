import os
from lib2to3.fixes.fix_input import context

import pytest
import dotenv
import logging
from utils.filepath import FilePath
from playwright.sync_api import expect
from pages.pageactions import PageActions
import elements.product_elements as productpage
import elements.cartpage_elements as cartpage


dotenv.load_dotenv()

URL = os.getenv('URL')
VISUAL_USER = os.getenv('STANDARD_USER')
PASSWD = os.getenv('PASSWD')

file_path = FilePath()


@pytest.fixture(scope="module")
def browser_context(browser):
    web_page = browser.new_page()
    login_session = PageActions(web_page) # pass the page context as input
    selected_items = []

    yield {
        'web_page' : web_page,
        'login_session': login_session,
        'selected_items': selected_items
    }
    # Close the browser entity after each test
    web_page.close()

def test_home_page(browser_context, request):
    web_page = browser_context["web_page"]
    web_page.goto(URL)
    expect(web_page.get_by_text('Swag Labs')).to_be_visible()
    logging.info('Swag Labs Header Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)


def test_login(browser_context, request):
    web_page = browser_context["web_page"]
    login_session = browser_context["login_session"]
    login_session.login(VISUAL_USER, PASSWD)
    expect(web_page.locator("//span[@class='title' and contains(text(), 'Products')]")).to_be_visible()
    logging.info('Products Title Found')
    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name)


def test_add_products_to_cart(browser_context, request):
    web_page = browser_context["web_page"]
    selected_items = browser_context["selected_items"]
    # Hard coded ...I'm yet to relate product and add to cart button ¯\_(ツ)_/¯
    web_page.locator(productpage.ADD_BUTTONS).nth(0).click()
    selected_items.append(web_page.locator(productpage.PRODUCTS).nth(0).text_content())

    web_page.locator(productpage.ADD_BUTTONS).nth(1).click()
    selected_items.append(web_page.locator(productpage.PRODUCTS).nth(2).text_content())

    web_page.locator(productpage.ADD_BUTTONS).nth(2).click()
    selected_items.append(web_page.locator(productpage.PRODUCTS).nth(4).text_content())

    logging.info(selected_items)

    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name, full_page=True)


def test_go_to_your_cart_page(browser_context, request):
    web_page = browser_context["web_page"]

    # Go the Your Cart page
    web_page.locator(productpage.SHOPPING_CART_LOGO).click()
    expect(web_page.get_by_text('Your Cart')).to_be_visible()

    logging.info('Landed in Your Cart Page')

    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name, full_page=True)


def test_added_products_ok(browser_context, request):
    web_page = browser_context["web_page"]
    selected_items = browser_context["selected_items"]
    cart_items = web_page.locator(cartpage.CART_ITEM_NAMES).all_text_contents()
    for item in cart_items:
        assert item in selected_items

    logging.info('Added Items Matched')

    nodeid = request.node.nodeid.replace("::", "_").replace("/", "_")
    file_name = file_path.screenshot_path(f'{nodeid}.png')
    web_page.screenshot(path=file_name, full_page=True)