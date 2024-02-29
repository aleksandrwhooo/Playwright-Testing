import re
from playwright.sync_api import Page, expect, sync_playwright, Playwright


# ReadyToProcess = "https://flooffy.mixlab.com/queue/confirm/readyToProcess"



def test_flooffy_login(page: Page):
    # page.goto("https://flooffy.mixlab.com/login")
    page.goto("https://flooffy.mixlab.com/queue/confirm/readyToProcess")
    page.get_by_label('Email').fill('aleks-test@mixlabrx.com')
    page.press('body','Tab')
    page.get_by_label('Password').fill('VkN56bCaYv4b$p28&rr#EM')
    page.get_by_role('button', name='Log in').click()
    expect(page.get_by_role("button", name="Scan bin")).to_be_visible
    # storage = new_context.storage_state(path="state.json")




def test_check_flooffy_login(page: Page):
    page.context.storage_state(path="state.json")
    # context = browser.new_context(storage_state="state.json")
    page.goto("https://flooffy.mixlab.com/queue/confirm/readyToProcess")
    expect(page.get_by_role("button", name="Scan bin")).to_be_visible




""" def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible() """