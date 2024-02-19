import logging
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
RESET = "\033[0m"


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
        self.browser = None
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
            raise OSError(f"{YELLOW}I'm sorry, your system is currently not supported. {os.name}")
        return self.clean, self.path

    # Get ASIN for URL build-up
    def get_asins(self):
        # Run system_type operations
        self.system_type()

        try:
            # Choose between 1 or 2 ONLY for further operations
            sel = int(input("- Digite 1 para busca única\n- Digite 2 para múltiplas buscas\nEscreva> "))
            while sel not in [1, 2]:
                # TODO fix: print(self.clean)
                print("Por favor:")
                sel = int(input(" - Digite 1 para busca única\n - Digite 2 para múltiplas buscas\n Escreva> "))
            print(GREEN, sel)
        # Throw exception and get ValueError
        except ValueError as ve:
            logger = logging.getLogger('example')
            logging.error(f'Something weird happened: {ve}')
            logging.info(f'This is info: {ve}')
            logger.debug('This is a debug message')
            logger.info('This is an info message')
            logger.warning('This is a warning message')
            logger.error('This is an error message')
            logger.critical('This is a critical message')
            print(RED, 'Algo deu errado, tente mais tarde.', ve)
            sleep(2)
            quit()

        # Make sel operations:
        if sel == 1:
            try:
                # Get single ASIN
                self.asin = input('Digite o ASIN do produto: ')
                while self.asin is None or self.asin == '' or len(self.asin) > 15:
                    print(RED, 'Algo deu errado.', RESET)
                    self.asin = input('Digite o ASIN do produto (e.g.: B93JDA31G): ')
            # Throw error if it didn't work.
            except ValueError as ve:
                print(RED, 'Algo deu errado. Tente novamente mais tarde. ', ve, RESET)
                sleep(1.5)
                quit()
        # TODO enable it to receive a .TXT or .XSLX; tolerable; verify file type and get an list full of ASINS
        elif sel == 2:
            # TODO -  This is not working properly for now!
            # TODO - out of main purpose
            df_as = pd.read_excel(self.path)
            self.asin = df_as['ASIN'].tolist()
            print(self.asin)
        # Quit program if unable to get ASIN properly
        else:
            print('Algo deu errado, por favor, tente novamente mais tarde! ', ValueError, RESET)
            sleep(1.5)
            quit()
        return self.asin

    # Gets price and name on the Amazon.com/dp/{asin}
    def get_price_and_name(self):
        # Gets today's date and time (complete, even the milliseconds)
        self.current_time = datetime.now()
        try:
            # Try to get price through CSS
            raw_usd_price = self.browser.find_element(By.CSS_SELECTOR, '.a-price').text
            print(VIOLET, 'What I got: ', raw_usd_price)

            # It formats the price tag to be Excel usable
            if "$" in raw_usd_price:
                raw_price = raw_usd_price.removeprefix('$')
                print(YELLOW, 'Dollar $ sign removed: ', raw_price)
                # if "\n" in raw_price:
                cleaned_price = raw_price.replace(',', '').replace('\n', '.')
                self._price = float(cleaned_price)
                print(GREEN, 'Replaced: ', self._price)
            # Try to get the product name through ID
            self.p_name = self.browser.find_element(By.ID, 'productTitle').text
            print(VIOLET, 'Product name: ', self.p_name)
        except Exception as e:
            print(RED, f'Dedell, an error occurred: {e}{RESET}')
            _price = 0

        # Exchange Rate Data
        self.browser.get("https://www.google.com/finance/quote/BRL-USD?hl=en")
        # Tries to get it by CSS
        try:
            # TODO - Try and except, not working properly!
            self.exc_BRL_USD = float(self.browser.find_element(By.CSS_SELECTOR, '.fxKbKc').text, )
            print(f'{VIOLET}Cotação atual: $ {self.exc_BRL_USD}')
        except ValueError as ve:
            self.exc_BRL_USD = float(0)
            print(f"{RED}Não consegui pegar a cotação!\n{RESET}O que peguei: {self.exc_BRL_USD}"
                  f"\nSegue o problema: {RED} {ve}{RESET}")

        return self.p_name, self._price, self.exc_BRL_USD

    # Initializes WebDriver and executes Browser Operations:
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
        self.browser = webdriver.Chrome(options=options)

        # TODO - Do a FOR, if applicable, to search several ASINS at once
        site = f'https://www.amazon.com/dp/{self.asin}'
        print(site)
        # Get URL
        self.browser.get(site)

        # Runs Get Price and Name
        self.get_price_and_name()
        return

    # Creates/Manipulates all the received data and exports that to Controle.xlsx
    def excel_builder(self):
        # Runs WebAsin > Asin > Get price and name
        self.web_ops()
        # Assign columns data - row operation:
        ws_asin = [self.asin]
        ws_price = [round(self._price / self.exc_BRL_USD, 2)]
        ws_name = [self.p_name]
        date = [str(self.current_time.strftime('%m/%d/%Y'))]

        # Check file existence, then, append/create new info:
        excel_file = 'Controle.xlsx'
        if os.path.exists(excel_file):

            # Reads Excel; Creates a new DF that does not overwrite existing column data; Append data.
            existing_df = pd.read_excel(excel_file)
            new_df = pd.DataFrame(list(zip(ws_asin, ws_name, ws_price, date)), columns=existing_df.columns)
            existing_df = pd.concat([existing_df, new_df], ignore_index=True)

            existing_df.to_excel(excel_file, index=False)
            print(f"{GREEN}Dedell, I've successfully appended the received data to {existing_df}{RESET}")

        else:
            # Generate columns and create Excel with new data
            columns = ['ASIN', 'PRODUCT', 'PRICE', 'DATE']
            new_df = pd.DataFrame(list(zip(ws_asin, ws_name, ws_price, date)), columns=columns)
            new_df.to_excel(excel_file, index=False)
            print(f"{GREEN}Dedell, I've successfully created {new_df} with the received data{RESET}")

    def close_webdriver(self):
        if self.browser:
            self.browser.quit()
            print(GREEN, 'Navegador, fechado com sucesso!')
        else:
            print(YELLOW, 'Navegador, não rodou! (WebDriver)')


# Executes the whole thing
info_instance = GetInfo()
info_instance.system_type()
info_instance.excel_builder()
