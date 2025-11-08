import os
import pytest
import logging
import time
import zipfile
from PyPDF2 import PdfReader
from helper import playwright_helper
from datetime import datetime, date
from pages.home_page import exampleHomePage
from locators.home_page_locators import HomePageLocators
from locators.bank_statemenet_page_locators import BankStatementPageLocators


class BankStatementPage:

    def __init__(self, page):
        self.page = page
        self.bank_stmnt_loc = BankStatementPageLocators
        self.home_loc = HomePageLocators
        self.pg_home = exampleHomePage(pytest.page)

    '''
    Define All the common functionalities related to Bank Statement
    '''

    def select_bank_statement_extraction_option(self, option: str):
        """
        Select bank statement or credit card radio button
        
        Args:
            option: 'bank_statement' or 'credit_card'
        """
        time.sleep(1)
        match option.lower():

            case 'bank_statement':
                element = playwright_helper.is_element_present(self.bank_stmnt_loc.BANK_STATEMENT_RADIO_CSS)
                res = element.is_checked()
                logging.info(f'{option} radio button value is {res}')

                if res == True:
                    logging.info('Bank Statement Radio Button is already selected')
                else:
                    logging.error('Bank Statement Radio Button is not selected Automatically')
                    playwright_helper.is_element_clickable(self.bank_stmnt_loc.BANK_STATEMENT_RADIO_CSS, 20).click()
                    logging.info('Clicked on the Bank Statement button')
                    time.sleep(1)

            case 'credit_card':
                element = playwright_helper.is_element_present(self.bank_stmnt_loc.CREDIT_CARD_RADIO_CSS)
                res = element.is_checked()
                logging.info(f'{option} radio button value is {res}')

                if res == True:
                    logging.info('Credit Card Radio Button is already selected')
                else:
                    logging.error('Credit Card Radio Button is not selected Automatically')
                    playwright_helper.is_element_clickable(self.bank_stmnt_loc.CREDIT_CARD_RADIO_CSS, 20).click()
                    logging.info('Clicked on the Financial Statement button')
                    time.sleep(1)

            case _:
                logging.error('Invalid Option type found')

    def bank_statement_extraction_section_upload(self, option: str, filepath: str):
        """
        Upload file for bank statement extraction
        
        Args:
            option: 'bank_statement' or 'credit_card'
            filepath: Path to file to upload
            
        Returns:
            dict: File details including name, extension, number of pages
        """
        self.select_bank_statement_extraction_option(option)

        self.pg_home.upload_file(filepath)

        required_details = dict()

        self.pg_home.click_on_next_btn()
        fileName = filepath.split('\\')[-1]
        file_extn = fileName.split('.')[-1]

        if file_extn.lower() == 'pdf':
            page_length = self.pg_home.select_page()
            required_details['no_of_page'] = page_length

        elif file_extn.lower() in ['jpg', 'jpeg', 'png']:
            time.sleep(2)
            playwright_helper.is_element_clickable(self.home_loc.DISCLAIMER_OKAY_XPATH).click()
            required_details['no_of_page'] = 1

        required_details['file_name'] = fileName
        required_details['file_extn'] = file_extn

        return required_details
    
    def verify_history_sections(self):
        """
        Verify history section and return list of file names
        
        Returns:
            list: List of all file names in history
        
        Raises:
            Exception: If no files found in history
        """
        playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_HEADER_XPATH, 20)
        time.sleep(1)
        playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH, 20)
        time.sleep(2)
        all_fileNames_ele = playwright_helper.get_all_elements(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH)
        org_fileName_list = [element.get_attribute('data-testid') for element in all_fileNames_ele]
        logging.info(f'All the file names are {org_fileName_list} and Number of files are {len(org_fileName_list)}')
        
        if len(org_fileName_list) < 1:
            raise AssertionError(
                f"No files found in History tab.\n"
                f"Expected: At least 1 file\n"
                f"Found: {len(org_fileName_list)} files\n"
                f"Locator used: {self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH}\n"
                f"Tip: Make sure files have been uploaded before checking history."
            )
        
        logging.info(f'Successfully found {len(org_fileName_list)} file(s) in History Tab')
        return org_fileName_list
        
    def verify_back_btn_from_OP_screen(self):
        """Verify back button functionality from output screen"""
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.PREVIEW_ENABLED_1ST_BTN_XPATH, 80)
        # time.sleep(2)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.PREVIEW_ENABLED_1ST_BTN_XPATH).click()
        logging.info('Clicked on the Enabled Preview Button from output Screen')
        self.verify_bank_statement_extraction_output()
        assert playwright_helper.is_element_clickable(self.bank_stmnt_loc.OP_SCREEN_BACK_BTN_XPATH, 30)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.OP_SCREEN_BACK_BTN_XPATH).click()
        assert playwright_helper.is_element_present(self.home_loc.UPLOAD_FILE_XPATH, 100)
        logging.info('Back Button is working and redirected to Home Page')

    def verify_history_btn_from_OP_screen(self):
        """Verify history button functionality from output screen"""
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.PREVIEW_ENABLED_1ST_BTN_XPATH, 80)
        time.sleep(2)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.PREVIEW_ENABLED_1ST_BTN_XPATH).click()
        logging.info('Clicked on the Enabled Preview Button from output Screen')
        self.verify_bank_statement_extraction_output()
        assert playwright_helper.is_element_clickable(self.bank_stmnt_loc.OP_SCREEN_HISTORY_BTN_XPATH, 30)
        time.sleep(1)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.OP_SCREEN_HISTORY_BTN_XPATH).click()
        assert playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH, 100)
        no_of_files = playwright_helper.get_all_elements(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH)
        assert len(no_of_files) == 30
        logging.info('History Button is working and redirected to History Tab. 30 Files are showing under History Tab')
        
    def verify_search_bar_module_history_section(self, ip_file_name: str):
        """
        Verify search functionality in module history
        
        Args:
            ip_file_name: File name to search for
        """
        # time.sleep(2)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.MODULE_HISTORY_SEARCH_BAR_CSS, 20).fill(ip_file_name)
        # time.sleep(2)
        playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH, 10)
        ui_fileNames = playwright_helper.get_all_elements(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH)
        for temp in range(len(ui_fileNames)):
            ui_file_name = ui_fileNames[temp].get_attribute('data-testid')
            logging.info(f'After Searched File Name is showing in UI {ui_file_name}')
            if ip_file_name.strip().lower() == ui_file_name.strip().lower():
                logging.info('Correct File Name is showing')
            else:
                logging.error('Exact File Name are not showing in UI')

    def verify_uploaded_file_on_history_tab(self, testdata, filename: str):
        """
        Verify uploaded file appears in history tab with correct details
        
        Args:
            testdata: Test data dictionary
            filename: Name of uploaded file
            
        Returns:
            dict: File details from module history
        """
        time.sleep(6)
        playwright_helper.is_element_clickable(self.home_loc.LAST_TAB_NAME_XPATH, 15).click()
        time.sleep(1)
        logging.info('Clicked on the History Tab')
        playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_ALL_FILENAME_XPATH, 30)
        time.sleep(1)
        ui_1st_filename = playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_1ST_FILENAME_XPATH).get_attribute('data-testid')
        logging.info(f'First file name is showing in UI {ui_1st_filename} and coming file name to this function {filename}')
        
        while True:
            temp = 0
            if ui_1st_filename.strip().lower() != filename.lower():

                logging.warning('1st time uploaded file is not showing under History Tab')
                self.pg_home.click_on_tab(testdata['tab_name1'])
                self.pg_home.click_on_tab(testdata['tab_name2'])
                time.sleep(2)

                if ui_1st_filename.strip().lower() == filename.lower():
                    assert ui_1st_filename.strip().lower() == filename.lower()
                    logging.info('Uploaded File is showing under History Tab after refreshed')
                    break
                else:
                    temp += 1
                    if temp < 6:
                        continue
                    else:
                        logging.error('After refreshed 5 times, still uploaded files is not showing under History Tab')
                        break
            else:
                assert ui_1st_filename.strip().lower() == filename.lower()
                logging.info('1st time Uploaded File is showing under History Tab')
                break
        
        ui_1st_dateTime = playwright_helper.is_element_present(self.bank_stmnt_loc.MODULE_HISTORY_DATETIME_XPATH).text_content()
        logging.info(f'1st Row Date Time is showing {ui_1st_dateTime}')
        ui_date = ui_1st_dateTime.strip().split()[0]
        ui_time = ui_1st_dateTime.strip().split()[-1]
        logging.info(f'After Splitted Date & Time are {ui_date}, {ui_time}')
        date_obj = datetime.strptime(ui_date, "%m-%d-%Y").date()
        time_obj = datetime.strptime(ui_time, "%H:%M:%S").time()
        today_date = date.today()
        temp_date = today_date.strftime("%m-%d-%Y")
        today_formatted_date = datetime.strptime(temp_date, "%m-%d-%Y").date()

        assert date_obj == today_formatted_date
        logging.info('Uploaded File is showing under History Tab and Date is also matched')

        assert playwright_helper.is_element_present(self.bank_stmnt_loc.FILESTATUS_PROCESSING_XPATH, 10)
        logging.info('Uploaded File Verified and started Processing')

        file_details_from_module_history = {}
        file_details_from_module_history["filename"] = ui_1st_filename
        file_details_from_module_history['ui_dateTime'] = ui_1st_dateTime.strip()
        file_details_from_module_history['file_uploading_date_str'] = ui_date
        file_details_from_module_history['file_uploading_date_dateObj'] = date_obj
        file_details_from_module_history['file_uploading_time_str'] = ui_time
        file_details_from_module_history['file_uploading_time_timeObj'] = time_obj
        return file_details_from_module_history
    
    def submit_file_from_output(self):
        """Submit file from output screen"""
        playwright_helper.is_element_clickable(self.home_loc.SUBMIT_BTN_XPATH, 50)
        time.sleep(2)
        playwright_helper.is_element_clickable(self.home_loc.SUBMIT_BTN_XPATH, 15).click()
        time.sleep(1)
        playwright_helper.is_element_clickable(self.bank_stmnt_loc.PROCEED_BTN_XPATH).click()

    def verify_file_upload_message(self, msg: str):
        """
        Verify success message after file upload
        
        Args:
            msg: Expected success message
        """
        time.sleep(3)
        playwright_helper.is_element_clickable(self.home_loc.SUCCESS_MSG_XPATH, 60)
        success_msg = playwright_helper.is_element_clickable(self.home_loc.SUCCESS_MSG_XPATH).text_content()
        assert msg.strip() in success_msg
        logging.info(f'After uploaded file success message is {success_msg}')
        time.sleep(2)

    def verify_file_status_from_module_history(self, testdata, filename: str, date_time: str, no_of_page: int):
        """
        Verify file processing status and download output when complete
        
        Args:
            testdata: Test data dictionary
            filename: Name of the file
            date_time: DateTime string for file
            no_of_page: Number of pages in document
            
        Returns:
            str: Final file status
        """
        dynamic_locator_status = f'''(//div[@class='row-data'][.//div[@data-testid='{filename}'] and .//div[contains(text(), '{date_time}')]]//div[@aria-label='status'])'''
        dynamic_locator_download = f'''(//div[@class='row-data'][.//div[@data-testid='{filename}'] and .//div[contains(text(), '{date_time}')]]//div[@aria-label='download'])'''
        dynamic_locator_preview = f'''(//div[@class='row-data'][.//div[@data-testid='{filename}'] and .//div[contains(text(), '{date_time}')]]//div[@aria-label='preview'])'''

        logging.info(f'Dynamic Locator Status {dynamic_locator_status}')
        logging.info(f'Dynamic Locator Download {dynamic_locator_download}')
        logging.info(f'Dynamic Locator Preview {dynamic_locator_preview}')

        # Wait for elements to be present
        playwright_helper.is_element_present(dynamic_locator_status, 50)
        playwright_helper.is_element_present(dynamic_locator_download, 50)
        playwright_helper.is_element_present(dynamic_locator_preview, 50)

        total_wait_time = no_of_page * 55
        count_time = total_wait_time / 5
        temp = 0

        while True:

            if temp > 1:
                self.pg_home.click_on_tab(testdata['tab_name1'])
                self.pg_home.click_on_tab(testdata['tab_name2'])

            time.sleep(2)
            file_status = self.page.locator(dynamic_locator_status).get_attribute('data-testid')
            logging.info(f'File Status is {file_status}')
            download_status = self.page.locator(dynamic_locator_download).get_attribute('data-testid')
            logging.info(f'File Download Status is {download_status}')
            preview_status = self.page.locator(dynamic_locator_preview).get_attribute('data-testid')
            logging.info(f'File Preview Status is {preview_status}')

            match file_status.strip().lower():

                case 'failed':
                    logging.error('File Processing Failed')
                    break

                case 'processing':
                    time.sleep(5)
                    temp += 1
                    logging.info(f'Count Value Increased to {temp}')

                    if temp <= count_time:
                        continue
                    else:
                        logging.error(f'Waited for {total_wait_time} Seconds, File is not yet processed, So Loop Breaked')
                        break

                case 'partially-done':
                    logging.info('File Processing Completed, Initially Status is Disabled')
                    assert download_status.strip().lower() == 'download-disabled'
                    logging.info('File Processing Completed, Initially Download button Disabled')
                    assert preview_status.strip().lower() == 'preview-disabled'
                    logging.info('File Processing Completed, Initially Preview button Disabled')
                    break

                case 'completed':
                    logging.info('File Processing Completed, Status is now Enabled')
                    assert download_status.strip().lower() == 'download-enabled'
                    logging.info('File Processing Completed, Download button is now Enabled')
                    assert preview_status.strip().lower() == 'preview-enabled'
                    logging.info('File Processing Completed, Preview button is now Enabled')
                    
                    working_dir = os.getcwd()
                    download_folder = os.path.join(working_dir, 'download_output_file', testdata['section'])
                    
                    # Handle download using Playwright's download API
                    with self.page.expect_download() as download_info:
                        self.page.locator(dynamic_locator_download).click()
                    download = download_info.value
                    
                    # Get the suggested filename from the download
                    suggested_filename = download.suggested_filename
                    logging.info(f'Download initiated successfully, URL: {download.url}')
                    logging.info(f'Suggested filename: {suggested_filename}')
                    
                    # Save the file with the correct filename
                    final_download_path = os.path.join(download_folder, suggested_filename)
                    download.save_as(final_download_path)
                    logging.info(f'Output Downloaded Successfully to: {final_download_path}')
                    break
                    
                case 'in-queue':
                    logging.error('Invalid File Status Found or Files are in Queue')
                    start_time = time.time()
                    time.sleep(5)
                    temp += 1
                    logging.info(f'Count Value Increased to {temp}')

                    if temp > 6:
                        continue
                    else:
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        logging.error(f'Waited for {elapsed_time:.2f} Seconds, File is not yet processed, So Loop Breaked')
                        break

        return file_status

    def verify_bank_statement_extraction_output(self):
        """Verify bank statement extraction output is displayed"""
        try:
            ui_msg_element = playwright_helper.is_element_present(self.home_loc.ERROR_OUTPUT_CSS2, 30)
            if ui_msg_element:
                ui_msg = ui_msg_element.text_content()
                logging.error(f'UI message is {ui_msg}')
                if 'File processing unsuccessful. Please try again.' in ui_msg.strip():
                    logging.error('Error Occurred while doing extraction')
                    pytest.fail(
                        f"Bank Statement extraction failed.\n"
                        f"Error message from UI: {ui_msg.strip()}\n"
                        f"Possible reasons:\n"
                        f"  - Invalid or corrupted PDF file\n"
                        f"  - Unsupported file format\n"
                        f"  - Server processing error\n"
                        f"  - File size too large"
                    )

        except Exception:
            try:
                playwright_helper.is_element_present(self.home_loc.OUTPUT_FILE_XPATH, 60)
                logging.info(f'Left Side PDF Extraction Output Verified')

                playwright_helper.is_element_present(self.bank_stmnt_loc.OP_TABLE_HEADER_XPATH)
                logging.info('Right side Table Column Header is present')

                col_headers_list = [col_header.text_content() for col_header in playwright_helper.get_all_elements(self.bank_stmnt_loc.OP_TABLE_HEADER_XPATH)]
                logging.info(f'Total {len(col_headers_list)} Column Header are showing, those are: - {col_headers_list}')
                
                playwright_helper.is_element_present(self.bank_stmnt_loc.OP_TABLE_BODY_XPATH)
                logging.info(f'Right side PDF Extraction Output Verified')

            except Exception as e:
                current_url = pytest.page.url
                logging.error(f'PDF Extraction Output is not generated. Error: {str(e)}')
                pytest.fail(
                    f"Bank Statement extraction output not displayed.\n"
                    f"Current URL: {current_url}\n"
                    f"Expected elements:\n"
                    f"  - Left side: PDF viewer ({self.home_loc.OUTPUT_FILE_XPATH})\n"
                    f"  - Right side: Data table ({self.bank_stmnt_loc.OP_TABLE_HEADER_XPATH})\n"
                    f"Possible reasons:\n"
                    f"  - File processing is taking longer than expected (timeout: 60s)\n"
                    f"  - Extraction failed silently without error message\n"
                    f"  - Page elements changed or locators are outdated\n"
                    f"  - Network issues or server errors\n"
                    f"Technical error: {str(e)}"
                )

    def unzip_output_and_verify_excel(self, section, option, file_name):
        """
        Unzip downloaded output file and verify Excel file exists
        
        Args:
            section: Section name (e.g., 'bank_statement')
            option: Option name (e.g., 'bank_statement')
            file_name: Uploaded file name
            
        Returns:
            Tuple (success: bool, excel_files: list)
        """
        excel_extensions = ('.xlsx', '.xls', '.xlsm', '.xlsb')
        working_dir = os.getcwd()
        zip_file_path = os.path.join(working_dir, 'download_output_file', section, option)
        zip_file_name = os.listdir(zip_file_path)
        extract_to = os.path.join(working_dir, 'download_output_file', section, option, 'extracted_output', file_name.split('.')[0])

        os.makedirs(extract_to, exist_ok=True)

        with zipfile.ZipFile(os.path.join(zip_file_path, zip_file_name[0]), 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            
            excel_files = [file_obj for file_obj in zip_ref.namelist() 
                        if file_obj.lower().endswith(excel_extensions)]
            
            if excel_files:
                logging.info(f"Unzipped successful!!! Found Excel files: {excel_files}")
                return True, excel_files
            else:
                logging.error("No Excel files found after Unzipped")
                return False, []

    def go_to_support_portal(self):
        """Navigate to support portal by changing URL"""
        playwright_helper.wait_for_page_to_load('extraction', 60)
        current_url = self.page.url
        logging.info(f'Current URL is {current_url}')
        new_url = current_url.replace('extraction', 'history')
        logging.info(f'After replaced New URL is {new_url}')
        self.page.goto(new_url)
        time.sleep(1)

    def search_filename_in_support_portal(self, filename: str, date_time: str):
        """
        Search for uploaded file in support portal
        
        Args:
            filename: Name of the uploaded file
            date_time: DateTime when file was uploaded
        """
        playwright_helper.is_element_present(self.bank_stmnt_loc.PAGE_SIZE_XPATH, 40)
        time.sleep(1)
        playwright_helper.select_element_by_value(self.bank_stmnt_loc.PAGE_SIZE_XPATH, '100')
        time.sleep(2)
        
        search_bar = playwright_helper.is_element_clickable(self.bank_stmnt_loc.SP_SEARCH_BAR_CSS, 20)
        search_bar.fill(filename)
        time.sleep(2)
        
        dynamic_locator = f'''//tr[.//td[@data-testid='{filename}'] and .//td[@data-testid='{date_time}'] and .//td[@data-testid='completed']]'''
        logging.info(f'Dynamic Locator created for Support Portal {dynamic_locator}')

        try:
            self.page.locator(dynamic_locator).click()
            logging.info('Uploaded File Found in Support Portal, Clicked')

        except Exception:
            logging.error('File not Found in Support Portal')
