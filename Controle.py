from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import os

GREEN = "\033[0;32m"
YELLOW = "\033[93m"
RED = "\033[1;31m"
VIOLET = "\033[95m"

# Load Drivers
options = webdriver.ChromeOptions()

# Set Options
options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-popup-blocking")
options.add_argument("--silent")
options.add_argument("--log-level-3")

services = webdriver.chrome.service.Service(ChromeDriverManager().install())

# Initialize Chrome Driver
navegador = webdriver.Chrome(options=options)

'''
# Dream big: rebuild code into callable DEFs for multi operation capabilities, e.g.:
c = int(input('Você quer, multiplos asins ou apenas um?'))
if c == 0:
    asins = [input('digite o asin')]
    
    for asin1 in asins:
        call_workers() that do this and that.
'''


# Get ASIN for URL build-up
def get_codes():
    asin = input('Digite o ASIN do produto: ')
    try:
        while asin is None or asin == '' or len(asin) > 15:
            print(RED, 'Algo deu errado.')
            asin = input('Digite o ASIN do produto (e.g.: B93JDA31G): ')
    except ValueError:
        print(RED, 'Algo deu errado. Tente novamente mais tarde.')
        sleep(1.5)
        quit()


# Get URL
navegador.get(f'https://www.amazon.com/dp/{asin}')

# Get Price and Name
current_time = datetime.now()
try:
    raw_usd_price = navegador.find_element(By.CSS_SELECTOR, '.a-price').text
    print(VIOLET, 'What I got: ', raw_usd_price)

    if "$" in raw_usd_price:
        raw_price = raw_usd_price.removeprefix('$')
        print(YELLOW, 'Dollar $ sign removed: ', raw_price)
        # if "\n" in raw_price:
        cleaned_price = raw_price.replace(',', '').replace('\n', '.')
        _price = float(cleaned_price)
        print(GREEN, 'Replaced: ', _price)

    p_name = navegador.find_element(By.ID, 'productTitle').text
    print(VIOLET, 'Product name: ', p_name)
except Exception as e:
    print(RED, f'Dedell, an error occurred: {e}')
    _price = 0
    pass

# Exchange Rate Data
navegador.get("https://www.google.com/finance/quote/BRL-USD?hl=en")
exc_BRL_USD = float(navegador.find_element(By.CSS_SELECTOR, '.fxKbKc').text, )
print(VIOLET, 'Cotação atual: $', exc_BRL_USD)

# Assign columns data - row operation:
ws_asin = [asin]
ws_price = [round(_price / exc_BRL_USD, 2)]
ws_name = [p_name]
date = [str(current_time.strftime('%m/%d/%Y'))]

# GPT Helped me think - Check file existence, then, append/create new info:
excel_file = './Controle.xlsx'
if os.path.exists(excel_file):

    # Reads Excel; Creates a new DF that does not overwrite existing column data; Append data.
    existing_df = pd.read_excel(excel_file)
    new_df = pd.DataFrame(list(zip(ws_asin, ws_name, ws_price, date)), columns=existing_df.columns)
    existing_df = pd.concat([existing_df, new_df], ignore_index=True)

    existing_df.to_excel(excel_file, index=False)
    print(GREEN, f"Dedell, I've successfully appended the received data to {existing_df}")

else:
    # Generate columns and create Excel with new data
    columns = ['ASIN', 'PRODUCT', 'PRICE', 'DATE']
    new_df = pd.DataFrame(list(zip(ws_asin, ws_name, ws_price, date)), columns=columns)
    new_df.to_excel(excel_file, index=False)
    print(GREEN, f"Dedell, I've successfully created {new_df} with the received data")
