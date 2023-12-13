
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import scipy.io.wavfile
import os, sys
import datetime
os.chdir(sys.path[0])

from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
#issue: original optimization used nearly unlimited precision. Here we limit to 12 bit integers (-2048 to 2047)

class preamble_optimization1(Problem):
    def __init__(self, M, N):
        
        # number of samples per signal
        self.N = N 
        # of signals to optimize
        self.M = M
        
        super().__init__(n_var=M*N, n_obj=2, xl=-2048, xu=2047, vtype=int, elementwise_evaluation=True)

        self._delta = np.where(np.arange(2 * N - 1) != int((2 * N - 1) / 2), 0, 1)

    # want to maximize the minimum "spikiness" of autocorrelation:
    # negate result to make it a minimization
    def autocorr_obj_fn(self, S):
        sig_ac = [signal.correlate(Sn, Sn) for Sn in S]
        # Select diagonal element of 2x2 corr. matrix fro cross correlation
        return -min([np.corrcoef(sig_ac_n, self._delta)[0][1] for sig_ac_n in sig_ac])

    # want to minimize the maximum cross corellation between 2 signals:
    def crosscorr_obj_fn(self, S):
        crosscorrs = np.full((self.M, self.M), -2) # 2 is out of bounds of corr. coeff
        # ignore the autocorrelation terms which = 1
        masked_crosscorrs = np.ma.masked_array(crosscorrs, mask=-2*np.identity(self.M))

        for i in range(0, self.M):
            # start at i so we don't repeat unnecessary operations
            # Add 1 so we don't find autocorrelation coefficient which is always 1.
            for j in range(i+1, self.M):
                rho = np.corrcoef(S[i], S[j])[0][1]
                crosscorrs[i][j] = rho
                crosscorrs[j][i] = rho
        return np.max(masked_crosscorrs)
    
    # Calls evaluation function on each generation of results, outputs those results
    # S_new_gen_flat_array has dimensions (num designs per gen) x (M*N)
    def _evaluate(self, S_new_gen_flat_array, out, *args, **kwargs):
        #Array of entire generation of M x N array of signal row vectors
        S_generation = np.array([np.reshape(Si, (self.M, N)) for Si in S_new_gen_flat_array])
        gen_results = []
        for S in S_generation:
            gen_results.append([self.autocorr_obj_fn(S), self.crosscorr_obj_fn(S)])
            # rounded_S = np.round(S).astype(int)  # Round to the nearest integer
            # gen_results.append([self.autocorr_obj_fn(rounded_S), self.crosscorr_obj_fn(rounded_S)])

            #print(S)
        out["F"] = np.array(gen_results)


# sample frequency
Fs = 10e6
# sample period
Ts = 1/Fs 
# 40uS symbol period
T_sig = 45e-6 
# number of signals to optimize
M = 4
# number of samples per signal
N = int(T_sig/Ts)
# Create an instance of the optimization problem
problem = preamble_optimization1(M, N)


# Choose the optimization algorithm (NSGA-II in this case)
algorithm = NSGA2(
    pop_size=200,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=1.0, eta=3.0, vtype=float, repair=RoundingRepair())
)

# Perform the optimization
result = minimize(problem, algorithm)

# Access the optimal solution
#print(len(result.X))
optimal_signal_set = np.array(np.reshape(result.X, (M, N))) 
#print(len(optimal_signal_set))

np.savetxt(f"optimal(12bit).txt", optimal_signal_set)

def plot_many(rows, cols, horiz_axis, data, title, x_label, y_label):

    for i in range(1, len(data)+1):
        plt.subplot(rows, cols, i)
        plt.stem(horiz_axis, data[i-1])
        # plt.xlabel(x_label)
        # plt.ylabel(y_label)
        # plt.title(title)
        #print(i)
    
    # ax.grid()
    # ax.set(xlabel='Sample [n]', ylabel='Autsocorrelation', tile=title)
    plt.show()


# wavgen(M,optimal_signal_set)
autocorr = [signal.correlate(Sn, Sn) for Sn in optimal_signal_set]
plot_many(int(math.sqrt(M)), int(math.sqrt(M)), range(0, N), optimal_signal_set, 'Optimal signal set', 'sample number', 'sample value')
plot_many(int(math.sqrt(M)), int(math.sqrt(M)), range(0, 2*N-1), autocorr, 'Autocorrelation of each signal', 'Time Lag', 'Autocorrelation of Signal ')

xcorr = [signal.correlate(optimal_signal_set[0], optimal_signal_set[i]) for i in range(0,M)]

plot_many(int(math.sqrt(M)), int(math.sqrt(M)), range(0, 2*N-1), xcorr, 'Autocorrelation of each signal', 'Time Lag', 'Autocorrelation of Signal ')


#print(np.corrcoef(optimal_signal_set))