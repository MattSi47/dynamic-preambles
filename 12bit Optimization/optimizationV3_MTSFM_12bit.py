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
# from pymoo.visualization.scatter import Scatter

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
# from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import FloatRandomSampling

class preamble_optimization(Problem):
    def __init__(self, M, N):
        
        # number of samples per signal
        self.N = round(N)
        # of signals to optimize
        self.M = round(M)
        
        # num coeffs per signal
        self.K = round(np.floor(N/2))
        super().__init__(n_var=2*self.K*self.M, n_obj=2, xl=-10, xu=10, vtype=float, elementwise_evaluation=True)

        # of form:
        # [
        #     [[max_ISL1, max_max_crosscorr1], [max_ISL2, max_max_crosscorr1], ...], #gen 0
        #     [[max_ISL1, max_max_crosscorr1], [max_ISL2, max_max_crosscorr1], ...], #gen 1
        #     ...
        # ]

        self.data = []
        self._gen_num = 0
    # want to maximize the minimum "spikiness" of autocorrelation:
    # negate result to make it a minimization

    #generates waveform for ONE signal set worth of coefficients   
    def gen_waveforms(self, a_mat, b_mat):
        # print(f'shape of b_mat: {np.shape(b_mat)}')
        n = np.linspace(0, self.N-1, self.N)
        phi = 0*n
        signals = np.zeros((self.M, self.N), dtype='complex_')
        for m in range(0, self.M):
            #vectors of a_k and b_k coeffs
            a_vec = a_mat[m]
            b_vec = b_mat[m]
            
            phi_m = np.zeros(self.N)

            for k in range(1, self.K+1):
                factor = self.N/(2*np.pi*k)
                # arrays are 0-based
                alpha = a_vec[k-1]*factor
                beta = b_vec[k-1]*factor

                phi_m = phi + alpha*np.sin(2*np.pi*k*n/self.N) - beta*np.cos(2*np.pi*k*n/self.N)
            # emulate 12 bit system (plus or minus 2048 max)
            s_m_tilde = np.round(2047 * np.exp(1j*2*np.pi * phi_m))
            #normalize to unit energy for conveniance
            signals[m] = s_m_tilde/np.sqrt(np.sum(np.square(np.abs(s_m_tilde))))
        
        return signals

    # Want to minimize the max ISR
    def ISL_obj_fn(self, signals):
        signals_AC = [signal.correlate(s_m, s_m) for s_m in signals]
        #location of mainlobe at max AC value:
        ISLs = []
        for m in range(self.M):
            ACmag_m = np.abs(signals_AC[m])

            ISL_acc = 0
            for l in range(self.N-1, 2*self.N-1):
                ISL_acc = ISL_acc + ACmag_m[l]
            
            ISLs.append(ISL_acc)
        return max(ISLs)
    
    # want to minimize the maximum cross correlation between 2 signals:
    def crosscorr_obj_fn(self, signals):
        # looks like no issues with type conversion here.
        #S_norms = [Sn / np.sqrt(np.sum(np.square(Sn))) for Sn in S]
        max_crosscorr = []
        for i in range(0, self.M):
            # start at i so we don't repeat unnecessary operations
            # Add 1 so we don't find autocorrelation.
            for j in range(i+1, self.M):
                max_xcorr = signal.correlate(signals[i], signals[j]).max()
                max_crosscorr.append(max_xcorr)
        max_max_xcorr = max(max_crosscorr)
        return max_max_xcorr
    
    def flat_coeffs_to_4D(self, coeff_flat_arr):
        #print(f'length of coeff_flat_arr in flat_coeffs_to_4D = {len(coeff_flat_arr)}, shape = {np.shape(coeff_flat_arr)}')
        #print(f'num coeffs per set in flat_coeffs_to_4D = {len(coeff_flat_arr[0])}')

        # J x M x 2K arrays of coefficients for all signal sets within generation
        generation_coeffs = [np.array(np.reshape(coeff_set, (round(self.M), 2*self.K))) for coeff_set in coeff_flat_arr]
        #print(f'Shape of generation_coeffs in flat_coeffs_to_4D: {np.shape(generation_coeffs)}')
        
        coeffs = [np.hsplit(coeff_set, 2) for coeff_set in generation_coeffs]
        #print(f'coeffs shape in flat_coeffs_to_4D: {np.shape(coeffs)}')
        # J x M x K
        generation_A_mat = []
        generation_B_mat = []

        for coeff_set in coeffs:
            generation_A_mat.append(coeff_set[0])
            generation_B_mat.append(coeff_set[1])

        # dimensions: 2 x J x M x K
        return([generation_A_mat,generation_B_mat])
    
    # TODO: FIX
    # Calls evaluation function on each generation of results, outputs those results
    # coeff_flat_arr has dimensions (num designs per gen) x (2*K)
    def _evaluate(self, coeff_flat_arr, out, *args, **kwargs):
        # print(f'length of coeff_flat_arr = {len(coeff_flat_arr)}, shape = {np.shape(coeff_flat_arr)}')
        # print(f'num coeffs per set = {len(coeff_flat_arr[0])}')

        # # J x M x 2K arrays of coefficients for all signal sets within generation
        # generation_coeffs = [np.array(np.reshape(coeff_set, (round(self.M), 2*self.K))) for coeff_set in coeff_flat_arr]
        # print(f'Shape of generation_coeffs in _evaluate: {np.shape(generation_coeffs)}')
        
        # coeffs = [np.hsplit(coeff_set, 2) for coeff_set in generation_coeffs]
        # print(f'coeffs shape: {np.shape(coeffs)}')
        # # J x M x K
        # generation_A_mat = []
        # generation_B_mat = []

        # for coeff_set in coeffs:
        #     generation_A_mat.append(coeff_set[0])
        #     generation_B_mat.append(coeff_set[1])

        generation_all_coeffs = self.flat_coeffs_to_4D(coeff_flat_arr)
        #print(f'Shape of generation_all_coeffs in _evaluate: {np.shape(generation_all_coeffs)}')
        generation_A_mat = generation_all_coeffs[0]
        generation_B_mat = generation_all_coeffs[1]
        

        #print(f'Shape of generation_B_mat in _evaluate: {np.shape(generation_B_mat)}')
        gen_results = []
        self.data.append([])

        #print(len(generation_all_coeffs))

        for j in range(len(generation_all_coeffs[0])):
            signal_set = self.gen_waveforms(generation_A_mat[j], generation_B_mat[j])
            max_ISL = self.ISL_obj_fn(signal_set)
            max_max_crosscorr = self.crosscorr_obj_fn(signal_set)
            self.data[self._gen_num].append([max_ISL, max_max_crosscorr])
            gen_results.append([max_ISL, max_max_crosscorr])
        print(self._gen_num)
        self._gen_num += 1
        #print(f'shape of gen_results: {np.shape(gen_results)}')
        out["F"] = np.array(gen_results)

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    # sample frequency
    Fs = 4e6
    # sample period
    Ts = 1/Fs 
    # 40uS symbol period
    T_sig = 40e-6 
    # number of signals to optimize
    M = 4
    # number of samples per signal
    N = int(T_sig/Ts)
    # Create an instance of the optimization problem
    problem = preamble_optimization(M, N)


    # Choose the optimization algorithm (NSGA-II in this case)
    algorithm = NSGA2(
        pop_size=25,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=1.0, eta=3.0, vtype=float),
        mutation=PM(prob=1.0, eta=3.0, vtype=float)
    )

    # Perform the optimization
    result = minimize(problem, algorithm)

    pareto_set = np.array(result.X)
    optimization_history = np.array(problem.data)

    #save data set
    timestamp = datetime.datetime.now()
    format_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    np.save(f"opt_signals/pareto-signals_M{M}-N{N}_{format_timestamp}.npy", pareto_set)
    np.save(f"opt_signals/optimization-data_{format_timestamp}.npy", optimization_history)