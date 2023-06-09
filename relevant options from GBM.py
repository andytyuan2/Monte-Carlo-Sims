import numpy as np
import matplotlib.pyplot as plt
import math

dict = {'price': 100, 'sigma': 0.3, 'return': 0.15, 'time': 0.001, 'time_total': 1}
# sigma and return are both annualized

option = {'strike' : 100, 'time steps' : 50, 'years': 2, 'risk-free rate': 0.03, 'dividend': 0.0, 
        'callput': 1, 'AmerEu': 1}
option['sigma'] = dict['sigma']
option_list = []

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

for num in price_list:
    option['price'] = num
    u = math.exp(option['sigma']*math.sqrt(option['years']/option['time steps']))
    d = 1/u
    probup = (((math.exp((option['risk-free rate']-option['dividend'])*option['years']/option['time steps'])) - d) / (u - d))
    discount_factor = option['risk-free rate']/option['time steps']
    duration_of_time_step = (option['years']/option['time steps'])

    if option['callput'] > 0:
        type = 'calls'
    else:
        type = 'puts'
    if option['AmerEu'] > 0:
        exercise = 'American'
    else:
        exercise = 'European'
    ##################################################################################################################################################################################### 
    def binomial():
        Tstep = option['time steps']
        payoffs = []
        for n in range(Tstep +1): 
            payoffs.append(max(0, option['callput']*(option['price']*(u**((Tstep)-n))*(d**n) - option['strike'])))     
        while Tstep >= 1:
    #####################################################################################################################################################################################
        # not used in the actual calculation but useful to see what the probabilities of each node is at a specific timestep    
            def combos(n, i):
                return math.factorial(n) / (math.factorial(n-i)*math.factorial(i))

            pascal = []
            for i in range(Tstep+1):
                pascal.append(combos(Tstep, i))

            probabilities = []
            for i in range(Tstep+1):
                probabilities.append(pascal[i]*(probup**((Tstep)-i))*((1-probup)**i))
    #####################################################################################################################################################################################
            discounting1 = []
            i = 0
            for i in range(0,Tstep):
                if option['AmerEu'] == 1:
                    American_payoff = (option['callput']*(option['price']*(u**(Tstep-i-1)*(d**i)) - option['strike']))
                    European_payoff = (((probup)*payoffs[i]) + ((1-probup)*payoffs[i+1])) / (math.exp(discount_factor))
                    discounting1.append(max(American_payoff, European_payoff))
                elif option['AmerEu'] == -1:
                    discounting1.append((((probup)*payoffs[i]) + ((1-probup)*payoffs[i+1]))
                                        / (math.exp(discount_factor)))
                else:
                    pass 
                
            payoffs.clear()
            payoffs.extend(discounting1)
            Tstep -= 1

        return discounting1[0]
    option_list.append(binomial())

plt.plot(time_list, price_list, label='Stock Price')
plt.plot(time_list, option_list, label='Option Price')
plt.xlabel('Time Increments')
plt.ylabel('Price ($)')
plt.legend()
plt.show()