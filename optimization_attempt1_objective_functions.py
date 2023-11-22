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
S = [np.random.uniform(-1, 1, N) for _ in range(M)]

# want to maximize this:
# delta = [0 if i != int((2*N-1)/2) else 1 for i in range(0, 2*N-1)]

delta = np.where(np.arange(2 * N - 1) != int((2 * N - 1) / 2), 0, 1)
def autocorr_obj_fn(sigs=S):
    sig_ac = [signal.correlate(Sn, Sn) for Sn in S]
    return min([np.corrcoef(sig_ac_n, delta) for sig_ac_n in sig_ac])

# want to minimize this:
# find max cross corellation between 2 signals
def crosscorr_obj_fn(sigs=S):
    l = len(sigs)
    crosscorrs = np.full((l, l), -2) # 2 is out of bounds of corr. coeff
    masked_crosscorrs = np.ma(crosscorrs, mask=-2*np.identity(l))

    for i in range(0, l):
        # start at i so we don't repeat unnecessary operations
        # Add 1 so we don't find autocorrelation coefficient which is always 1.
        for j in range(i+1, l):
            rho = np.corrcoef(sigs[i], sigs[j])
            crosscorrs[i][j] = rho
            crosscorrs[j][i] = rho
        return max(masked_crosscorrs)