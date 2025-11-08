import os
import time
import shutil
import random
import inspect
import logging
import random
import string
from pathlib import Path
from datetime import datetime, timezone


def get_testdata_path(option: str, file_extn = ''):
    cur_dir = os.getcwd()
    caller_func_name = inspect.stack()[1][3]
    
    if 'classification' not in caller_func_name:
        
        file_path = os.path.join(cur_dir, 'testdata', option)
        cur_file = os.listdir(file_path)

        if len(file_extn) > 1:
            specific_files = [file for file in cur_file if file.lower().endswith('.'+file_extn)]
            temp_fileName = random.choice(specific_files)
            return os.path.join(file_path, temp_fileName)
        
        else:

            temp_fileName = random.choice(os.listdir(file_path))
            # temp_fileName = '4_BankForm_ACH.pdf'
            return os.path.join(file_path, temp_fileName)

    else:
        
        file_path = os.path.join(cur_dir, 'testdata', 'classification', option)
        cur_file = random.choice(os.listdir(file_path))
        # cur_file = '60_new.pdf'
        full_filePath = os.path.join(file_path, cur_file)
        logging.warning(f'The file Path to be found {full_filePath} !!!')
        return full_filePath

def get_list_of_testdata_path(option: str, document_type = ''):
    
    cur_dir = os.getcwd()

    if len(document_type) == 0:

        file_path = os.path.join(cur_dir, 'testdata', option)
        list_of_files = os.listdir(file_path)
        lst_of_full_filePath = [os.path.join(file_path, rel_file_path) for rel_file_path in list_of_files]
        return lst_of_full_filePath
            
    else:

        file_path = os.path.join(cur_dir, 'testdata', 'classification', document_type.lower())
        logging.info(f'The File Path including document type is {file_path}')
        list_of_files = os.listdir(file_path)
        lst_of_full_filePath = [os.path.join(file_path, rel_file_path) for rel_file_path in list_of_files]
        logging.info(f'List Of Full File Path is {lst_of_full_filePath}')
        return lst_of_full_filePath
        
def remove_files(section: str, option: str):
        
    working_dir = os.getcwd()
    rm_file_dir = os.path.join(working_dir, 'download_output_file', section, option)

    for item in os.listdir(rm_file_dir):
        item_path = os.path.join(rm_file_dir, item)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                logging.info('File removed successfully')
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                logging.info('Folder removed successfully')
        except:
            logging.error(f"Error deleting {item_path}", exc_info=True)
    
    # if len(document_type) == 0:
        
    #     rm_file_dir = os.path.join(working_dir, 'download_output_file', section, option)
    #     all_files_name = os.listdir(rm_file_dir)
    
    #     for file_name in all_files_name:
            
    #         try:
    #             os.remove(os.path.join(rm_file_dir, file_name))
    #             logging.info(f'{file_name} removed successfully')
                
    #         except:
    #             logging.error(f'Unable to remove {file_name}', exc_info=True)
                
    # elif len(document_type) >= 1:
        
    #     new_rm_file_dir = os.path.join(working_dir, 'download_output_file', section, option, 'extracted_output', document_type)
    #     new_all_files_name = os.listdir(new_rm_file_dir)
        
    #     for file_name in new_all_files_name:
            
    #         try:
    #             os.remove(os.path.join(new_rm_file_dir, file_name))
    #             logging.info(f'{file_name} removed successfully')
                
    #         except:
    #             logging.error(f'Unable to remove {file_name}', exc_info=True)
                
def move_all_download_file_to_current_directory(section: str, option: str, document_type = ''):
    
    downloads_dir = str(Path.home() / "Downloads")
    working_dir = os.getcwd()
    dst_file_name = os.path.join(working_dir, 'download_output_file', section, option)
    new_dst_file_name = os.path.join(working_dir, 'download_output_file', section, option, document_type)
    current_time = time.time()
    time_window = 80
    recent_files = []
    all_files_names_list = os.listdir(downloads_dir)
    data_dict = dict()

    for file_name in all_files_names_list:
        temp_file_path = os.path.join(downloads_dir, file_name)
        
        if os.path.isfile(temp_file_path):
            modification_time = os.path.getmtime(temp_file_path)
            
            if current_time - modification_time <= time_window:
                current_utc_time = datetime.now(timezone.utc).strftime('%H%M%S%f')
                temp_list = file_name.split('.')
                temp_file_name = temp_list[0]+current_utc_time
                new_file_name = temp_file_name +'.'+ temp_list[-1]
                new_full_filePath = os.path.join(downloads_dir, new_file_name)
                os.rename(temp_file_path, new_full_filePath)
                recent_files.append(new_full_filePath)
                logging.info('Recent Downloaded file detected')
    
    if len(recent_files) >= 1:
        
        if len(document_type) == 0:
            
            for file_path in recent_files:
                shutil.move(file_path, dst_file_name)
                logging.info('File Moved Successfully')
                
        elif len(document_type) >= 1:
            
            for file_path in recent_files:
                shutil.move(file_path, new_dst_file_name)
                logging.info('Classification Section File Moved Successfully')
    else:
        
        logging.error('No Recent Downloaded file is added')

    data_dict['rename_filename'] = new_file_name
    data_dict['rename_fullpath'] = new_full_filePath
    return data_dict

