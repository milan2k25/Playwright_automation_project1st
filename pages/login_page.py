import logging
import time
from helper import playwright_helper
from locators.login_page_locators import LoginPageLocators
from locators.home_page_locators import HomePageLocators


'''
Define All the common functionalities related to Login and Logout into example Application
'''


class exampleLoginPage:

    def __init__(self, page):
        self.page = page
        self.login_loc = LoginPageLocators
        self.home_loc = HomePageLocators

    def example_login(self, url, email, password):
        """
        Login to example application
        
        Args:
            url: Application URL
            email: User email
            password: User password
        """
        self.page.goto(url)

        try:
            time.sleep(1)
            playwright_helper.is_element_clickable(self.login_loc.SIGN_IN_XPATH).click()
            playwright_helper.is_element_clickable(self.login_loc.IP_EMAIL_XPATH, 30)
            time.sleep(2)
            playwright_helper.is_element_clickable(self.login_loc.IP_EMAIL_XPATH).fill(email)
            playwright_helper.is_element_clickable(self.login_loc.SUBMIT_BTN).click()
            playwright_helper.is_element_clickable(self.login_loc.IP_PASSWORD_XPATH, 30).fill(password)
            time.sleep(1)
            playwright_helper.is_element_clickable(self.login_loc.SUBMIT_BTN).click()
            playwright_helper.is_element_clickable(self.home_loc.EXTRACTION_BTN_XPATH, 70)
            logging.info('Home Page Present')
        except:
            logging.info('User already logged in')
            
    def example_logout(self):
        """
        Logout from example application
        """
        try:
            playwright_helper.is_element_clickable(self.login_loc.PROFILE_ICON_CSS).click()
            time.sleep(1)
            playwright_helper.is_element_clickable(self.login_loc.LOGOUT_BTN_XPATH).click()
            time.sleep(2)
            logging.info('User Logged out Successfully')
        except:
            logging.info('User Already Logged out')
