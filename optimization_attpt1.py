import numpy as np
from scipy import signal

from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.optimize import minimize

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


class preamble_optimization1(Problem):
    def __init__(self, Fs, T_sig, M):
        # sample period
        self.Ts = 1/Fs
        # total time for each signal
        self.T_sig = T_sig
        # number of samples per signal
        N = int(T_sig/Ts)
        # of signals to optimize
        self.M = M

        super().__init__(n_var=M*N, n_obj=2, xl=-1, xu=1, elementwise_evaluation=True)

        self._delta = np.where(np.arange(2 * N - 1) != int((2 * N - 1) / 2), 0, 1)

    # want to maximize the minimum "spikiness" of autocorrelation:
    # negate result to make it a minimization
    def autocorr_obj_fn(self, S):
        sig_ac = [signal.correlate(Sn, Sn) for Sn in S]
        return -min([np.corrcoef(sig_ac_n, self.delta) for sig_ac_n in sig_ac])

    # want to minimize the maximum cross corellation between 2 signals:
    def crosscorr_obj_fn(self, S):
        crosscorrs = np.full((self.M, self.M), -2) # 2 is out of bounds of corr. coeff
        # ignore the autocorrelation terms which = 1
        masked_crosscorrs = np.ma(crosscorrs, mask=-2*np.identity(self.M))

        for i in range(0, self.M):
            # start at i so we don't repeat unnecessary operations
            # Add 1 so we don't find autocorrelation coefficient which is always 1.
            for j in range(i+1, self.M):
                rho = np.corrcoef(self.S[i], self.S[j])
                crosscorrs[i][j] = rho
                crosscorrs[j][i] = rho
            return max(masked_crosscorrs)
    
    # Calls evaluation function on each generation of results, outputs those results
    # S_new_gen_flat_array has dimensions (num designs per gen) x (M*N)
    def _evaluate(self, S_new_gen_flat_array, out, *args, **kwargs):
        #Array of entire generation of M x N array of signal row vectors
        S_generation = np.array([np.reshape(Si, (self.M, N)) for Si in S_new_gen_flat_array])
        gen_results = []
        for S in S_generation:
            gen_results.append([self.autocorr_obj_fn(S), self.crosscorr_obj_fn(S)])

        out["F"] = np.array(gen_results)

# sample frequency
Fs = 10e6
# sample period
Ts = 1/Fs 
# 40uS symbol period
T_sig = 45e-6 
# number of signals to optimize
M = 6

# Create an instance of the optimization problem
problem = preamble_optimization1(Fs, T_sig, M)

# Choose the optimization algorithm (NSGA-II in this case)
algorithm = NSGA2()

# Perform the optimization
result = minimize(problem, algorithm)

# Access the optimal solution
optimal_signal = result.X

# Print the result
print("Optimal Signal:", optimal_signal)