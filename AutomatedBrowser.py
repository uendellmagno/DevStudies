from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-webauthn")
chrome_options.add_argument("--disable-credential-manager-api")
chrome_options.add_argument("--disable-password-manager")
chrome_options.add_argument("--allow-insecure-localhost")  # Allows insecure connections on localhost
chrome_options.add_argument("--ignore-certificate-errors")  # Ignores certificate errors

# Initialize the WebDriver with ChromeDriverManager
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),  # Auto-detects the correct driver
    options=chrome_options
)

# Test website
try:
    driver.get("http://localhost:5001")
    print(driver.title)
except Exception as e:
    print("An error occurred: ", e)

# Close the browser
if  input("Press any key to close the browser..."):
    driver.quit()
