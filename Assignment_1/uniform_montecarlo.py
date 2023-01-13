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
trials = 185
i = 0
monte_carlo_sim = []
#alpha is the confidence error, and epsilon times h which gives how much utility you are off
#TODO calculate what the error (alpha) is with value 42
#TODO calculate probability to win the bid
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
print(monte_carlo_sim.shape)
print(f"Monte carlo simulated utility for {trials} trials {np.sum([0.087,1.89, 2.92, 4.33, 5.21, 6.2868, 7.10, 7.83, 8.37, 8.85])/10}")

def calculateExpectedUtility(bids, data):
    exact_values = []
    winning_probability = []
    for idx, bid in enumerate(bids):
        cur_row = []
        win_prob = 0
        for r in data:
            for c in r:
                if float(c) <= bid:
                    win_prob += 1
                    cur_row.append(value[idx] - bid)
                elif float(c) > bid:
                    cur_row.append(0)

        exact_values.append(cur_row)
        winning_probability.append(win_prob)

    exact_values = np.array(exact_values)
    summed_exact = exact_values.sum(axis=1)
    utility_exact = np.divide(summed_exact, len(data) * len(data[0]))
    winning_probability = np.divide(winning_probability, len(data) * len(data[0]))
    print(exact_values.shape)
    # print(f"Exact total utility {summed_exact}")
    # print(f"Exactly utility {utility_exact}")
    return utility_exact, winning_probability

extended_data = []
step = 0.01
#slightly lower than median for values [0, value] based on data sample?

for idx, val in enumerate(value):
    extended_data.append(np.arange(val-10, val, step))

best_values = [-1 for i in range(len(value))]
best_utility = [-1 for i in range(len(value))]
best_prob = [-1 for i in range(len(value))]
all_utility = []

for idx, val in enumerate(value):
    max = -1
    for cur_bid in np.arange(0, val):
        utility = 0
        beat = 0
        for r in data:
            for c in r:
                utility += value[idx] - cur_bid if cur_bid >= float(c) else 0
                beat += 1 if cur_bid >= float(c) else 0
        if utility >= max:
            best_values[idx] = cur_bid
            best_utility[idx] = utility
            best_prob[idx] = beat
            max = utility
        all_utility.append(utility)


print(f"Best value for maximum utility within this dataset is {best_values}")
print(f"Best expected utility winning probability is {np.divide(best_prob, 420)} ")
print(f"Best expected utility within this data is {np.divide(best_utility, len(data) * len(data[0]))}")

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
#just say that raising it by a tiny epsilon is basically insignficant


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

#TODO Can generate more data points to test out this algorithm, try to increase samples by a good amount

#Assumption: noone bids above their value in order to produce negative utility


def algorithm(data):
    num_samples = len(data)
    out = [-1 for i in range(len(value))]
    for idx, val in enumerate(value):
        less_than = []
        for r in data:
            for c in r:
                if float(c) <= val:
                    less_than.append(float(c))
        median = np.median(less_than)
        std = np.std(less_than)
        calculated_value = median + (num_samples/50)
        out[idx] = calculated_value
    return out


new_bids = algorithm(extended_data)

print(calculateExpectedUtility(best_values, data))
print(np.sum(calculateExpectedUtility(new_bids, data)))

real_expected = calculateExpectedUtility(bids, data)[0]

print(np.sum(real_expected)/10)
print(100 * np.divide(np.abs(np.subtract(real_expected, averaged_monte_sim.sum(axis=1))), real_expected))
extended_value = np.arange(0, 100, 1)
prob_chance = calculateExpectedUtility(np.add(value, 1), data)[1]

best_utility_prob = np.divide(best_prob, 420)
# prob_chance = np.multiply(prob_chance, 100)


import matplotlib.pyplot as plt



# for val in value:
#     utility = list(map(lambda x: val - x, np.arange(10, 110, 10)))
#     expected_utility = np.multiply(prob_chance, utility)
#     plt.plot( np.arange(10, 110, 10), expected_utility, label=f"Value {val}")
#
# plt.legend()
# plt.title("Expected Utility vs Bid Value ")
# plt.xlabel("Bid Value")
# plt.ylabel("Expected Utility")
#
# # plt.ylim(np.min(prob_chance), np.max(prob_chance))
# # plt.plot(np.multiply(prob_chance, 100), np.arange(0, 100, 10))
# plt.show()

# plt.title("Probability Chance to Win Given Bid Value")
# plt.xlabel("Bid Value")
# plt.ylabel("Probability to Win")
# plt.plot( np.arange(10, 110, 10), prob_chance)
# plt.show()

# for val in value:
#     utility = list(map(lambda x: val - x, np.arange(10, 110, 10)))
#     expected_utility = np.multiply(prob_chance, utility)
#     plt.plot(np.arange(10, 110, 10), utility, label=f"Value {val}")
#
# plt.legend()
# plt.title("Utility if Won vs Bid Value")
# plt.xlabel("Bid Value")
# plt.ylabel("Utility")
#
# # plt.ylim(np.min(prob_chance), np.max(prob_chance))
# # plt.plot(np.multiply(prob_chance, 100), np.arange(0, 100, 10))
# plt.show()
