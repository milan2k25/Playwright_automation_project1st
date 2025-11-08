"""
Custom exceptions for Playwright automation to provide more specific error messages
Similar to Selenium exceptions for better debugging
"""


class NoSuchElementException(Exception):
    """
    Raised when element is not found in the DOM
    Similar to Selenium's NoSuchElementException
    """
    pass


class ElementNotVisibleException(Exception):
    """
    Raised when element exists in DOM but is not visible
    """
    pass


class ElementNotInteractableException(Exception):
    """
    Raised when element is visible but not interactable (disabled, readonly, etc.)
    """
    pass


class ElementClickInterceptedException(Exception):
    """
    Raised when element click is intercepted by another element
    (e.g., overlay, modal, loading spinner covering the element)
    Similar to Selenium's ElementClickInterceptedException
    """
    pass


class StaleElementReferenceException(Exception):
    """
    Raised when element reference becomes stale (removed from DOM or page reloaded)
    Similar to Selenium's StaleElementReferenceException
    """
    pass


class TimeoutException(Exception):
    """
    Raised when operation times out
    """
    pass


class InvalidSelectorException(Exception):
    """
    Raised when locator/selector syntax is invalid
    """
    pass
