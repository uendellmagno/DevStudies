from time import sleep
import os
from pathlib import Path
import traceback

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login_params():
    os.chdir(Path(__file__).resolve().parent)
    load_dotenv('.env')

    email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASSWORD')

    return email, password


def web_ops():
    options = webdriver.ChromeOptions()

    options.add_argument('--start-maximized')
    options.add_argument('--silent')
    options.add_argument('--log-level-3')

    services = webdriver.chrome.service.Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(options=options, service=services)

    browser.get('https://aulas.descomplica.com.br/')

    return browser


def main():
    browser = web_ops()
    wait = WebDriverWait(driver=browser, timeout=70)

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[1]/div/div/input")))

    email = browser.find_element(By.XPATH,
                                 "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[1]/div/div/input")
    password = browser.find_element(By.XPATH,
                                    "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[2]/div/div/input")

    email.send_keys(login_params()[0])
    password.send_keys(login_params()[1])

    browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[3]/button").click()

    navbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
    if navbar.is_displayed():
        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
        if modal.is_displayed():

            try:
                browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[2]/div/div/div/button").click()
                print('Successfully closed the modal')

            except NoSuchElementException:
                print("Couldn't close the modal banner")
        else:
            print('no modal')
            pass

    try:
        browser.find_element(By.XPATH,
                             "/html/body/div[4]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/ul/li[3]").click()
    except:
        print(f"Couldn't click on Disciplinas: {traceback.format_exc()}")

    sleep(5)
    browser.quit()


main()
