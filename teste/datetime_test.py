from datetime import datetime as dt

today = dt.strftime(dt.today().date(), '%m/%d/%Y')
# today = dt.strptime(today, '%m/%d/%Y')

today_ = dt.strptime(dt.strftime(dt.today().date(), '%m/%d/%Y'), '%m/%d/%Y')

print(today, type(today))
print(today_, type(today_))