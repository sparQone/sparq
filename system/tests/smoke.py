# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Smoke test for the application.
#
# Copyright (c) 2025 remarQable LLC

from playwright.sync_api import sync_playwright
def test_smoke():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode for speed
        page = browser.new_page()

        page.goto("http://localhost:8080")  # Replace with your Flask app URL

        # Check if key elements load
        assert page.title() == "Login"
        assert page.locator("text=Please login to continue").is_visible()  # Example: check if "Login" button is visible

        # Screenshot for debugging
        page.screenshot(path="smoke_test.png")

        browser.close()
