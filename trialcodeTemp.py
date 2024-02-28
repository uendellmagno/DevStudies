from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from time import sleep

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-popup-blocking")
options.add_argument("--silent")
options.add_argument("--log-level-3")

navegador = webdriver.Chrome(options=options)

navegador.get("https://www.google.com/finance/quote/BRL-USD?hl=en")

#r = requests.get("https://www.google.com/finance/quote/BRL-USD?hl=en")
t = float(navegador.find_element(By.CSS_SELECTOR, '.fxKbKc').text)

print(t, type(t))

sleep(100)
