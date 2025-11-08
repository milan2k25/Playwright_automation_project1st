import pytest
import logging
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from helper.playwright_exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    InvalidSelectorException
)


def _check_element_state(locator_str: str, timeout: int = 2):
    """
    Internal method to check why element is not accessible and raise specific exception
    
    Args:
        locator_str: The locator string to check
        timeout: Quick timeout for state checking (default: 2s)
        
    Raises:
        NoSuchElementException: Element not in DOM
        ElementNotVisibleException: Element in DOM but not visible
        ElementNotInteractableException: Element visible but not interactable
        StaleElementReferenceException: Element reference is stale
        ElementClickInterceptedException: Element is covered by another element
    """
    try:
        element = pytest.page.locator(locator_str)
        
        # Check if element exists in DOM at all
        try:
            count = element.count()
            if count == 0:
                raise NoSuchElementException(
                    f"NoSuchElementException: Element not found in DOM.\n"
                    f"Locator: {locator_str}\n"
                    f"Current URL: {pytest.page.url}\n"
                    f"Page Title: {pytest.page.title()}\n"
                )
        except PlaywrightError as e:
            if "Selector" in str(e) or "parsing" in str(e).lower():
                raise InvalidSelectorException(
                    f"InvalidSelectorException: Invalid locator syntax.\n"
                    f"Locator: {locator_str}\n"
                    f"Error: {str(e)}"
                )
            raise NoSuchElementException(
                f"NoSuchElementException: Element not found in DOM.\n"
                f"Locator: {locator_str}\n"
                f"Current URL: {pytest.page.url}"
            )
        
        # Check if element reference is still valid (not stale)
        try:
            element.first.wait_for(state='attached', timeout=timeout*1000)
        except PlaywrightTimeoutError:
            raise StaleElementReferenceException(
                f"StaleElementReferenceException: Element is no longer attached to DOM.\n"
                f"Locator: {locator_str}\n"
                f"Current URL: {pytest.page.url}\n"
                f"Possible reasons:\n"
                f"  - Page was refreshed or navigated\n"
                f"  - Element was removed and re-added (DOM manipulation)\n"
                f"  - Dynamic content replaced the element"
            )
        except Exception as e:
            if "detached" in str(e).lower() or "stale" in str(e).lower():
                raise StaleElementReferenceException(
                    f"StaleElementReferenceException: Element reference is stale.\n"
                    f"Locator: {locator_str}\n"
                    f"Error: {str(e)}"
                )
        
        # Element exists, check if it's visible
        try:
            is_visible = element.first.is_visible()
            
            if not is_visible:
                raise ElementNotVisibleException(
                    f"ElementNotVisibleException: Element found in DOM but NOT visible.\n"
                    f"Locator: {locator_str}\n"
                    f"Current URL: {pytest.page.url}\n"
                    f"Element count: {count}\n"
                    f"Possible reasons:\n"
                    f"  - Element has display:none or visibility:hidden\n"
                    f"  - Element is off-screen or has zero dimensions\n"
                    f"  - Element is behind another element\n"
                    f"  - Parent element is hidden"
                )
        except (ElementNotVisibleException, StaleElementReferenceException):
            raise
        except Exception:
            pass
        
        # Element is visible, check if it's enabled/interactable
        try:
            is_enabled = element.first.is_enabled()
            if not is_enabled:
                raise ElementNotInteractableException(
                    f"ElementNotInteractableException: Element is visible but NOT interactable.\n"
                    f"Locator: {locator_str}\n"
                    f"Current URL: {pytest.page.url}\n"
                    f"Possible reasons:\n"
                    f"  - Element is disabled (disabled attribute)\n"
                    f"  - Element has readonly attribute\n"
                    f"  - Element is not ready for interaction\n"
                    f"  - JavaScript hasn't initialized the element yet"
                )
        except (ElementNotInteractableException, StaleElementReferenceException):
            raise
        except Exception:
            pass
        
        # Check if element is covered by another element (will cause click intercept)
        try:
            # Try to check if element is at the point where we'll click
            bounding_box = element.first.bounding_box()
            if bounding_box:
                # Check if element at center point is the one we're looking for
                center_x = bounding_box['x'] + bounding_box['width'] / 2
                center_y = bounding_box['y'] + bounding_box['height'] / 2
                
                element_at_point = pytest.page.evaluate(
                    f"document.elementFromPoint({center_x}, {center_y})"
                )
                
                # This is a basic check - if we can't click at center, element might be covered
                if element_at_point is None:
                    raise ElementClickInterceptedException(
                        f"ElementClickInterceptedException: Element is covered by another element.\n"
                        f"Locator: {locator_str}\n"
                        f"Current URL: {pytest.page.url}\n"
                        f"Possible reasons:\n"
                        f"  - Modal/overlay is covering the element\n"
                        f"  - Loading spinner is active\n"
                        f"  - Another element is positioned on top\n"
                        f"  - Fixed header/footer covering the element\n"
                        f"Suggestion: Wait for overlay to disappear or scroll element into view"
                    )
        except ElementClickInterceptedException:
            raise
        except Exception:
            # Can't determine if covered, skip this check
            pass
            
    except (NoSuchElementException, ElementNotVisibleException, 
            ElementNotInteractableException, StaleElementReferenceException,
            ElementClickInterceptedException, InvalidSelectorException):
        raise
    except Exception as e:
        logging.error(f"Unexpected error in _check_element_state: {str(e)}")


