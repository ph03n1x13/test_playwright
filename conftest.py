"""
Import modules for testing and browser interaction.

- os: for file path manipulation
- pytest: for testing framework
- pytest_html: for generating HTML reports
- datetime: for generating timestamps
- playwright.sync_api: for launching and managing browsers

Additionally, import the FilePath class from the 'utils.filepath' module.
"""

import os
import pytest
import pytest_html
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.filepath import FilePath


filepath = FilePath()
screenshot_dir_path = filepath.screenshot_dir_path()
report_dir = filepath.report_dir_path()


def pytest_addoption(parser):
    """
    Add command-line options for browser behavior during tests:

    - --run-headed: Run the browser in headed mode (default: False)
    - --slow-mo: Run the browser with a delay between actions (in milliseconds, default: 0)
    """
    parser.addoption(
        "--run-headed", action="store_true", default=False, help="Run browser in headed mode"
    )
    # Option for slow motion (in milliseconds)
    parser.addoption(
        "--slow-mo", action="store", default=0, type=int, help="Run browser with slow motion (ms delay between actions)"
    )

@pytest.fixture(scope="session")
def browser_context_args(pytestconfig):
    """
Fixture to get browser context arguments based on command-line options:

- headed: Flag to control headless mode (derived from --run-headed option)
- slow_mo: Delay between browser actions (derived from --slow-mo option)

Returns a dictionary containing headless and slow_mo values.
"""
    headed = pytestconfig.getoption("--run-headed")
    slow_mo = pytestconfig.getoption("--slow-mo")
    return {
        "headless": not headed,
        "slow_mo": slow_mo
    }

@pytest.fixture(scope="session")
def browser(browser_context_args):
    """
Fixture to launch and manage the browser instance:

- Uses sync_playwright() to create a Playwright instance.
- Launches a Chromium browser based on headless and slow_mo arguments.
- Yields the browser instance for tests.
- Closes the browser instance after tests finish.
"""
    with sync_playwright() as playwright_instance:
        # Launch browser with headless and slow_mo options
        browser = playwright_instance.chromium.launch(
            headless=browser_context_args["headless"],
            slow_mo=browser_context_args["slow_mo"]
        )
        yield browser
        browser.close()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
Hook to capture screenshots for passed tests and add them to the report.

- outcome: The result of the test execution.
- report: The test report object.
- extras: A list containing additional information attached to the report.

If the test passes:
    - Constructs the expected screenshot path based on test ID and sanitized name.
    - Checks if the screenshot exists.
    - If the screenshot exists, adds it as an image attachment to the report.
    - Optionally, adds a success message to the report.
    - Updates the report's extras with the new information.
"""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.passed:
        # Construct the expected screenshot path
        screenshot_dir = screenshot_dir_path
        sanitized_nodeid = item.nodeid.replace("::", "_").replace("/", "_")
        screenshot_path = os.path.join(screenshot_dir, f"{sanitized_nodeid}.png")
        if os.path.exists(screenshot_path):
            extras.append(pytest_html.extras.image(screenshot_path))
        # Add a success message (optional)
        extras.append(pytest_html.extras.html("<div>Log of Passed Tests</div>"))
        report.extras = extras


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure unique report name for each test session."""
    test_files = config.args
    test_name = os.path.splitext(os.path.basename(test_files[0]))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"{test_name}_{timestamp}.html")
    config.option.htmlpath = report_file