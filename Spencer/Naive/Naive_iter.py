
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
import csv
import os, sys
os.chdir(sys.path[0])

from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

class preamble_optimization1(Problem):
    def __init__(self, M, N):
        
        # number of samples per signal
        self.N = N 
        # of signals to optimize
        self.M = M

        super().__init__(n_var=M*N, n_obj=2, xl=-1, xu=1, elementwise_evaluation=True)

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

        out["F"] = np.array(gen_results)

def plot_many(rows, cols, horiz_axis, data, title, x_label, y_label):

    for i in range(1, len(data)+1):
        plt.subplot(rows, cols, i)
        plt.stem(horiz_axis, data[i-1])
        # plt.xlabel(x_label)
        # plt.ylabel(y_label)
        # plt.title(title)
        #print(i)
    
    # ax.grid()
    # ax.set(xlabel='Sample [n]', ylabel='Autocorrelation', tile=title)
    plt.show()



# sample frequency
Fs = 10e6
# sample period
Ts = 1/Fs 
# 40uS symbol period
T_sig = 45e-6 
# number of samples per signal
N = int(T_sig/Ts)
# Create a CSV file to store timing data
with open("timing_data.csv", mode='w', newline='') as csv_file:
    fieldnames = ['M', 'Execution Time (seconds)']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader() # Write header

#Ask to perform 5x loop for timing pts to avg
timingcheck=False
response = input( "Averaging timing check? (y/n): ").lower()
if response =="y":
    timingcheck=True
elif response =="n":
    timingcheck=False
else:
    print("Invalid entry, skipping averaging timing check")
    timingcheck=False

for _ in range(5): # Repeat the while loop 5 times, collect 25 timing data pts
    M = 4  # Reset M for each iteration, start @ 4   
    while M <= 64: #Loop 5 times (M = 2^2 to 2^6)
        start_time = time.time()
        print(f"M={M}")

        # Create an instance of the optimization problem
        problem = preamble_optimization1(M, N)

        # Choose the optimization algorithm (NSGA-II in this case)
        algorithm = NSGA2(pop_size=20)

        # Perform the optimization
        result = minimize(problem, algorithm)

        # Access the optimal solution
        #print(len(result.X))
        optimal_signal_set = np.array(np.reshape(result.X, (M, N))) 

        #Save execution time
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for M={M}: {execution_time} seconds")
        with open("timing_data.csv", mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'M': M, 'Execution Time (seconds)': execution_time})



        #print(len(optimal_signal_set))
        np.savetxt(f"optimal_{M}signals.txt", optimal_signal_set)

        #Visualization
        ##autocorr = [signal.correlate(Sn, Sn) for Sn in optimal_signal_set]
        ##plot_many(9, 9, range(0, N), optimal_signal_set, 'Optimal signal set', 'sample number', 'sample value')
        ##plot_many(9, 9, range(0, 2*N-1), autocorr, 'Autocorrelation of each signal', 'Time Lag', 'Autocorrelation of Signal ')
        ##xcorr = [signal.correlate(optimal_signal_set[0], optimal_signal_set[i]) for i in range(0,M)]
        ##plot_many(9, 9, range(0, 2*N-1), xcorr, 'Autocorrelation of each signal', 'Time Lag', 'Autocorrelation of Signal ')
        #print(np.corrcoef(optimal_signal_set))

        
        M = M*2 #iter (2^n)
    if timingcheck== False:
        break
