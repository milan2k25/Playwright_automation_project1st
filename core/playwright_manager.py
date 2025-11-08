from playwright.sync_api import sync_playwright
from interface import Interface, implements


def playwright_manager_factory(browser_type):
    """
    Factory function to return appropriate PlaywrightManager implementation
    based on browser type
    
    Args:
        browser_type: Browser type string ('chrome', 'firefox', 'edge', 'webkit')
    
    Returns:
        Appropriate PlaywrightManager implementation instance
    """
    b_type = browser_type.lower()

    if b_type in ['chrome', 'chromium']:
        return ChromiumPlaywrightManager()

    elif b_type in ['firefox']:
        return FirefoxPlaywrightManager()

    elif b_type in ['edge', 'msedge']:
        return EdgePlaywrightManager()

    elif b_type in ['webkit', 'safari']:
        return WebKitPlaywrightManager()

    else:
        # Default to Chromium
        return ChromiumPlaywrightManager()


class PlaywrightManager(Interface):
    """
    Interface for Playwright Browser Management
    All concrete implementations must implement these methods
    """

    def __init__(self):
        '''
        Initiate the Playwright instance and browser configuration
        '''
        pass

    def create_browser(self):
        '''
        Create and return Playwright page, context, browser, and playwright objects
        Returns: tuple(page, context, browser, playwright)
        '''
        pass


class ChromiumPlaywrightManager(implements(PlaywrightManager)):
    """
    Chromium/Chrome browser implementation using Playwright
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def create_browser(self):
        """
        Launch Chromium browser and create page context
        
        Returns:
            tuple: (page, context, browser, playwright) objects
        """
        self.playwright = sync_playwright().start()
        
        # Launch Chrome (Chromium)
        self.browser = self.playwright.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context with no viewport to allow maximized window
        self.context = self.browser.new_context(
            no_viewport=True
        )
        
        # Create page
        self.page = self.context.new_page()
        
        return self.page, self.context, self.browser, self.playwright


class FirefoxPlaywrightManager(implements(PlaywrightManager)):
    """
    Firefox browser implementation using Playwright
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def create_browser(self):
        """
        Launch Firefox browser and create page context
        
        Returns:
            tuple: (page, context, browser, playwright) objects
        """
        self.playwright = sync_playwright().start()
        
        # Launch Firefox
        self.browser = self.playwright.firefox.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context
        self.context = self.browser.new_context(
            no_viewport=True
        )
        
        # Create page
        self.page = self.context.new_page()
        
        return self.page, self.context, self.browser, self.playwright


class EdgePlaywrightManager(implements(PlaywrightManager)):
    """
    Microsoft Edge browser implementation using Playwright
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def create_browser(self):
        """
        Launch Edge browser and create page context
        
        Returns:
            tuple: (page, context, browser, playwright) objects
        """
        self.playwright = sync_playwright().start()
        
        # Launch Edge (using Chromium with Edge channel)
        self.browser = self.playwright.chromium.launch(
            channel='msedge',  # This launches Edge specifically
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context
        self.context = self.browser.new_context(
            no_viewport=True
        )
        
        # Create page
        self.page = self.context.new_page()
        
        return self.page, self.context, self.browser, self.playwright


class WebKitPlaywrightManager(implements(PlaywrightManager)):
    """
    WebKit/Safari browser implementation using Playwright
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def create_browser(self):
        """
        Launch WebKit browser and create page context
        
        Returns:
            tuple: (page, context, browser, playwright) objects
        """
        self.playwright = sync_playwright().start()
        
        # Launch WebKit (Safari engine)
        self.browser = self.playwright.webkit.launch(
            headless=False
        )
        
        # Create context
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Create page
        self.page = self.context.new_page()
        
        return self.page, self.context, self.browser, self.playwright
