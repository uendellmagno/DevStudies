import os
import slack_sdk as slack
from dotenv import load_dotenv
import traceback
import json
import requests



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
print(token)

client = slack.WebClient(token=token)

a = 'Teste'
b = 'de'
c = 'mensagem'
d = 'YEY!'

msg = 'Tst of summary: \n\n```'
for i in range(500):
    msg += f'\n{a} - {b} - {c} - {d}'
msg += '```\n\n Teste de fim'

fetch_api = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()
exchangerate_api = fetch_api['rates']['BRL']


fetch_api = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL').json()
awesome_api = fetch_api['USDBRL']['high']
print(f"Exchange rate: {awesome_api}")

with open('exchange_rate.json', 'w') as f:
    f.write(f'{fetch_api}')
    f = open('exchange_rate.json', 'w')
    f.close()
# client.chat_postMessage(channel='U06GSVDJRCP', text=msg)
# user_list()

# import json
#
# a = 'Teste'
# b = 'de'
# c = 'mensagem'
# d = 'YEY!'

# blocks = [
#     {
#         "type": "section",
#         "text": {
#             "type": "mrkdwn",
#             "text": f"*Tst of summary:* \n\n```",
#         },
#     },
#     {
#         "type": "section",
#         "text": {
#             "type": "mrkdwn",
#             "text": "Teste de fim",
#         },
#     },
# ]
#
# for i in range(110):
#     blocks[0]['text']['text'] += f'\n{a} - {b} - {c} - {d}'
# blocks[0]['text']['text'] += '```'

# print(blocks)
# client.chat_postMessage(channel='U06GSVDJRCP', blocks=json.dumps(blocks))







