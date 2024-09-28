from playwright.sync_api import sync_playwright

"""
These are rough scripts for one time execution. You can ignore these
"""

playwright = sync_playwright().start()
chromium = playwright.chromium.launch(headless=False)
context = chromium.new_context()

context.tracing.start(screenshots=True, snapshots=True, sources=True)
page = context.new_page()
page.goto('https://playwright.dev/python/')
locator = page.get_by_role('button', name='Search')
locator.press_sequentially("Trace", delay=100)
context.tracing.stop(path='pl_trace.zip')