def is_element_clickable(locator: str, timeout=10):
    """
    Method to wait for element to be clickable and return the locator
    
    Args:
        locator: CSS selector or XPATH locator string
        timeout: Maximum wait time in seconds (default: 10)

    Returns:
        Locator object if element is clickable
    
    Raises:
        NoSuchElementException: Element not found in DOM
        ElementNotVisibleException: Element in DOM but not visible
        ElementNotInteractableException: Element visible but not clickable
        ElementClickInterceptedException: Element click is intercepted by another element
        StaleElementReferenceException: Element reference is stale
        InvalidSelectorException: Invalid locator syntax
        TimeoutException: Operation timed out
    """
    try:
        # Playwright auto-waits for element to be actionable
        element = pytest.page.locator(locator)
        element.first.wait_for(state='visible', timeout=timeout*1000)
        return element.first
    except PlaywrightTimeoutError as err:
        # Timeout occurred - figure out WHY
        logging.error(f"Timeout waiting for element: {locator}")
        _check_element_state(locator, timeout=2)
        
        # If _check_element_state didn't raise specific exception, raise generic timeout
        raise TimeoutException(
            f"TimeoutException: Timeout waiting for element to be clickable ({timeout}s).\n"
            f"Locator: {locator}\n"
            f"Current URL: {pytest.page.url}\n"
            f"Element might be loading or taking too long to appear"
        ) from err
    except PlaywrightError as err:
        # Check for specific Playwright errors
        error_msg = str(err).lower()
        
        if "intercept" in error_msg or "covered" in error_msg:
            raise ElementClickInterceptedException(
                f"ElementClickInterceptedException: Click was intercepted.\n"
                f"Locator: {locator}\n"
                f"Current URL: {pytest.page.url}\n"
                f"Error: {str(err)}\n"
                f"Suggestion: Element might be covered by modal, overlay, or loading spinner"
            ) from err
        elif "detached" in error_msg or "stale" in error_msg:
            raise StaleElementReferenceException(
                f"StaleElementReferenceException: Element reference is stale.\n"
                f"Locator: {locator}\n"
                f"Error: {str(err)}"
            ) from err
        elif "selector" in error_msg or "parsing" in error_msg:
            raise InvalidSelectorException(
                f"InvalidSelectorException: Invalid locator syntax.\n"
                f"Locator: {locator}\n"
                f"Error: {str(err)}"
            ) from err
        else:
            raise Exception(
                f"Unexpected Playwright error.\n"
                f"Locator: {locator}\n"
                f"Current URL: {pytest.page.url}\n"
                f"Error: {str(err)}"
            ) from err
    except (NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException,
            ElementClickInterceptedException, StaleElementReferenceException, 
            InvalidSelectorException, TimeoutException):
        # Re-raise specific exceptions
        raise
    except Exception as err:
        current_url = pytest.page.url
        page_title = pytest.page.title()
        raise Exception(
            f"Unexpected error while waiting for element.\n"
            f"Locator: {locator}\n"
            f"Current URL: {current_url}\n"
            f"Page Title: {page_title}\n"
            f"Error: {str(err)}"
        ) from err


