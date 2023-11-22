import numpy as np
from scipy import fft, signal, constants

import matplotlib as mpl
import matplotlib.pyplot as plt

# sample frequency
Fs = 10e6
# sample period
Ts = 1/Fs 
# 40uS symbol period
T_sig = 45e-6 
# number of signals to optimize
M = 6

# number of points per signal
N = int(T_sig/Ts)
S = np.random.rand(M, N)

def plot_many(rows, cols, horiz_axis, data, title=''):

    for i in range(1, len(data)+1):
        plt.subplot(rows, cols, i)
        plt.stem(horiz_axis, data[i-1])
        print(i)
    
    # ax.grid()
    # ax.set(xlabel='Sample [n]', ylabel='Autocorrelation', tile=title)
    plt.show() 

autocorr = [signal.correlate(Sn, Sn) for Sn in S]

# plot_many(2, 3, range(0, N), S, 'Signals')
# plot_many(2, 3, range(0, 2*N-1), autocorr, 'Autocorrelation of each signal')


#objective 1: thumbtack-like autocorrelation    
    

# plt.plot(range(0, 2*N-1), delta, color='r')
# plt.plot(range(0, 2*N-1), autocorr[0], color='g')
# plt.show() 