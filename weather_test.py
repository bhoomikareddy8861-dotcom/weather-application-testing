
import re
from playwright.sync_api import sync_playwright

city = "Bengaluru"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # Step 1: Open DuckDuckGo
    page.goto("https://duckduckgo.com")
    page.wait_for_timeout(3000)

    # Step 2: Search weather automatically
    search_box = page.get_by_role("combobox").first
    search_box.wait_for(state="visible", timeout=30000)
    search_box.fill("weather in " + city)
    search_box.press("Enter")

    # Step 3: Wait for results
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(5000)

    # Step 4: Read page content
    content = page.locator("body").inner_text()

    # Step 5: Validate search result
    assert city.lower() in content.lower(), "City not found!"

    print("City search: PASSED")

    # Step 6: Extract temperature
    temperature = re.search(r"-?\d+\s*°\s*[CF]", content)

    if temperature:
        print("Temperature:", temperature.group())
        print("Temperature test: PASSED")
    else:
        print("Temperature not found")
        print("Temperature test: FAILED")

    browser.close()
