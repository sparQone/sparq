# -----------------------------------------------------------------------------
# sparQ
#
# Description:
#     Smoke test for the application.
#
# Copyright (c) 2025 remarQable LLC
# -----------------------------------------------------------------------------


import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def s_playwright():
    with sync_playwright() as p:
        yield p


def test_smoke(s_playwright):
    browser = s_playwright.chromium.launch(headless=True)  # Run in headless mode for speed
    page = browser.new_page()

    page.goto("http://localhost:8000")  # Replace with your Flask app URL

    # Check if key elements load
    assert page.title() == "Login - SparqOne"
    assert page.get_by_role("button", name="Login")  # Example: check if "Login" button is visible

    # Screenshot for debugging
    page.screenshot(path=".scratch/smoke_test.png")

    browser.close()
