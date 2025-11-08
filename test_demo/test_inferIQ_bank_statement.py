import pytest
from utility import utils
from pages.login_page import exampleLoginPage
from pages.home_page import exampleHomePage
from pages.bank_statement_page import BankStatementPage

required_lst = list()
file_history = dict()


class TestBankStatement:

    @pytest.fixture
    def initialize_pages(self, scope='class'):

        self.pg_login = exampleLoginPage(pytest.page)
        self.pg_home = exampleHomePage(pytest.page)
        self.pg_bank_stmnt = BankStatementPage(pytest.page)
        

    def test_verify_bank_statement_side_bar_expanded(self, initialize_pages, testdata):
        
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Click on the side bar button and verify the navigation bar
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_side_bar()

    def test_verify_bank_statement_home_page_tablist(self, initialize_pages, testdata):
        
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Verify the two tabs should be shown, i.e. Upload File and History
        '''
        
        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])
        
        self.pg_home.verify_tablist(testdata['section'])
        
    def test_verify_bank_statement_home_page_default_tablist(self, initialize_pages, testdata):
        
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Verify the two tabs should be shown and Upload file tab should be selected by default
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_tablist(testdata['section'])

        self.pg_home.verify_default_tablist()

    def test_verify_bank_statement_home_page_history_tablist(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Verify the two tabs should be shown and Hitory tab should be shown right to Upload File Tab
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_tablist(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

    def test_verify_fileName_shown_under_bank_statement_history_tab(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Under History Tab all the file names should be shown which are uploaded yet(Currently last 30 files are showing)
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        lst_of_file_name = self.pg_bank_stmnt.verify_history_sections()
        required_lst.append(lst_of_file_name[0])

        self.pg_login.example_logout()

    def test_verify_BS_radio_button_selected(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Check by default bank statement Radio button should be selected
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_bank_stmnt.select_bank_statement_extraction_option(testdata['option'])

    def test_verify_bank_statement_search_optn_under_module_history_tab(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Under History Tab Search By File Name option should be present and working
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        if not required_lst:
            pytest.fail(
                "Cannot test search functionality: No file name available.\n"
                "Reason: Previous test 'test_verify_fileName_shown_under_bank_statement_history_tab' "
                "did not populate required_lst.\n"
                "This could happen if:\n"
                "  1. The previous test was skipped or failed\n"
                "  2. No files exist in history\n"
                "  3. Tests are not running in the correct order\n"
                "Tip: Run tests in order or upload a file first."
            )
        
        self.pg_bank_stmnt.verify_search_bar_module_history_section(required_lst[0])
        required_lst.clear()

        self.pg_login.example_logout()

    def test_verify_BS_back_button_functionality(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Under History Tab, Click over Preview button of a file for which Preview is enabled
        3. Output screen should be opened. Click over Back Button
        4. It should be redirected to Home Page
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        self.pg_bank_stmnt.verify_back_btn_from_OP_screen()

        self.pg_login.example_logout()

    def test_verify_BS_history_button_functionality(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Under History Tab, Click over Preview button of a file for which Preview is enabled
        3. Output screen should be opened. Click over the History Button
        4. It should be redirected to History Page and all the files should be shown
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        self.pg_bank_stmnt.verify_history_btn_from_OP_screen()

        self.pg_login.example_logout()

    def test_verify_disclaimer_popup_should_come_and_uploaded_file_should_show_under_BS_history_tab(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Bank Statement Radio option should be automatically selected, then Upload a File and Click on the Next Button
        3. Select Required pages and then Click on the Submit button
        4. Immediately Disclaimer popup should come with Okay button which is clickable
        5. Then Go to History tab and check the uploaded file should be shown in 1st row of the table and it should be processing
        6. Wait until it is completed, Initially that file status, Download, Preview buttons should be Disabled
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        data_dict = self.pg_bank_stmnt.bank_statement_extraction_section_upload(testdata['option'], utils.get_testdata_path(testdata['option'], testdata['file_extn']))

        self.pg_bank_stmnt.verify_file_upload_message(testdata['success_msg'])

        file_details = self.pg_bank_stmnt.verify_uploaded_file_on_history_tab(testdata, data_dict['file_name'])
        
        self.pg_bank_stmnt.verify_file_status_from_module_history(testdata, file_details['filename'], file_details['ui_dateTime'], data_dict['no_of_page'])

        file_history.update(file_details)
        file_history.update(data_dict)

        self.pg_login.example_logout()

    def test_verify_uploaded_file_should_show_under_support_portal(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Go to the Support portal, Search by using that file name
        3. Check that file name, Service Type, Time, Status which you uploaded based on file name and date-timing
        4. Click over the searched file, Output file should be opened
        5. History and Back button, both should be present
        6. Submit that file, it should be Submitted and the output screen should be closed
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_bank_stmnt.go_to_support_portal()

        self.pg_bank_stmnt.search_filename_in_support_portal(file_history['filename'], file_history['ui_dateTime'])

        self.pg_bank_stmnt.verify_bank_statement_extraction_output()

        self.pg_bank_stmnt.submit_file_from_output()

        self.pg_bank_stmnt.verify_file_upload_message(testdata['success_msg'])

        self.pg_login.example_logout()

    def test_verify_uploaded_file_should_enabled_from_module_history(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. The file which is uploaded by following above test case, Download, and Preview button should be enabled from module history
        3. Status should show Completed Successfully
        4. Click on the Preview Button, Output file should be opened, then close it. Download the output file
        5. Zip Output file should be downloaded, Unzip it and verify Output excel file should be present
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        self.pg_bank_stmnt.verify_file_status_from_module_history(testdata, file_history['filename'], file_history['ui_dateTime'], file_history['no_of_page'])

        utils.move_all_download_file_to_current_directory(testdata['section'], testdata['option'])

        self.pg_bank_stmnt.unzip_output_and_verify_excel(testdata['section'], testdata['option'], file_history['filename'])

        utils.remove_files(testdata['section'], testdata['option'])
        file_history.clear()

        self.pg_login.example_logout()


    def test_verify_disclaimer_popup_should_come_and_uploaded_image_should_show_under_history_tab(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Bank Statement Radio option should be automatically selected, then Upload a Image File and Click on the Next Button
        3. Immediately Disclaimer popup should come with Okay button which is clickable
        4. Then Go to History tab and check the uploaded file should be shown in 1st row of the table and it should be processing
        5. Wait until it is completed, Initially that file status, Download, Preview buttons should be Disabled
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        data_dict = self.pg_bank_stmnt.bank_statement_extraction_section_upload(testdata['option'], utils.get_testdata_path(testdata['option'], testdata['file_extn']))

        self.pg_bank_stmnt.verify_file_upload_message(testdata['success_msg'])

        file_details = self.pg_bank_stmnt.verify_uploaded_file_on_history_tab(testdata, data_dict['file_name'])

        self.pg_bank_stmnt.verify_file_status_from_module_history(testdata, file_details['filename'], file_details['ui_dateTime'], data_dict['no_of_page'])

        file_history.update(file_details)
        file_history.update(data_dict)

        self.pg_login.example_logout()

    
    def test_verify_uploaded_image_should_show_under_support_portal(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Go to the Support portal, Search by using that file name
        3. Check that file name, Service Type, Time, Status which you uploaded based on file name and date-timing
        4. Click over the searched file, Output file should be opened
        5. History and Back button, both should be present
        6. Submit that file, it should be Submitted and the output screen should be closed
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_bank_stmnt.go_to_support_portal()

        self.pg_bank_stmnt.search_filename_in_support_portal(file_history['filename'], file_history['ui_dateTime'])

        self.pg_bank_stmnt.verify_bank_statement_extraction_output()

        self.pg_bank_stmnt.submit_file_from_output()

        self.pg_bank_stmnt.verify_file_upload_message(testdata['success_msg'])

        self.pg_login.example_logout()

    
    def test_verify_uploaded_image_should_enabled_from_module_history(self, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. The file which is uploaded by following above test case, Download, and Preview button should be enabled from module history
        3. Status should show Completed Successfully
        4. Click on the Preview Button, Output file should be opened, then close it. Download the output file
        5. Zip Output file should be downloaded, Unzip it and verify Output excel file should be present
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])
        
        self.pg_home.select_section(testdata['section'])

        self.pg_home.verify_home_page_history_tab()

        self.pg_bank_stmnt.verify_file_status_from_module_history(testdata, file_history['filename'], file_history['ui_dateTime'], file_history['no_of_page'])

        utils.move_all_download_file_to_current_directory(testdata['section'], testdata['option'])

        self.pg_bank_stmnt.unzip_output_and_verify_excel(testdata['section'], testdata['option'], file_history['filename'])

        utils.remove_files(testdata['section'], testdata['option'])

        self.pg_login.example_logout()

    @pytest.mark.parametrize("file_path", utils.get_list_of_testdata_path('bank_statement'))
    def _test_verify_bank_statement_extraction_output(self, file_path, initialize_pages, testdata):
        '''
        Steps: - 
        1. Login into the Application and Navigate to Bank Statement section
        2. Take all those files from respective folder, upload it one after another and wait until it is completed
        3. Go to History Section, and check Output should be able to open for all the files
        '''

        self.pg_login.example_login(
            pytest.config['dev_url'], pytest.config['dev_login']['email'], pytest.config['dev_login']['password'])

        self.pg_home.select_section(testdata['section'])

        data_dict = self.pg_bank_stmnt.bank_statement_extraction_section_upload(
            testdata['option'], file_path)
        
        self.pg_bank_stmnt.verify_file_upload_message(testdata['1st_success_msg'])

        file_details = self.pg_bank_stmnt.verify_uploaded_file_on_history_tab(testdata, data_dict['file_name'])

        status = self.pg_bank_stmnt.verify_file_status_from_module_history(testdata, file_details['filename'], file_details['ui_dateTime'], data_dict['no_of_page'])

        if status.strip().lower() == 'failed':

            pytest.fail('Extraction Failed')

        file_history.update(file_details)
        file_history.update(data_dict)