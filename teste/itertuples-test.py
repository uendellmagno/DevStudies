import pandas as pd
import datetime
from datetime import datetime as dt


current_day = dt.today().strftime('%A')

df = pd.read_excel('/Users/uendellmagno/Desktop/Configuração - AdsFlow BID.xlsx', skiprows=1)
print(f'DF = {df}')

df = df.loc[(df[current_day].notna()) & (df['STATUS'] == 'Ativo')]
print(f'DF with .loc: {df}')

for row in df.itertuples():
    selector = row._2
    country = row.Marketplace

    print(f'Starting Calibration: {selector} - {country}')

    final_date = dt.today() - datetime.timedelta(days=int(row._6[-1])) - datetime.timedelta(hours=dt.today().hour,
                                                                                          minutes=dt.today().minute,
                                                                                          seconds=dt.today().second,
                                                                                          microseconds=dt.today().microsecond)
    start_date = final_date - datetime.timedelta(days=int(row._7[0]))

    roas_target = row._5

    print(roas_target)

