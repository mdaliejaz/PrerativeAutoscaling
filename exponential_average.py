from functools import *

noOfMachines = 10


# https://weblab.ing.unimore.it/people/sara/papers/casolari-valuetools2006.pdf
def exponential_moving_average(window_values):
    sum = reduce(lambda x, y: x + y, window_values)
    ema0 = sum / noOfMachines
    alpha = int(2 / (noOfMachines + 1))
    expected_rate = alpha * noOfMachines + (1 - alpha) * ema0
    return int(expected_rate)


# http://www.wikihow.com/Calculate-Weighted-Average
# https://en.wikipedia.org/wiki/Exponential_function with x = 2 and then sort with little modifications
def weighted_exponential_moving_average(window_values):
    # weights = [0.0021, 0.0029, 0.005, 0.01, 0.04, 0.09, 0.13, 0.18, 0.25, 0.29]
    weights = [0.02, 0.02, 0.05, 0.05, 0.08, 0.1, 0.14, 0.16, 0.18, 0.22]
    sum = 0
    for x in range(0, noOfMachines):
        sum += window_values[x] * weights[x]
    ema0 = sum / noOfMachines
    alpha = int(2 / (noOfMachines + 1))
    expected_rate = (alpha * noOfMachines + (1 - alpha) * ema0) * 10 + 10
    return int(expected_rate)


'''
if __name__ == '__main__':
    # print exponential_moving_average([114, 120, 100, 130, 150, 140, 111, 100, 120, 125])
    # print weighted_exponential_moving_average([114, 120, 100, 130, 150, 140, 111, 100, 120, 125])
    # print exponential_moving_average([150, 150, 150, 150, 150, 150, 150, 150, 150, 150])
    # print weighted_exponential_moving_average([150, 150, 150, 150, 150, 150, 150, 150, 150, 150])
    # print exponential_moving_average([900, 950, 980, 920, 990, 910, 940, 960, 950, 980])
    # print weighted_exponential_moving_average([900, 950, 980, 920, 990, 910, 940, 960, 950, 980])
    print(exponential_moving_average([1050, 985, 1011, 1030, 967, 1010, 958, 1005, 1009, 1004]))
    print(weighted_exponential_moving_average([1050, 985, 1011, 1030, 967, 1010, 958, 1005, 1009, 1004]))

'''
