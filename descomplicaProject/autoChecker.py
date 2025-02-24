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
    """Get Login details from .environment"""
    os.chdir(Path(__file__).resolve().parent)
    load_dotenv('.env')

    email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASSWORD')

    return email, password


def web_ops():
    """Website .get() gathered with Chrome initializer and parameters definers"""
    options = webdriver.ChromeOptions()

    # options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--silent')
    options.add_argument('--log-level-3')

    services = webdriver.chrome.service.Service(ChromeDriverManager().install())

    browser = webdriver.Chrome(options=options)

    browser.get('https://aulas.descomplica.com.br/')

    return browser


def main():
    """Main function that loads all other functions and executes the given commands on the Descomplica website"""
    browser = web_ops()
    wait = WebDriverWait(driver=browser, timeout=70)

    """login operations"""
    # def login_section():
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[1]/div/div/input")))

    email = browser.find_element(By.XPATH,
                                 "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[1]/div/div/input")
    password = browser.find_element(By.XPATH,
                                    "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[2]/div/div/input")

    email.send_keys(login_params()[0])
    password.send_keys(login_params()[1])

    browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div/div[3]/div/div/form/div[3]/button").click()

    """Logged in navigations to Disciplines section"""
    print("Waiting for the website to be loaded.")
    navbar = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "navbar")))
    print('Loaded!')
    if navbar.is_displayed():
        print('Checking for Banners...')
        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal")))
        if modal.is_displayed():
            print('Got a banner! Already working on it...')
            try:
                browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[2]/div/div/div/button").click()
                print("Successfully closed the 'modal' banner!")

            except NoSuchElementException:
                print("Couldn't close the 'modal' banner!")
                # login_section() browser.get(/main again)- retry
                print("Giving up... :(")
                sleep(3)
                browser.quit()
                quit()

        else:
            print("There are no banners.")
            pass

    try:
        browser.find_element(By.XPATH,
                             "/html/body/div[4]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/ul/li[3]").click()
    except:
        print(f"Couldn't click on Disciplinas: {traceback.format_exc()}")

    browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div/div[1]/span/div").click()
    try:
        ps = browser.find_element(By.XPATH, "//div[contains(@class, 'modal')]/div/ol/li/span/p")
        print(ps.text)
        browser.execute_script()

    except Exception as e:
        print('exception', e)

    for p in ps:
        text = p.text



    sleep(1000)
    browser.quit()


if __name__ == "__main__":
    main()
