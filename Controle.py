import os
from datetime import datetime
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

GREEN = "\033[0;32m"
YELLOW = "\033[93m"
RED = "\033[1;31m"
VIOLET = "\033[95m"


# Initializes a new Class
class GetInfo:

    # Initializes self.variables
    def __init__(self):
        self.p_name = None
        self._price = None
        self.exc_BRL_USD = None
        self.current_time = None
        self.clean = None
        self.path = None
        self.navegador = None
        self.asin = None

    # Gets system information and gives the right attributes
    def system_type(self):
        # If its UNIX like system:
        if os.name == 'posix':
            self.clean = os.system('clear')
            self.path = './Controle.xlsx'
        # If its Windows-NT like system:
        elif os.name == "nt":
            self.clean = os.system("cls")
            self.path = '.\Controle.xlsx'
        # If its unrecognizable:
        else:
            raise OSError(f"I'm sorry, your system is currently not supported. {os.name}")
        return self.clean, self.path

    # Get ASIN for URL build-up
    def get_asins(self):
        self.system_type()
        try:
            sel = int(input("- Digite 1 para busca única\n- Digite 2 para múltiplas buscas\nEscreva> "))
            while sel not in [1, 2]:
                print(self.clean)
                print("Por favor:")
                sel = int(input(" - Digite 1 para busca única\n - Digite 2 para múltiplas buscas\n Escreva> "))
            print(GREEN, sel)
        except ValueError:
            print(RED, 'Algo deu errado, tente mais tarde.')
            sleep(2)
            quit()

        if sel == 1:
            try:
                self.asin = input('Digite o ASIN do produto: ')
                while self.asin is None or self.asin == '' or len(self.asin) > 15:
                    print(RED, 'Algo deu errado.')
                    self.asin = input('Digite o ASIN do produto (e.g.: B93JDA31G): ')
            except ValueError:
                print(RED, 'Algo deu errado. Tente novamente mais tarde.')
                sleep(1.5)
                quit()
        elif sel == 2:
            df_as = pd.read_excel(self.path)
            self.asin = df_as['ASIN'].tolist()
            print(self.asin)
        else:
            pass
        return self.asin

    def get_price_n_name(self):
        self.current_time = datetime.now()
        try:
            raw_usd_price = self.navegador.find_element(By.CSS_SELECTOR, '.a-price').text
            print(VIOLET, 'What I got: ', raw_usd_price)

            if "$" in raw_usd_price:
                raw_price = raw_usd_price.removeprefix('$')
                print(YELLOW, 'Dollar $ sign removed: ', raw_price)
                # if "\n" in raw_price:
                cleaned_price = raw_price.replace(',', '').replace('\n', '.')
                self._price = float(cleaned_price)
                print(GREEN, 'Replaced: ', self._price)

            self.p_name = self.navegador.find_element(By.ID, 'productTitle').text
            print(VIOLET, 'Product name: ', self.p_name)
        except Exception as e:
            print(RED, f'Dedell, an error occurred: {e}')
            _price = 0

        # Exchange Rate Data
        self.navegador.get("https://www.google.com/finance/quote/BRL-USD?hl=en")
        self.exc_BRL_USD = float(self.navegador.find_element(By.CSS_SELECTOR, '.fxKbKc').text, )
        print(VIOLET, 'Cotação atual: $', self.exc_BRL_USD)

        return self.p_name, self._price, self.exc_BRL_USD

    def web_ops(self):
        # Run ASIN code
        self.get_asins()
        # Load Drivers
        options = webdriver.ChromeOptions()

        # Set Options
        options.add_argument("--headless")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--silent")
        options.add_argument("--log-level-3")

        # services = webdriver.chrome.service.Service(ChromeDriverManager().install())

        # Initialize Chrome Driver
        self.navegador = webdriver.Chrome(options=options)

        site = f'https://www.amazon.com/dp/{self.asin}'
        print(site)
        # Get URL
        self.navegador.get(site)
        self.get_price_n_name()
        return

    def excel_builder(self):
        self.web_ops()
        # Assign columns data - row operation:
        ws_asin = [self.asin]
        ws_price = [round(self._price / self.exc_BRL_USD, 2)]
        ws_name = [self.p_name]
        date = [str(self.current_time.strftime('%m/%d/%Y'))]

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

    def close_webdriver(self):
        if self.navegador:
            self.navegador.quit()
            print(GREEN, 'Navegador, fechado com sucesso!')
        else:
            print(YELLOW, 'Navegador, não rodou! (WebDriver)')


info_instance = GetInfo()
info_instance.system_type()
info_instance.excel_builder()
