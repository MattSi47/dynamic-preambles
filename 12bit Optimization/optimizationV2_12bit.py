from datetime import datetime
import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import rcParams
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

class preamble_optimization(Problem):
    def __init__(self, M, N):
        
        # number of samples per signal
        self.N = N 
        # of signals to optimize
        self.M = M
        
        super().__init__(n_var=M*N, n_obj=2, xl=-2048, xu=2047, vtype=int, elementwise_evaluation=True)

        # of form:
        # [
        #     [beta1, alpha1, beta2, alpha2,..], #gen 0
        #     [beta1, alpha1, beta2, alpha2,..], #gen 1
        #     ...
        # ]
        self.data = np.array([], dtype=np.float64)
        self._gen_num = 0
    # want to maximize the minimum "spikiness" of autocorrelation:
    # negate result to make it a minimization
    def autocorr_obj_fn(self, S):
        norm_S = [Sn / np.sqrt(np.sum(np.square(Sn))) for Sn in S]
        sig_ac_sorted = [sorted(signal.correlate(Sn, Sn), reverse=True) for Sn in norm_S]
        # maximize distance between largest and second largest value
        min_alpha = min([sorted_list[0]-sorted_list[1] for sorted_list in sig_ac_sorted])
        return -min_alpha
    
    # want to minimize the maximum cross correlation between 2 signals:
    def crosscorr_obj_fn(self, S):
        # looks like no issues with type conversion here.
        S_norms = [Sn / np.sqrt(np.sum(np.square(Sn))) for Sn in S]
        max_crosscorr = []
        for i in range(0, self.M):
            # start at i so we don't repeat unnecessary operations
            # Add 1 so we don't find autocorrelation.
            for j in range(i+1, self.M):
                max_xcorr = signal.correlate(S_norms[i], S_norms[j]).max()
                max_crosscorr.append(max_xcorr)
        max_max_xcorr = max(max_crosscorr)
        return max_max_xcorr

    # Calls evaluation function on each generation of results, outputs those results
    # S_new_gen_flat_array has dimensions (num designs per gen) x (M*N)
    def _evaluate(self, S_new_gen_flat_array, out, *args, **kwargs):
        #Array of entire generation of M x N array of signal row vectors
        S_generation = np.array([np.reshape(Si, (self.M, self.N)) for Si in S_new_gen_flat_array])
        gen_results = []
        self.data.append([])
        for Si in S_generation:

            worst_autocorr = self.autocorr_obj_fn(Si)
            worst_crosscorr = self.crosscorr_obj_fn(Si)
            
            #undo the (-) to make it a maximin from the minimax
            self.data[self._gen_num].append([-worst_autocorr, worst_crosscorr])
            gen_results.append([worst_autocorr, worst_crosscorr])

        self._gen_num += 1
        out["F"] = np.array(gen_results)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    # sample frequency
    Fs = 5e6
    # sample period
    Ts = 1/Fs 
    # 40uS symbol period
    T_sig = 40e-6 
    # number of signals to optimize
    M = 6
    # number of samples per signal
    N = int(T_sig/Ts)
    # Create an instance of the optimization problem
    problem = preamble_optimization(M, N)


    # Choose the optimization algorithm (NSGA-II in this case)
    algorithm = NSGA2(
        pop_size=500,
        sampling=IntegerRandomSampling(),
        crossover=SBX(prob=1.0, eta=3.0, vtype=int, repair=RoundingRepair()),
        mutation=PM(prob=1.0, eta=3.0, vtype=int, repair=RoundingRepair())
    )

    # Perform the optimization
    result = minimize(problem, algorithm)

    pareto_set = np.array([np.array(np.reshape(sig_set, (M, N))) for sig_set in result.X])
    optimization_history = np.array(problem.data)

    #save data set
    timestamp = datetime.datetime.now()
    format_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    np.save(f"pareto-signals_M{M}-N{N}_{format_timestamp}.npy", pareto_set)
    np.save(f"optimization-data_{format_timestamp}.npy", optimization_history)