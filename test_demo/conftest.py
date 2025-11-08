import json
import logging
import os
import sys
import pytest
from datetime import datetime

sys.path[0] = os.getcwd()

from core import playwright_manager


def pytest_html_report_title(report):
    """Set custom HTML report title"""
    report.title = "example Automation Report - Playwright"


def pytest_addoption(parser):
    """Add command-line options for browser selection"""
    parser.addoption(
        "--browser_name",
        action="store",
        default='chrome',
        help="options: chrome | firefox | edge | webkit",
    )


@pytest.fixture(scope='session', autouse=True)
def setup(request):
    '''
    Session level - Setup:

    Session level scope items
    Since autouse is set to 'true' the setup will be run automatically.
    - config (updated in pytest namespace)
    - logger (default session level scope once initiated)
    - page (updated in pytest namespace)

    Session level - Teardown:

    - close context, browser, and stop playwright
    '''

    pytest.config = load_config()

    setup_custom_logger()

    # Initialize Playwright
    page, context, browser, playwright = initialize_playwright(
        request.config.getoption("browser_name")
    )
    
    pytest.page = page
    pytest.context = context
    pytest.browser = browser
    pytest.playwright_instance = playwright

    yield
    
    # Cleanup Playwright resources
    context.close()
    browser.close()
    playwright.stop()


def initialize_playwright(browser_name):
    '''
    Invoking playwright browser for provided browser
    
    Args:
        browser_name: Browser type ('chrome', 'firefox', 'edge', 'webkit')
    
    Returns:
        tuple: (page, context, browser, playwright) objects
    '''
    return playwright_manager.playwright_manager_factory(browser_name).create_browser()


def load_config():
    '''
    Reading config file to fetch url and credentials
    
    Returns:
        dict: Configuration dictionary
    '''
    with open("config.json") as f:
        return json.load(f)


def setup_custom_logger():
    '''
    Generates custom log report file of each testcase
    '''
    logger = logging.getLogger()
    
    file_handler = logging.FileHandler('custom_logfile.log', mode="w")
    formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s : %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


@pytest.fixture
def testdata(shared_datadir, request):
    """
    testdata provides the data for a test
    the details are fetched based on the caller's (test method) context [provided by request(built-in) fixture]

    .
    ├── data/
    │   └── example_bank_statement.json
    └── test_example_bank_statement.py

    the testdata fixture opens the file matching the module name (without 'test_') and
    will look for the key name which is the caller (test_method)
    Note: on the test_method also the 'test_*' will not be considered, since 'test_*' is dedicated to pytest patterns
    """

    # Get only the module name, not the full package path
    module_name = request.module.__name__.split('.')[-1]  # Gets last part after dots
    file_name = module_name[len("test_") :] + ".json"
    function_name = request.function.__name__[len("test_") :]
    return json.loads((shared_datadir / file_name).read_text())[function_name]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Capture screenshot on failure
            screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Create screenshots directory in report folder
            screenshot_dir = os.path.join('report', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            # Take screenshot
            pytest.page.screenshot(path=screenshot_path)
            
            if pytest_html:
                # Add screenshot to HTML report
                html = '<div><img src="screenshots/%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot_name
                extra.append(pytest_html.extras.html(html))
        
        report.extra = extra


def pytest_configure(config):
    """Configure pytest-html to handle assets properly"""
    # This ensures pytest-html can find the screenshots
    config._metadata = None