from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time as t

# Instantiate WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

# Chrome Options:
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-popup-blocking")
options.add_argument("--incognito")
options.add_argument("--silent")
options.add_argument("--log-level-3")

# Input URL
driver.get("https://www.amazon.com")
assert "Amazon" in driver.title

# Click actions through XPATH - Change Region
button = driver.find_element(By.XPATH, '//*[@id="icp-touch-link-country"]')
button.click()
button = driver.find_element(By.XPATH, '//*[@id="icp-dropdown"]/span/span')
button.click()
button = driver.find_element(By.XPATH, '//*[@id="icp-dropdown_2"]')
button.click()
button = driver.find_element(By.XPATH, '//*[@id="icp-save-button"]/span/input')
button.click()

print('success! :)')
t.sleep(10000)

driver.close()
