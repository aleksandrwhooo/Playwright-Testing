
import re
import datetime
import pandas as pd
import logging
import os
# import dot_env
from playwright.sync_api import expect, Playwright, sync_playwright
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from typing import Dict, Union
from datetime import datetime



ready_to_process="https://flooffy.mixlab.com/queue/confirm/readyToProcess"
real_time_ops = "https://insights.mixlab.com/dashboard/295"

authFile = ".auth/flooffy_state.json" 

flooffy_viewport = {"width": 900, "height": 1600}
# flooffy_viewport = {"width": 960, "height": 1800}
dullahan = False
dullahan = True #Headless toggle

logging.basicConfig(filename='app.log',
                    level=logging.INFO, #Thank you James
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def make_check_directory(folder: str = "Playwright Testing"):
    # folder: str = 'Queue Logs'
    directory = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Downloads') if os.name == 'nt' else 
                             os.path.join(  os.path.expanduser('~'), 'Downloads'), folder)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

##
def to_df(dict_data: Dict[str, str], ):
    dict_data['time_stamp'] = datetime.today().strftime('%Y-%m-%d %H:%M')
    df = pd.DataFrame([dict_data], columns=list(dict_data.keys()))
    return df



# to be integrated
def flooffy_to_df(html: str) -> pd.DataFrame:    
    soup = BeautifulSoup(html, 'html.parser')
    
    pattern = re.compile(r'.*?\d+')
    data_dict = {}


    for element in soup.find_all(class_='flex flex-col align-items-center'):
        matches = pattern.findall(element.text)
        for match in matches:
            cleaned_match = re.sub(r"(\D)(\d)", r"\1 \2",
                                    match.replace('PharmacyNY', '').replace('Lab', '')).strip()
            parts = cleaned_match.rsplit(' ', 1)
            if len(parts) == 2 and parts[1].isdigit():
                data_dict[parts[0]] = int(parts[1])
    print             
    return 
    

# to be integrated
def meta_to_df(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, 'html.parser')        
    # pattern = re.compile(r'.*?\d+')
    
    data_dict = {}
    dash_cards = soup.find_all(class_='DashCard')
    for card in dash_cards:
        title = card.find('h3', class_='Scalar-title')
        value = card.find('h1', class_='ScalarValue')

        if title is not None and value is not None:
            title = title.get_text(strip=True)
            value = value.get_text(strip=True)

            # Replace None values with 'no results'
            title = title if title is not None else 'no results'
            value = value if value is not None else 'no results'

            data_dict[title] = value
    return to_df(data_dict)

def get_creds(playwright: Playwright, dullahan: bool): 
    email = os.getenv('EMAIL')
    passwd = os.getenv('PASSWORD')

    browser = playwright.chromium.launch(headless=dullahan)
    context = browser.new_context()
    page = context.new_page()


    # Flooffy Credentials
    scan_bin = page.get_by_role("button", name="Scan bin")
    loading_icon = page.get_by_role("img", name="loading...")
    
    
    page.set_viewport_size(flooffy_viewport)
    page.goto(ready_to_process)
    page.get_by_label('Email').fill(email)
    page.press('body','Tab')
    page.get_by_label('Password').fill(passwd)
    page.get_by_role('button', name='Log in').click()

    expect(scan_bin).to_be_visible(timeout=29991)
    page.goto(ready_to_process)
    logging.info("Login successful - Scan bin visibile")
    
    expect(loading_icon).not_to_be_visible(timeout=60000) 
    try:
        page.screenshot(path=".screenshot/flooffy_creds.png", full_page=True)
    except Exception as e:
        print(e)


    #Meta Credentials
    real_time_reporting = page.get_by_role("heading", name="Real Time Ops Reporting")

    page.goto(real_time_ops)
    expect(page.locator("#formField-username"))

    page.get_by_placeholder("youlooknicetoday@email.com").fill(email)
    page.get_by_placeholder("Shhh...").fill(passwd)
    page.press('body','Enter')
  
    expect(real_time_reporting).to_be_visible()
    try:
        page.screenshot(path="meta_creds.png", full_page=True)
        logging.info("RTOps Screenshot saved")
    except Exception as e:
        logging.info(e)

    storage = page.context.storage_state(path=authFile)
    logging.info("Storage/Credentials State Saved")
    # print("Stroage state saved")


    context.close()
    browser.close()
    print("Browser closed")

    #Make local directory 
    try: 
        yield make_check_directory()
    except Exception as e:
        logging.info(e)





def flooffy_test(playwright: Playwright, dullahan: bool): 

    browser = playwright.chromium.launch(headless=dullahan)
    context = browser.new_context(storage_state=authFile)    
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    if dullahan == False: page.set_viewport_size(flooffy_viewport)


    page.goto(ready_to_process)
    expect(page.get_by_role("button", name="Scan bin")).to_be_visible(timeout=10000)
    expect(page.get_by_role("img", name="loading...")).not_to_be_visible(timeout=15000)
    # print("authFile Works")
    logging.info("Flooffy Authorization works")

    try:
        page.screenshot(path=".screenshots/flooffytest.png", timeout=12345)
        logging.info("Flooffy screenshot taken")
    except Exception as e:
        logging.info(e)
    
    context.tracing.stop(path = ".auth/trace2.zip")
    logging.info("Trace complete")

    html = page.content() # "Capture" #page.capture()
    directory = make_check_directory()
    print(directory)

    df = flooffy_to_df(html)
    print(df)

    site = "NY"
    prefix = "_flooffy"

    csv_filename = f"{site}{prefix}_{datetime.today().strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join(directory, csv_filename)

    print(csv_path)

    # if os.path.exists(csv_path):
    #     print("OS path exists")
    #     existing_df = pd.read_csv(csv_path)
    #     updated_df = pd.concat([existing_df, df], ignore_index=True)
    #     updated_df.to_csv(csv_path, index=False)
    # else:
    #     df.to_csv(csv_path)

    if not os.path.exists(csv_path):
        print("Flooffy csv DNE, making one")
        df.to_csv(csv_path)
    else:
        print("Flooffy csv exists")
        existing_df = pd.read_csv(csv_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)

    context.close()
    browser.close()
    logging.info("Flooffy test complete")





def meta_test(playwright: Playwright, dullahan: bool):

    browser = playwright.chromium.launch(headless=dullahan)
    context = browser.new_context(storage_state=authFile)
    page = context.new_page()
#   page.set_viewport_size(flooffy_viewport)   

    page.goto(real_time_ops)
    expect(page.locator(".LoadingSpinner").first).not_to_be_visible()

    try:
        page.screenshot(path=".screenshots/rts.png", timeout=12345)
        logging.info("Meta Credentials work")
    except Exception as e:
        logging.info(e)








if __name__ == "__main__":
    logging.info("Starting point")


    with sync_playwright() as pw:
        # get_creds(pw, dullahan=dullahan)
        flooffy_test(pw, dullahan=dullahan)
        meta_test(pw, dullahan=dullahan)






# '''
#             path = download_path()

#             directory = os.path.join(path, folder) if folder else path

#             if not os.path.exists(directory):
#                 os.mkdir(directory)

#             file = f'{prefix}{datetime.now().strftime("%m%d%y_%I%M")}.png'
#             file_path = os.path.join(directory, file) 