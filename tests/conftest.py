
import os
import json
import pytest
from playwright.sync_api import sync_playwright, Playwright


# @pytest.fixture(scope="session")
# def user_1_storage_state(playwright: Playwright,
#                          base_url,
#                          user_1_username,
#                          user_1_password) -> None:
#     browser = playwright.chromium.launch(headless=False)

@pytest.fixture(scope="session")
def flooffy2(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # page.goto(base_url)
    # logon_page = LogonPage(page)
    # nav = Nav(page)
    # logon_page.password_logon(user_1_username, user_1_password)
    # nav.home_btn.wait_for()
    context.storage_state(path=".auth/flooffy_state.json")
    page.close()
    browser.close()

@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": ".auth/flooffy_state.json",
    }


@pytest.fixture(scope="function")
def creds_ready():
    # Get the path to the context configuration JSON file
    # config_path = os.path.join(".auth", "context_config.json")
    
    # # Load the context configuration from the JSON file
    # with open(config_path, "r") as file:
    #     context_config = json.load(file)
    
    # Create a Playwright context based on the loaded configuration
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # context = browser.new_context(**contextf_config)  # Pass the configuration as keyword arguments
        context = browser.new_context(storage_state=".auth/flooffy_state.json")  # Pass the configuration as keyword arguments

        yield context
        context.close()
        browser.close()