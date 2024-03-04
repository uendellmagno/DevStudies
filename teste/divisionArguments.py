# import inspect
# def division(a, b, name):
#     print(name)
#     return a / b
#
#
# dividend = 10
# divisor = 2
# result_of_division = division(dividend, divisor, 'divisor')

result = {'Client 1': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')],
          'Client 2': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')],
          'Client 3': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')],
          'Client 4': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')],
          'Client 5': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')],
          'Client 6': [('Brazil', '2021-05-01', 'Success'), ('Canada', '2021-05-01', 'Success')]}

total_clients = len(result.keys())
fails = 0

result_message = '_Summary_ of Partial update - *DAILY:*\n\n```'
for client_name, details_list in result.items():
    for i, country, when_ran, status in enumerate(details_list):
        result_message += f'{status} - {client_name} - {country} - {when_ran}'
        if i < len(details_list) - 1:
            result_message = '\n'
result_message += f'```\n\n*Total Clients:* {total_clients} | *Accounts Failed:* {fails}'

print(result_message)
