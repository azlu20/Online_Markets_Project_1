import csv
import random
import numpy as np
data = []
bids = [9, 11, 21, 31, 41, 51, 61, 71, 81, 91]
value = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
with open('bid_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)

data.pop(0)


rows = 42
trials = 100
i = 0
monte_carlo_sim = []

for idx, bid in enumerate(bids):
    cur_bid_sim = []
    i = 0
    while i < trials:
        rand_row = random.randint(0, 41)
        rand_col = random.randint(0, 9)

        if float(data[rand_row][rand_col]) <= bid:
            cur_bid_sim.append(value[idx] - bid)
        elif float(data[rand_row][rand_col]) > bid:
            cur_bid_sim.append(0)

        i+=1
    monte_carlo_sim.append(cur_bid_sim)

monte_carlo_sim = np.array(monte_carlo_sim)


averaged_monte_sim = np.divide(monte_carlo_sim, trials)
#N >= (ln(2)/alpha) / (2 * epsilon**2)
#TODO: ask about equation and figure out trial number for 95% confidence
print(f"Monte carlo simulated utility for {trials} trials {averaged_monte_sim.sum(axis=1)}")

exact_values = []
for idx, bid in enumerate(bids):
    cur_row = []
    for r in data:
        for c in r:
            if float(c) <= bid:
                cur_row.append(value[idx] - bid)
            elif float(c) > bid:
                cur_row.append(0)

    exact_values.append(cur_row)

exact_values = np.array(exact_values)
summed_exact = exact_values.sum(axis=1)
utility_exact = np.divide(summed_exact, len(data) * len(data[0]))

print(f"Exact total utility {summed_exact}")
print(f"Exactly utility {utility_exact}")

best_values = [-1 for i in range(len(value))]
best_utility = [-1 for i in range(len(value))]
for idx, bid in enumerate(value):
    max = -1
    for cur_bid in range(0, bid+1):
        utility = 0
        for r in data:
            for c in r:
                utility += value[idx] - cur_bid if cur_bid >= float(c) else 0

        if utility >= max:
            best_values[idx] = cur_bid
            best_utility[idx] = utility
            max = utility

print(f"Best value for maximum utility within this dataset is {best_values}")

epsilons = [0.9, 0.5, 0.1, 0.01, 0.0001] #tested for multiple epsilon values such as 0.8, 0.5, 0.01, 0.0001

for epsilon in epsilons:
    for idx, val in enumerate(best_values):
        utility = 0
        upper_val = val + epsilon
        for r in data:
            for c in r:
                utility += value[idx] - upper_val if upper_val >= float(c) else 0

        if utility > best_utility[idx]:
            best_utility[idx] = utility
            best_values[idx] = upper_val

        utility = 0
        lower_val = val - epsilon
        for r in data:
            for c in r:
                utility += value[idx] - lower_val if lower_val >= float(c) else 0

        if utility > best_utility[idx]:
            best_utility[idx] = utility
            best_values[idx] = upper_val

print(f"Best value for maximum utility within this dataset is {best_values}") #know this is true maximum as changing by an epsilon did not change anything

#TODO update report for question 2/3 with logic along these lines
#the best way to increase utility is to beat up the small numbers, around 20-30 lower than your value because even though you will likely beat less larger numbers,
# the few times you do beat the smaller numbers, the gains are much more increased
#additionally, since many people tried to game the system by choosing exactly 9 less than their value, tieing or beating them with a tiny epsilon is a good strategy

#TODO Part 2:
#Ideas: simply average the data and then beat the data by a tiny epsilon
#run a standard deviation to calculate likely it is a bid to be away from the median and then calculate the percentage chance for a smaller bid to win weighing that against the increased utility

#1 sample: probably just beat out the value by a tiny bit or stick to the same value
#10 sample: can calculate the standard deviation, but stick to standard deviations closer to the median since the sigma and values are not guranteed to be fully accurate
#100 samples: can start exploring further away data such as more sigmas away from median
