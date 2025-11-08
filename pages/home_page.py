import os
import time
import logging
from helper import playwright_helper
from locators.home_page_locators import HomePageLocators


class InferIQHomePage:
    
    def __init__(self, page):
        self.page = page
        self.home_loc = HomePageLocators
    
    '''
    Define All the common functionalities related to Home Page
    '''
    
    def select_section(self, section: str):
        """
        Navigate to specific section from home page
        
        Args:
            section: Name of the section to navigate to
        """
        logging.warning(f'The current section to be found {section}')
        time.sleep(1)
        
        match section.lower():
            
            case 'extraction':
                playwright_helper.is_element_clickable(self.home_loc.EXTRACTION_BTN_XPATH, 20).click()
                logging.info('Extraction Section Selected')
                
            case 'bank_statement':
                playwright_helper.is_element_clickable(self.home_loc.BANK_STMNT_XPATH, 20).click()
                logging.info('Bank Statement Section Selected')

            case 'cash_flow_analysis':
                playwright_helper.is_element_clickable(self.home_loc.CASH_FLOW_XPATH, 60).click()
                logging.info('Cash Flow Analysis Section Selected')
            
            case 'conversational_ai':
                playwright_helper.is_element_clickable(self.home_loc.CON_AI_BTN_XPATH, 10).click()
                logging.info('Conversational AI Section Selected')
                
            case 'rent_roll':
                playwright_helper.is_element_clickable(self.home_loc.RENT_ROLL_BTN_XPATH, 10).click()
                logging.info('Rent Roll Section Selected')
                
            case 'predictive_analytics':
                playwright_helper.is_element_clickable(self.home_loc.PA_BTN_XPATH, 10).click()
                logging.info('Predictive Analytics Section Selected')
                
            case 'redaction':
                playwright_helper.is_element_clickable(self.home_loc.REDACTION_BTN_XPATH, 10).click()
                logging.info('Redaction Section Selected')
                
            case 'recognition':
                playwright_helper.is_element_clickable(self.home_loc.RECOGNITION_BTN_XPATH, 10).click()
                logging.info('Recognition Section Selected')
                
            case 'classification':
                playwright_helper.scroll_to_element(self.home_loc.CLASSIFICATION_BTN_XPATH)
                time.sleep(1)
                playwright_helper.is_element_clickable(self.home_loc.CLASSIFICATION_BTN_XPATH).click()
                logging.info('Classification Section Selected')
                
            case _:
                logging.error('No Section has been selected from Home Page')
            
    def verify_side_bar(self):
        """
        Verify sidebar expand/collapse functionality
        """
        attr_value = playwright_helper.is_element_clickable(self.home_loc.SIDE_BAR_BTN_CSS, 10).get_attribute('data-icon')
        logging.info(f'Side Bar attribute value is {attr_value}')
        
        match attr_value:
            case 'angle-left':
                logging.info('Initially Side Bar is expanded')
            case 'angle-right':
                logging.info('Initially Side Bar is Collapsed')
            case _:
                logging.error('Side Bar not present')
            
        playwright_helper.is_element_clickable(self.home_loc.SIDE_BAR_BTN_CSS, 10).click()
        time.sleep(2)
        attr_value2 = playwright_helper.is_element_clickable(self.home_loc.SIDE_BAR_BTN_CSS).get_attribute('data-icon')
        logging.info(f'After clicked, side bar value is {attr_value2}')
        
        if attr_value2 == 'angle-right':
            logging.info('Now Side Bar is Collapsed')
        else:
            logging.error('Exception Occurred on Side Bar')
            
    def upload_file(self, filepath: str):
        """
        Upload file using file input element
        
        Args:
            filepath: Absolute path to the file to upload
        
        Returns:
            filepath: The uploaded file path
        """
        time.sleep(1)
        # Playwright handles file uploads using set_input_files
        self.page.locator(self.home_loc.UPLOAD_FILE_XPATH).set_input_files(filepath)
        time.sleep(2)
        
        logging.info(f'{filepath} file uploaded successfully')
        
        return filepath
            
    def click_on_next_btn(self):
        """Click on Next button"""
        playwright_helper.scroll_to_element(self.home_loc.NEXT_BTN_XPATH)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.home_loc.NEXT_BTN_XPATH).click()
        logging.info('Clicked on the Next Button')

    def click_on_submit_btn(self):
        """Click on Submit button"""
        playwright_helper.scroll_to_element(self.home_loc.SUBMIT_BTN_XPATH)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.home_loc.SUBMIT_BTN_XPATH).click()
        logging.info('Clicked on the Submit Button')
        
    def verify_error_msg_without_choosing_necessary_optn(self, error_msg: str):
        """
        Verify error message when necessary option is not chosen
        
        Args:
            error_msg: Expected error message
        """
        UI_error_msg = playwright_helper.is_element_clickable(self.home_loc.ERROR_MSG_XPATH, 10).text_content()
        logging.info(f'UI error message is coming: {UI_error_msg}')
        
        assert UI_error_msg.strip() == error_msg, 'Error message is not showing without selecting necessary fields'
        logging.info('Error Message validated')

    def select_page(self):
        """
        Select pages from PDF preview
        
        Returns:
            int: Number of pages selected
        """
        time.sleep(4)
        all_pages = playwright_helper.get_all_elements(self.home_loc.SELECT_PAGE_XPATH)
        length = len(all_pages)
        logging.info(f'Total number of pages to be selected {length}')
        
        for index in range(1, length+1):
            dynamic_locator = f'''(//button[@class='select_pdf_page_container']//canvas[contains(@class,'canvas')])[{index}]'''
            logging.info(f'Clicked over dynamic locator {dynamic_locator}')
            self.page.locator(dynamic_locator).click()
            time.sleep(1)
            if index >= 4:
                logging.warning(f'Number of pages selected {index}, so loop breaked')
                break
        
        playwright_helper.scroll_to_element(self.home_loc.SUBMIT_BTN_XPATH)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.home_loc.SUBMIT_BTN_XPATH).click()
        time.sleep(2)
        playwright_helper.is_element_clickable(self.home_loc.DISCLAIMER_OKAY_XPATH).click()
        return length

    def get_last_API_response(self, file_name=''):
        """
        Get last API response (Playwright network interception)
        
        Args:
            file_name: Optional filename for screenshot
        """
        if len(file_name) > 1:
            self.page.screenshot(path=os.path.join(os.getcwd(), "report", f"{__name__}____{file_name}.png"))
        
        # Note: Playwright network interception requires setup in conftest.py
        logging.info('API response capture requires network listener setup')
    
    def check_tab_attribute_value(self, tab_name: str):
        """
        Check tab attribute values for validation
        
        Args:
            tab_name: Name of the tab to check
        """
        match tab_name.lower():

            case 'upload_file':
                attr_value = playwright_helper.is_element_clickable(self.home_loc.UPLOAD_FILE_TAB_CSS).get_attribute('aria-selected')
                attr_value2 = playwright_helper.is_element_clickable(self.home_loc.UPLOAD_FILE_TAB_CSS).get_attribute('class')
                logging.info(f'Upload File Tablist values are {attr_value, attr_value2}')

                if 'true' != attr_value.strip() or 'nav-link active' != attr_value2.strip():
                    raise AssertionError(
                        f"Upload File tab is not selected.\n"
                        f"Expected: aria-selected='true' and class='nav-link active'\n"
                        f"Found: aria-selected='{attr_value.strip()}' and class='{attr_value2.strip()}'\n"
                        f"Tab selector: {self.home_loc.UPLOAD_FILE_TAB_CSS}"
                    )

            case 'history':
                attr_value = playwright_helper.is_element_clickable(self.home_loc.HISTORY_TAB_CSS).get_attribute('aria-selected')
                attr_value2 = playwright_helper.is_element_clickable(self.home_loc.HISTORY_TAB_CSS).get_attribute('class')
                logging.info(f'History Tablist values are {attr_value, attr_value2}')

                if 'true' != attr_value.strip() or 'nav-link active' != attr_value2.strip():
                    raise AssertionError(
                        f"History tab is not selected.\n"
                        f"Expected: aria-selected='true' and class='nav-link active'\n"
                        f"Found: aria-selected='{attr_value.strip()}' and class='{attr_value2.strip()}'\n"
                        f"Tab selector: {self.home_loc.HISTORY_TAB_CSS}"
                    )

    def verify_tablist(self, section_name: str):
        """
        Verify tab list presence
        
        Args:
            section_name: Name of the section to verify tabs for
        """
        time.sleep(3)
        # Don't use is_element_clickable for locators that match multiple elements
        # Just get all elements directly
        all_tabs = playwright_helper.get_all_elements(self.home_loc.OUTPUT_TABLIST_NAME_XPATH)
        
        if not all_tabs:
            raise Exception(
                f"No tabs found in {section_name.replace('_', ' ')} section.\n"
                f"Locator: {self.home_loc.OUTPUT_TABLIST_NAME_XPATH}\n"
                f"Expected to find 'Upload File' and 'History' tabs."
            )

        all_tabs_name = [element.text_content().lower() for element in all_tabs]
        logging.info(f'All Tab Names are: {all_tabs_name}')

        if 'history' not in all_tabs_name or 'upload file' not in all_tabs_name:
            raise AssertionError(
                f"Expected tabs not found in {section_name.replace('_', ' ')} home page.\n"
                f"Expected: ['upload file', 'history']\n"
                f"Found: {all_tabs_name}"
            )
        
        logging.info(f'''Both the Tabs are present in {section_name.replace('_', ' ')} home page''')

    def verify_default_tablist(self):
        """Verify default tab selection"""
        time.sleep(3)
        all_tabs = playwright_helper.get_all_elements(self.home_loc.OUTPUT_TABLIST_NAME_XPATH)
        
        if not all_tabs:
            raise Exception(
                f"No tabs found on the page.\n"
                f"Locator: {self.home_loc.OUTPUT_TABLIST_NAME_XPATH}\n"
                f"Expected to find at least 'Upload File' tab as default."
            )
        
        all_tabs_name = [element.text_content().strip().lower() for element in all_tabs]

        if len(all_tabs_name) == 0:
            raise Exception("No tab names could be extracted from the page.")
        
        if 'upload file' != all_tabs_name[0]:
            raise AssertionError(
                f"Default tab mismatch.\n"
                f"Expected first tab: 'upload file'\n"
                f"Found first tab: '{all_tabs_name[0]}'\n"
                f"All tabs: {all_tabs_name}"
            )
        
        logging.info(f'1st Tab is: {all_tabs_name[0]}')

        self.check_tab_attribute_value('Upload_file')
        logging.info('Upload file Tab is initially selected')

    def verify_home_page_history_tab(self):
        """Verify and click history tab"""
        playwright_helper.is_element_clickable(self.home_loc.LAST_TAB_NAME_XPATH, 15)
        playwright_helper.scroll_to_element(self.home_loc.LAST_TAB_NAME_XPATH)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.home_loc.LAST_TAB_NAME_XPATH).click()
        time.sleep(2)
        logging.info('Clicked on the Last Tab')
        tab_name = playwright_helper.is_element_clickable(self.home_loc.LAST_TAB_NAME_XPATH, 30).text_content()
        logging.info(f'Current Tab name is {tab_name}')

        assert 'history' == tab_name.strip().lower()
        logging.info('History Tab Verified')

        self.check_tab_attribute_value('History')
        logging.info('History Tab Selected')

    def click_on_tab(self, tab_name: str):
        """
        Click on specific tab
        
        Args:
            tab_name: Name of the tab to click
        """
        match tab_name.lower():

            case 'upload_file':
                playwright_helper.is_element_clickable(self.home_loc.UPLOAD_FILE_TAB_CSS).click()
                time.sleep(2)
                self.check_tab_attribute_value(tab_name)

            case 'history':
                playwright_helper.is_element_clickable(self.home_loc.HISTORY_TAB_CSS).click()
                time.sleep(2)
                self.check_tab_attribute_value(tab_name)
