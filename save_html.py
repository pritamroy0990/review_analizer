import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
from pathlib import Path

# url='''https://www.google.com/maps/place/Rooftop+Restaurant/@25.7513596,89.2603454,15.49z/data=!4m18!1m9!3m8!1s0x39e32dbb546f649f:0x54ecd2c10a496647!2sJSK+Rooftop+Restaurant!8m2!3d25.7482134!4d89.25655!9m1!1b1!16s%2Fg%2F11ltcx6_8g!3m7!1s0x39e32db990340751:0xaa6f2de2d36fc946!8m2!3d25.7421728!4d89.2644856!9m1!1b1!16s%2Fg%2F11khf4kg30?entry=ttu&g_ep=EgoyMDI1MDkyMS4wIKXMDSoASAFQAw%3D%3D'''

# url='''https://www.google.com/maps/place/Keranipara+Chowrasta+Mor/@25.7493814,89.2302849,15.89z/data=!4m18!1m9!3m8!1s0x39e333006e8d331f:0xe4c87b4b213cc6f2!2sPancake's+Rangpur!8m2!3d25.7491644!4d89.2333836!9m1!1b1!16s%2Fg%2F11w4p8dmy8!3m7!1s0x39e333ce6a049637:0xc820bc22c5b9cac7!8m2!3d25.7504704!4d89.2343289!9m1!1b1!16s%2Fg%2F11rcfvr4lv?hl=en&entry=ttu&g_ep=EgoyMDI1MDkxMC4wIKXMDSoASAFQAw%3D%3D'''


def run(playwright: Playwright,url) -> None:
    out = Path("page.html")
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.on("response", lambda response:print(response.url))
    page.goto(url)

    page.get_by_role("button", name="Sort reviews").click()
    page.get_by_role("menuitemradio", name="Newest").click()

    last_response_time = time.time()

    def on_response(response):
        nonlocal last_response_time
        last_response_time = time.time()
        print("📡 Response:", response.url)

    page.on("response", on_response)

    # Keep scrolling until no new responses for N seconds
    while True:
        page.keyboard.press("End")
        page.wait_for_timeout(2000)
        page.evaluate('''document.querySelectorAll('button.w8nwRe.kyuRq').forEach(btn => btn.click());''')

        if time.time() - last_response_time > 10:  # 5 seconds idle
            print("✅ Finished scrolling")
            break
    page.evaluate('''document.querySelectorAll('button.w8nwRe.kyuRq').forEach(btn => btn.click());''')

    html = page.content()  # full HTML of the page (string)
    out.write_text(html, encoding="utf-8")
    print(f"Saved HTML to {out}")

    # time.sleep(1000)

    # ---------------------
    context.close()
    browser.close()


def save_html_file(url):
    with sync_playwright() as playwright:
        run(playwright,url)
