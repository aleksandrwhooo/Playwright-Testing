
from playwright.sync_api import Page, expect, sync_playwright, Playwright


ready_to_process="https://flooffy.mixlab.com/queue/confirm/readyToProcess"
real_time_ops = ""
flooffy_viewport = {"width": 960, "height": 1800}
authFile = ".auth/flooffy_state.json" 




def test_credentials(page: Page , flooffy2):
    # page.context = page.browser.new_context(authFile)
    # context = page.context.add_cookies(authFile)
    # page.add_coo
    # page = Page
    page = flooffy2.new_page()
    page.goto(ready_to_process)
    # expect(page.get_by_role("button", name="Scan bin")).to_be_visible(timeout=10000)
    # ecpect(page.)

    print("authFile Works")
    try:
        page.screenshot(path="awww.png", timeout=12345)
    except Exception as e:
        print(e)
    # page.screenshot(path="afw.png")
    # context.close()

    # browser.close()
    print("Test Complete")