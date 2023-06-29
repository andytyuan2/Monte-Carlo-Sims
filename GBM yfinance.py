import numpy as np
import matplotlib.pyplot as plt
import math
import yfinance as yf

dict = {'increments': 730, 'years': 2}
ticker = 'gs'
stock = yf.Ticker(ticker)
price = stock.info['currentPrice']
expected_return = stock.info['52WeekChange']
stock_history = np.array(stock.history(period = '1y', interval = '1d')['Close'])
historical_avg = np.average(stock.history(period = '1y', interval = '1d')['Close'])
stock_vol = (np.std(stock_history))/historical_avg
# volatility and expected return are annualized


time_list = [0]
price_list = [price]
for num in range(0,dict['increments']):
    rng = np.random.default_rng()
    numbers = rng.normal()
    change = expected_return*price_list[num]*1/dict['increments'] + stock_vol*math.sqrt(1/dict['increments'])*price_list[num]*numbers
    new_price = price_list[num]+change
    price_list.append(new_price)
    time_list.append(num)

tick = ticker.upper()
day_increment = str((365*dict['years'])/dict['increments'])
plt.figure(figsize=(15,8))
plt.plot(time_list, price_list)
plt.xlabel('Time Increments of '+str(dict['years'])+' year(s)')
plt.ylabel('Stock Price ($)')
plt.xticks(np.arange(min(time_list), max(time_list)+1, 50))
plt.title('GBM price movements for $'+tick+' in '+day_increment+' day increments where expected return = '
          +str(100*expected_return)+'% and volatility = '+str(round(stock_vol,4)*100)+'%')
plt.show()
