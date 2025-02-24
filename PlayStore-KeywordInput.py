from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Load keywords from a text file (comma-separated)
with open("keywords.txt", "r", encoding="utf-8") as file:
    keywords = file.read().split(",")

# Initialize Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Keeps browser open
driver = webdriver.Chrome(options=options)

# Open the target webpage
url = "https://play.google.com/console/u/0/developers/5124211662090352559/app/4975364078217239196/custom-store-listings/create?linkedFrom=main"
driver.get(url)

# Wait for the page to load
wait_time = 60
for i in range(wait_time, 0, -1):
    print(f"Waiting for page to load... {i}s remaining", end="\r")
    time.sleep(1)

print("\nPage loaded. Starting keyword input...\n")

# Find the input field
input_xpath = '//*[@id="default-acx-overlay-container"]/div[5]/div/focus-trap/div[2]/relative-popup/div/span/div/div[2]/div/console-block-1-2/div[1]/div/console-search-input/div/material-input/label/input'

try:
    input_field = driver.find_element(By.XPATH, input_xpath)

    total_keywords = len(keywords)
    for i, keyword in enumerate(keywords, start=1):
        keyword = keyword.strip()
        if keyword:
            input_field.send_keys(keyword)
            input_field.send_keys(Keys.RETURN)
            input_field.clear()

            print(f'Added "{keyword}" - {i}/{total_keywords}')

    print("\nAll keywords entered successfully!")

except Exception as e:
    print(f"\nError: {e}")

# Keep browser open or close it after completion
# driver.quit()  # Uncomment to close browser after execution
