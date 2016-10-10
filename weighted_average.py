import numpy as np
from numpy import convolve
#import matplotlib.pyplot as plt
 
def movingaverage (values, window):
    #weights = np.repeat(1.0, window)/window
    weights = [0.06, 0.07, 0.08, 0.09, 0.1, 0.1, 0.11, 0.12, 0.13, 0.14]
    #print('weights = ', weights)
    sma = np.convolve(values, weights, 'valid')
    return sma[0]