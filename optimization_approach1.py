import numpy as np

from scipy import constants
# sample frequency
Fs = 10e6
# sample period
Ts = 1/Fs 
# 40uS symbol period
T_sig = 40e-6 
# number of signals to optimize
K = 5

# number of points per signal
N = T_sig/Ts

