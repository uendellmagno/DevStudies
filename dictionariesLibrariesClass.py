# import pandas as pd
# people = {"first": ["Uendell", 'Thalita', 'Julia'], "last": ["Avila", 'Souza', 'Medeiros'], "email": ["uendellmagno@gmail.com", "thalitaalisouza@gmail.com", "julinheiros@gmail.com"]}
# print(people['first'])
#
# df = pd.DataFrame(people)
# print(df[['first', 'last']])
# print(df.iloc[[0,2], 2])


# Irei criar um banco:

account_number = input("Digite o número da conta: ")
owner = input("Digite o nome do dono da conta: ")
balance = float(input("Digite o saldo da conta: "))
limit = float(input("Digite o limite da conta: "))


def create_account(account_number, owner, balance, limit):
    account = {"account_number": account_number, owner: owner, "balance": balance, "limit": limit}
    return account


def deposit(account, value):
    account['balance'] += value


def withdraw(account, value):
    account['balance'] -= value


def statement(account):
    print(account['balance'])


choice = [0, 1, 2, 3]
choose = int(input("Digite 0 para Nome conta, 1 para depositar, 2 para sacar e 3 para ver o saldo: "))
if choose in choice:

    if choice == 0:
        print('your name is {}'.format(account['owner']))
    elif choice == 1:
        value = float(input("Digite o valor do depósito: "))
        deposit(account, value)
    elif choice == 2:
        withdraw(account, 100)
    elif choice == 3:
        statement(account)