def generate_random_bank_name():

    REAL_BANK_NAMES = [
    "Wells Fargo Bank", "JPMorgan Chase Bank", "Bank of America", "Citibank",
    "U.S. Bank", "PNC Bank", "Capital One Bank", "TD Bank", "Bank of the West",
    "Fifth Third Bank", "KeyBank", "Regions Bank", "SunTrust Bank", "BB&T Bank",
    "Huntington Bank", "M&T Bank", "Comerica Bank", "Zions Bank", "First National Bank",
    "Community First Bank", "First Citizens Bank", "United Community Bank",
    "First Republic Bank", "Silicon Valley Bank", "City National Bank",
    "East West Bank", "First Interstate Bank", "Frost Bank", "Hancock Whitney Bank",
    "Pinnacle Bank", "First Horizon Bank", "Synovus Bank", "Umpqua Bank",
    "Banner Bank", "Pacific Premier Bank", "Western Alliance Bank", "Prosperity Bank",
    "Texas Capital Bank", "First Financial Bank", "Old National Bank",
    "First Merchants Bank", "German American Bank", "Park National Bank",
    "First Commonwealth Bank", "S&T Bank", "Premier Bank", "Heartland Bank",
    "Community Bank", "Farmers Bank", "Security Bank", "Liberty Bank",
    "Heritage Bank", "Cornerstone Bank", "Pinnacle Financial", "Metro Bank"
]
    
    return random.choice(REAL_BANK_NAMES)

def generate_random_address():

    STREETS = ["Main St", "Oak Ave", "Pine Rd", "Maple Dr", "Cedar Ln", "Elm St", "Washington Ave", "Park Rd", "First St", "Second Ave", "Lincoln Dr", "Madison St", "Jefferson Ave", "Adams Rd", "Jackson St", "Franklin Ave", "Church St", "Spring Rd", "Mill Ln", "River Dr"]

    CITIES = ["Springfield", "Franklin", "Georgetown", "Clinton", "Madison", "Salem", "Fairview", "Riverside", "Oak Grove", "Maple Grove"]

    STATES = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"]

    return f"{random.randint(1, 9999)} {random.choice(STREETS)}, {random.choice(CITIES)}, {random.choice(STATES)} {random.randint(10000, 99999)}"

def generate_random_acc_number():

    return random.randint(10**11, 10**12 - 1)

def generate_random_acc_type():

    account_types = [
        "Checking",
        "Savings",
        "Money Market",
        "Certificate of Deposit (CD)",
        "Individual Retirement Account (IRA)",
        "Business Checking",
        "Business Savings",
        "Business Money Market",
        "Student Checking",
        "High-Yield Savings",
        "Joint Checking",
        "Joint Savings",
        "Traditional IRA",
        "Roth IRA",
        "Money Market CD",
        "Custodial",
        "Health Savings",
        "Senior Checking"
    ]
    
    return random.choice(account_types)

def generate_random_person_name():

    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Nancy", "Daniel", "Lisa", "Sophia",
        "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna", "Abigail",
        "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle", "Ashley",
        "Kenneth", "Laura", "Kevin", "Sarah", "Brian", "Kimberly", "George", "Deborah", "Samantha",
        "Edward", "Dorothy", "Ronald", "Lisa", "Timothy", "Nancy", "Jason", "Karen"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Morris",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Murphy",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
        "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Stewart",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker"
    ]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    return f"{first_name} {last_name}"

def generate_random_string(length):

    first_letter = random.choice(string.ascii_uppercase)
    remaining_letters = ''.join(random.choices(string.ascii_lowercase, k=length - 1))
    return first_letter + remaining_letters

def generate_portfolio_name():

    current_utc_time = datetime.now(timezone.utc).strftime('%y%m%d%H%M%S%f')
    portfolio_name = f"Automation_Portfolio_{current_utc_time}"
    return portfolio_name