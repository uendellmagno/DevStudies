# import logging
# import os
# from datetime import datetime
# from time import sleep
#
# def amazon():
#     a = 'john'
#     b = 'brazil'
#     c = datetime.now()
#     print('logged in')
#     with open('/Users/uendellmagno/Library/CloudStorage/GoogleDrive-uendell.magno@sellersflow.com/.shortcut-targets'
#               '-by-id/1G-jxbsNLb5a3HcpcgBsa13UAAMM1Oc8I/Clients/Current/00. Others/08. Analytics/PowerBI/Robot '
#               'Data/Programa e Logs/logs/business report/Summary_Report.txt', 'a') as summary:
#         summary.write(f'\n{a} {b} {c} - SUCCESS\n')
#
#     print('logged out')
#     with open(
#             '/Users/uendellmagno/Library/CloudStorage/GoogleDrive-uendell.magno@sellersflow.com/.shortcut-targets-by'
#             '-id/1G-jxbsNLb5a3HcpcgBsa13UAAMM1Oc8I/Clients/Current/00. Others/08. Analytics/PowerBI/Robot '
#             'Data/Programa e Logs/logs/business report/Summary_Report.txt',
#             'a') as summary:
#         summary.write(f'\n{a} {b} {c} - FAILED\n')
#
# amazon()

import datetime

# def param():
#     status = ''
#     selector = {'Select':{
#                     'Uendell': {'Country': {'Brazil', 'United States', 'Europe'}},
#                     'Thalitinha': {'Country': {'Brazil', 'Australia', 'Panama'}}
#                     }
#                 }
#     start_time = ''
#     result = teste(selector, start_time)
#
#
# def teste(selector, start_time):
#     for client, client_info in selector['Select'].items():
#         client_countries = client_info.get('Country')
#
#     return {'Cliente': {'Status': 'VERDADEIRO', 'Cliente': f'{selector}', 'Country': f'{country}', 'Time': f'{start_time}' }}


import time

def param():
    status = ''
    selector = {'Select': {
                    'Uendell': {'Country': {'Brazil', 'United States', 'Europe'}},
                    'Thalitinha': {'Country': {'Brazil', 'Australia', 'Panama'}}
                    }
                }
    start_time = ''
    result = teste(selector, start_time)

    # Process the result dictionary to create a txt file
    with open('output.txt', 'w') as file:
        for client, details in result.items():
            for country, status, execution_time in details:
                file.write(f"{client} - {country} - {execution_time} - {status}\n")


def teste(selector, start_time):
    result = {}

    print(selector,'\n')
    print(selector['Select'],'\n')
    print(selector['Select'].items(),'\n')

    for client, details in selector['Select'].items():
        client_name = client
        countries = details['Country']
        print(client_name, countries, '\n')

        for country in countries:
            # Perform actions with client_name, country, and time_now
            time_now = time.strftime("%Y-%m-%d %H:%M:%S")
            status = 'SUCCESS'  # You can modify this based on your actual logic

            # Print the output
            print(f"{client_name} - {country} - {time_now}")

            # Store the result in the dictionary
            if client_name not in result:
                result[client_name] = []
            result[client_name].append((country, status, time_now))

    return result

# Call the param function to execute the code
param()
