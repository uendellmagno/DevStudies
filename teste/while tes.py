import traceback
import ntplib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pyotp
from dotenv import load_dotenv
import os
import slack_sdk as slack
import ssl

# Disable SSL certificate verification (not recommended for production) - for macOS environment test only
ssl._create_default_https_context = ssl._create_unverified_context

token = 'xoxb-975889060628-5597501425762-71SVkYEiIWqTdjSAep0hERO9'
client = slack.WebClient(token=token)

def inicializar():
    # Define as opções do Chrome (opcional)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--silent')
    options.add_argument('--log-level=3')

    service = webdriver.chrome.service.Service(ChromeDriverManager().install())

    # Cria uma instância do WebDriver passando o Service e as opções
    navegador = webdriver.Chrome(service=service, options=options)

    navegador.get(
            'https://sellercentral.amazon.com/authorization/select-account?returnTo=%2Fbusiness-reports&mons_redirect'
            '=remedy_url')

    return navegador

def otp(conta):
    def get_google_time():
        try:
            # Servidor NTP do Google
            ntp_server = 'time.google.com'

            client = ntplib.NTPClient()
            response = client.request(ntp_server)
            ntp_timestamp = response.tx_time
            return ntp_timestamp
        except ntplib.NTPException:
            return None

    # Backup 1
    if conta == 'amazonuser01@sellersflow.com':
        backup = "X3QEBV25GAVS37HP5O3J3UGQBD4JCCNGNNATQNCSKVPLBOY6SF6A" #-A +Q
    else:
        raise ValueError(f'Conta "{conta}" não cadastrada')

    # Gerar OTPs a partir dos backups
    otp1 = pyotp.TOTP(backup, interval=30)

    # Obter o horário correto do servidor NTP do Google
    google_time = get_google_time()

    if google_time is not None:
        # Gerar o OTP com base no horário do Google
        otp_value = otp1.at(int(google_time))
        return otp_value
    else:
        otp_value = otp1.now()
        return otp_value

def login(conta):
    token = 'xoxb-975889060628-5597501425762-71SVkYEiIWqTdjSAep0hERO9'
    client = slack.WebClient(token=token)
    navegador = inicializar()
    sleep(1)

    seguir = False
    while not seguir:
        try:
            navegador.find_element('xpath', '//*[@id="ap_email"]').send_keys(conta)
            senha = 'ydf6edb@vkf.fvm9PKE'
            navegador.find_element('xpath', '//*[@id="ap_password"]').send_keys(senha)
            navegador.find_element('xpath', '//*[@id="signInSubmit"]').click()

            nova_pag = False
            i = 1
            while not nova_pag:
                try:
                    navegador.find_element('xpath', '//*[@id="auth-mfa-otpcode"]').send_keys(otp(conta))
                    print(f'Autenticando... Tentativa {i}')
                    navegador.find_element('xpath', '//*[@id="auth-signin-button"]').click()
                    if 'signin' not in navegador.current_url or '/ap/' not in navegador.current_url:
                        try:
                            navegador.refresh()
                            navegador.find_element('xpath', '//*[@id="auth-error-message-box"]/div')
                        except:
                            nova_pag = True
                            seguir = True


                except:
                    print(traceback.format_exc())

                i += 1
                if i == 5:
                    print(i, ' - 5 tentativas sem sucesso')
                    client.chat_postMessage(channel='C06L5UAQYBD',
                                            text=f'WARNING - {conta} - 100 failed attempts, still trying...')
                    sleep(5)
                elif i == 10:
                    print(i, ' - 10 tentativas sem sucesso, saindo...')
                    client.chat_postMessage(channel='C06L5UAQYBD',
                                            text=f'*WARNING* - {conta} - 200 failed attempts, giving up.\n*EXITING* >> '
                                                 f'Please, restart the program')
                    seguir = False
                    sleep(5)
                    quit()
                else:
                    print(i)

            if 'returnTo' not in navegador.current_url:
                seguir = False
                navegador.refresh()

        except:
            if '/ap/signin' not in navegador.current_url:
                seguir = True
            try:
                navegador.find_element('xpath', '/html/body/div/div[1]/div[2]/div/h4')
                sleep(2)
            except:
                pass
            navegador.refresh()

login('amazonuser01@sellersflow.com')