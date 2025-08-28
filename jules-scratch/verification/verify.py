import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8501")
    time.sleep(5)  # Give the page some time to load
    page.screenshot(path="jules-scratch/verification/main_page_anonymous.png")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
