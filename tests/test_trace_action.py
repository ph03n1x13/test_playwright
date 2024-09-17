import pytest
import os
import dotenv
from playwright.sync_api import sync_playwright
from pages.tracable_webpage import WebPage  # Assuming 'pages.tracable_webpage' exists

dotenv.load_dotenv()

URL = os.getenv("PLAYWRIGHT_URL")


@pytest.fixture(scope="module")
def browser_context():
    """
    Note: Docstring is generating using LLM Assistant::Gemini

    Fixture to provide a Playwright browser context with tracing enabled.

    Yields:
        dict: A dictionary containing a single key 'web_page' with an instance of the WebPage class.
    """

    playwright_engine = sync_playwright().start()
    browser = playwright_engine.chromium.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    web_page = WebPage(context)

    yield {
        'web_page': web_page,
    }

    context.tracing.stop(path='pl_trace.zip')
    web_page.close_browser()
    playwright_engine.stop()


def test_go_to_page(browser_context):
    """
    Test that the WebPage object can navigate to a given URL.

    Args:
        browser_context (dict): The fixture providing the WebPage instance.
    """

    web_page = browser_context['web_page']
    web_page.go_to_page(URL)


def test_keyboard_input(browser_context):
    """
    Test that the WebPage object can simulate keyboard input.

    Args:
        browser_context (dict): The fixture providing the WebPage instance.
    """

    web_page = browser_context['web_page']
    locator = web_page.page.get_by_role('button', name='Search')
    locator.press_sequentially("Trace", delay=1000)