def is_element_present(locator: str, timeout=10):
    """
    Method to wait for element to be present in DOM and return the locator
    
    Args:
        locator: CSS selector or XPATH locator string
        timeout: Maximum wait time in seconds (default: 10)
    
    Returns:
        Locator object if element is present
    
    Raises:
        NoSuchElementException: Element not found in DOM
        StaleElementReferenceException: Element reference is stale
        InvalidSelectorException: Invalid locator syntax
        TimeoutException: Operation timed out
    """
    try:
        element = pytest.page.locator(locator)
        element.first.wait_for(state='attached', timeout=timeout*1000)
        return element.first
    except PlaywrightTimeoutError as err:
        # Timeout occurred - check if element exists at all
        logging.error(f"Timeout waiting for element in DOM: {locator}")
        
        try:
            count = pytest.page.locator(locator).count()
            if count == 0:
                raise NoSuchElementException(
                    f"NoSuchElementException: Element not found in DOM.\n"
                    f"Locator: {locator}\n"
                    f"Current URL: {pytest.page.url}\n"
                    f"Possible reasons:\n"
                    f"  - Incorrect locator\n"
                    f"  - Element not loaded yet\n"
                    f"  - Wrong page"
                ) from err
            else:
                raise StaleElementReferenceException(
                    f"StaleElementReferenceException: Element found but couldn't attach to DOM.\n"
                    f"Locator: {locator}\n"
                    f"Current URL: {pytest.page.url}\n"
                    f"Found {count} matching element(s) but they're stale or being modified"
                ) from err
        except (NoSuchElementException, StaleElementReferenceException):
            raise
        except PlaywrightError as e:
            if "Selector" in str(e) or "parsing" in str(e).lower():
                raise InvalidSelectorException(
                    f"InvalidSelectorException: Invalid locator syntax.\n"
                    f"Locator: {locator}\n"
                    f"Error: {str(e)}"
                ) from err
            raise NoSuchElementException(
                f"NoSuchElementException: Element not found in DOM.\n"
                f"Locator: {locator}\n"
                f"Current URL: {pytest.page.url}"
            ) from err
        except Exception:
            raise TimeoutException(
                f"TimeoutException: Timeout waiting for element in DOM ({timeout}s).\n"
                f"Locator: {locator}\n"
                f"Current URL: {pytest.page.url}"
            ) from err
    except PlaywrightError as err:
        error_msg = str(err).lower()
        
        if "detached" in error_msg or "stale" in error_msg:
            raise StaleElementReferenceException(
                f"StaleElementReferenceException: Element reference is stale.\n"
                f"Locator: {locator}\n"
                f"Error: {str(err)}"
            ) from err
        elif "selector" in error_msg or "parsing" in error_msg:
            raise InvalidSelectorException(
                f"InvalidSelectorException: Invalid locator syntax.\n"
                f"Locator: {locator}\n"
                f"Error: {str(err)}"
            ) from err
        else:
            raise Exception(
                f"Unexpected Playwright error.\n"
                f"Locator: {locator}\n"
                f"Error: {str(err)}"
            ) from err
    except (NoSuchElementException, StaleElementReferenceException, 
            InvalidSelectorException, TimeoutException):
        raise
    except Exception as err:
        current_url = pytest.page.url
        raise Exception(
            f"Unexpected error while waiting for element in DOM.\n"
            f"Locator: {locator}\n"
            f"Current URL: {current_url}\n"
            f"Error: {str(err)}"
        ) from err


def wait_for_page_to_load(url: str, timeout=10):
    """
    Method to wait for page URL to contain specified substring
    
    Args:
        url: URL substring to wait for
        timeout: Maximum wait time in seconds (default: 10)
    
    Raises:
        PlaywrightTimeoutError: If URL doesn't contain substring within timeout
    """
    try:
        pytest.page.wait_for_url(f"**/*{url}*", timeout=timeout*1000)
    except PlaywrightTimeoutError as err:
        current_url = pytest.page.url
        raise PlaywrightTimeoutError(
            f"Expected URL not loaded within {timeout}s.\n"
            f"Expected to contain: {url}\n"
            f"Current URL: {current_url}"
        ) from err
    except Exception as err:
        current_url = pytest.page.url
        raise Exception(
            f"Failed while waiting for page to load.\n"
            f"Expected URL to contain: {url}\n"
            f"Current URL: {current_url}\n"
            f"Error: {str(err)}"
        ) from err


def accept_alert(timeout=5):
    """
    Accept alert/dialog if present
    
    Args:
        timeout: Maximum wait time in seconds (default: 5)
    
    Raises:
        TimeoutError: If no alert is present within timeout
    """
    try:
        # Playwright handles dialogs via event listeners
        pytest.page.on("dialog", lambda dialog: dialog.accept())
        logging.info("Alert handler registered")
    except Exception as err:
        raise Exception("Failed to handle alert") from err


def execute_script(script):
    """
    Execute JavaScript on the page
    
    Args:
        script: JavaScript code to execute
    
    Returns:
        Result of JavaScript execution
    """
    return pytest.page.evaluate(script)


def scroll_to_page_bottom():
    """
    Scroll to bottom of the page using JavaScript
    
    Returns:
        None
    """
    return pytest.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")


def scroll_to_element(locator: str):
    """
    Scroll element into view
    
    Args:
        locator: CSS selector or XPATH locator string
    
    Returns:
        None
    """
    element = pytest.page.locator(locator)
    element.scroll_into_view_if_needed()


def get_all_elements(locator: str):
    """
    Get all elements matching the locator
    
    Args:
        locator: CSS selector or XPATH locator string
    
    Returns:
        List of all matching element handles
    """
    return pytest.page.locator(locator).all()


def select_element_by_text(locator: str, text: str):
    """
    Select option from dropdown by visible text
    
    Args:
        locator: CSS selector or XPATH locator string
        text: Visible text of the option to select
    
    Returns:
        None
    """
    pytest.page.locator(locator).select_option(label=text)


def select_element_by_index(locator: str, index: int):
    """
    Select option from dropdown by index
    
    Args:
        locator: CSS selector or XPATH locator string
        index: Index of the option to select (0-based)
    
    Returns:
        None
    """
    pytest.page.locator(locator).select_option(index=index)


def select_element_by_value(locator: str, value: str):
    """
    Select option from dropdown by value attribute
    
    Args:
        locator: CSS selector or XPATH locator string
        value: Value attribute of the option to select
    
    Returns:
        None
    """
    pytest.page.locator(locator).select_option(value=value)


def get_dropdown_selection(locator: str):
    """
    Get currently selected option from dropdown
    
    Args:
        locator: CSS selector or XPATH locator string
    
    Returns:
        Text of the selected option
    """
    return pytest.page.locator(locator).input_value()
