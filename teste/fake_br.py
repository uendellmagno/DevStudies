from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from pythonProject.teste.login_sc_function import login_sc as lsc

import ssl

# Disable SSL certificate verification (not recommended for production) - for macOS environment test only
ssl._create_default_https_context = ssl._create_unverified_context


def main(url):

    def inicializar():
        # Define as opções do Chrome (opcional)
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument('--silent')
        options.add_argument('--log-level=3')

        service = webdriver.chrome.service.Service(ChromeDriverManager().install())

        # Cria uma instância do WebDriver passando o Service e as opções
        navegador = webdriver.Chrome(service=service, options=options)

        navegador.get(url)
        print('login do fake_br')
        lsc(navegador, 'amazonuser01@sellersflow.com')

    inicializar()
