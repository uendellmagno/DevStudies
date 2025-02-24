from datetime import datetime as dt
import time

today = dt.strftime(dt.today().date(), '%m/%d/%Y')
# today = dt.strptime(today, '%m/%d/%Y')

today_ = dt.strptime(dt.strftime(dt.today().date(), '%m/%d/%Y'), '%m/%d/%Y')

date_range = f"from {today_.strftime("%d/%m")} to {today_.strftime("%m/%d")}"

print(today, type(today))
print(today_, type(today_))
print(date_range)

start_time = dt.now()
run_time = dt.now() - start_time
print(f'Run time: {dt.now() - start_time}')


