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
    parser.addoption(
        "--run-headed", action="store_true", default=False, help="Run browser in headed mode"
    )

@pytest.fixture(scope="session")
def browser_context_args(pytestconfig):
    headed = pytestconfig.getoption("--run-headed")
    return {"headless": not headed}

@pytest.fixture(scope="session")
def browser(browser_context_args):
    with sync_playwright() as playwright_instance:
        browser = playwright_instance.chromium.launch(headless=browser_context_args["headless"])
        yield browser
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
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