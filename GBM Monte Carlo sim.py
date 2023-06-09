import numpy as np
import matplotlib.pyplot as plt
import math

dict = {'price': 100, 'sigma': 0.3, 'return': 0.15, 'time': 0.001, 'time_total': 1}
# time increment is typically of one year
# by all means the time total is just the 'long-term', while time is the incremental change of small time steps
# sigma and return are both annualized

# one week = 0.0192 of a year

time_list = [0]
time_increment = round(int(dict['time_total']/dict['time']),0)
price_list = [dict['price']]
for num in range(0,time_increment):
    rng = np.random.default_rng()
    numbers = rng.normal()
    change = dict['return']*price_list[num]*dict['time'] + dict['sigma']*math.sqrt(dict['time'])*price_list[num]*numbers
    new_price = price_list[num]+change
    price_list.append(new_price)
    time_list.append(num)

plt.plot(time_list, price_list)
plt.xlabel('Time')
plt.ylabel('Stock Price ($)')
plt.show()