import os
import slack_sdk as slack
from dotenv import load_dotenv
import traceback
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def user_list():
    members = client.users_list()['members']

    for member in members:
        try:
            print(f'{member["real_name"]}: {member["id"]}')
        except:
            pass


load_dotenv(
    dotenv_path=r'/Users/uendellmagno/Library/CloudStorage/GoogleDrive-uendell.magno@sellersflow.com/.shortcut-targets-by-id/1G-jxbsNLb5a3HcpcgBsa13UAAMM1Oc8I/Clients/Current/00. Others/08. Analytics/PowerBI/Robot Data/Programa e Logs/config 2.0/env/.env')
token = os.getenv('SLACK_API_TOKEN')

client = slack.WebClient(token=token)

msg = 'Tst of summary: \n\n```'
for i in range(100):
    msg += '\n Teste de mensagem'
msg += '```\n\n Teste de fim'

client.chat_postMessage(channel='U06GSVDJRCP', text=msg)
# user_list()
