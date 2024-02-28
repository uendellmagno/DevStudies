from datetime import datetime as dt
import pandas
import pandas as pd

path = "/Users/uendellmagno/Desktop/base de dados business report - Copy.xlsx"
hour_now = dt.now().time().hour

df = pd.read_excel(path, sheet_name='Base Business Evento')
print(f'df=\n{df}\n\n')
print(f'df[time]=\n{df['Time']}\n\n')

df['Time'] = pd.to_datetime(df['Time'])

print(f'done=\n{df['Time']}')




