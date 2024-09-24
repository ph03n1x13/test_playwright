import os
import pytest
import dotenv

dotenv.load_dotenv()

URL = os.getenv("PLAYWRIGHT_URL")


@pytest.fixture(scope="module")
def browser_context(browser):
    """
    Note: Docstring is generating using LLM Assistant::Gemini

    Fixture to provide a Playwright browser context with tracing enabled.

    Yields:
        dict: A dictionary containing a single key 'web_page' with an instance of the WebPage class.
    """

    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    web_page = browser.new_page()

    yield {
        'web_page': web_page,
    }

    context.tracing.stop(path='pl_trace.zip')
    web_page.close()

def test_go_to_page(browser_context):
    """
    Test that the WebPage object can navigate to a given URL.

    Args:
        browser_context (dict): The fixture providing the WebPage instance.
    """

    web_page = browser_context['web_page']
    web_page.goto(URL)


def test_keyboard_input(browser_context):
    """
    Test that the WebPage object can simulate keyboard input.

    Args:
        browser_context (dict): The fixture providing the WebPage instance.
    """

    web_page = browser_context['web_page']
    locator = web_page.get_by_role('button', name='Search')
    locator.press_sequentially("Trace", delay=1000)