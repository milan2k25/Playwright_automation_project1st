class LoginPageLocators:

    SIGN_IN_XPATH = "//button[text()='Sign In']"
    IP_EMAIL_XPATH = "//input[@type='email']"
    IP_EMAIL_ID = "email"
    IP_EMAIL_NAME = "email id"
    IP_PASSWORD_XPATH = "//input[@name='password']"
    TERMS_AND_CONDITIONS_CHECKBOX_XPATH = "(//div//input[@type='checkbox'])[last()]"
    SUBMIT_BTN = "//button[@type='submit']"
    PROFILE_ICON_CSS = "[id='dropdown-basic']"
    LOGOUT_BTN_XPATH = "//span[text()='Logout']"
    

# def __init__(self, driver):
#     self.driver = driver