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

# a = 'Teste'
# b = 'de'
# c = 'vczvcxcxvczVVVVVVVVVVlongmessagerczvczxvczxvxvcxzvc'
# d = 'YEY!'
#
# _structure = ''
# for i in range(80):
#     phrase = f'\n{a} - {b} - {c} - {d}'
#     print('phrase:', phrase)
#     if len(_structure + phrase) <= 4000:
#         _structure += phrase
#         print('structure is: ', _structure)
#     else:
#         _structure += '...break_here...'
#         print('structure is: ', _structure)
#     if len(_structure) > 0:
#         _structure += '...break_here...'
#
# messages = _structure.split('...break_here...')
# print('MESSAGES SPLIT:', messages)
# header = '_Summary_ of Partial update - *DAILY:*\n\n'
# footer = f"*Total Clients:* XX | *Accounts Failed:* XX"
#
# client.chat_postMessage(channel='U06GSVDJRCP', text=header)
# for message in messages:
#     client.chat_postMessage(channel='U06GSVDJRCP', text=f"```{message}```")
#     print('message:', message)
# client.chat_postMessage(channel='U06GSVDJRCP', text=footer)

a = 'Teste'
b = 'de'
c = 'vczvcxcxvczVVVVVVVVVVlongmessagerczvczxvczxvxvcxzvc'
d = 'YEY!'

messages = []
current_message = ''
for i in range(150):
    phrase = f'\n{a} - {b} - {c} - {d}'

    # Check if current message + phrase fits within the limit
    if len(current_message + phrase) <= 4000:
        current_message += phrase
    else:
        # If overflow, add current message as a block and start a new one
        messages.append(f"```{current_message}```")
        current_message = phrase

# Add the last message block even if it's less than 4000 characters
if current_message:
    messages.append(f"```{current_message}```")

header = '_Summary_ of Partial update - *DAILY:*\n\n'
footer = f"*Total Clients:* XX | *Accounts Failed:* XX"

client.chat_postMessage(channel='U06GSVDJRCP', text=header)
for message in messages:
    client.chat_postMessage(channel='U06GSVDJRCP', text=message)  # Send each message as a code block
    print('message:', message)
client.chat_postMessage(channel='U06GSVDJRCP', text=footer)



#
# # Check if the message exceeds Slack API character limit (maximum is 4000 characters)
# if counter <= 80:
#     # Send the result as a single code block
#     fm = f"Tst of summary: \n\n```{msg}```\n\n Teste de fim"
#     client.chat_postMessage(channel='U06GSVDJRCP', text=fm)
# else:
#     # Split the message into chunks if it exceeds the character limit
#     chunk_size = 4000  # Adjust as needed
#     result_chunks = [result_code_block[i:i + chunk_size] for i in range(0, len(result_code_block), chunk_size)]
#
#     client.chat_postMessage(channel='U06GSVDJRCP', text=f'{lele}')
#     # Send each chunk as a separate message
#     for chunk in result_chunks:
#         client.chat_postMessage(channel='U06GSVDJRCP', text=f'```{chunk}```')
#     client.chat_postMessage(channel='U06GSVDJRCP', text=f'Teste de fim')

# fetch_api = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()
# exchangerate_api = fetch_api['rates']['BRL']
#
#
# fetch_api = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL').json()
# awesome_api = fetch_api['USDBRL']['high']
# print(f"Exchange rate: {awesome_api}")
#
# with open('exchange_rate.json', 'w') as f:
#     f.write(f'{fetch_api}')
#     f = open('exchange_rate.json', 'w')
#     f.close()
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







