import numpy as np
import matplotlib.pyplot as plt
from waveform_design_lib import *
from scipy.io import loadmat #loadmat("can_test.mat")

# #----------------------------------#
# # normalize:
# M=5
# N=10
# # S = np.zeros((M, N)).astype(np.csingle)

# # for m in range(M):
# #     for n in range(N):
# #         S[m][n] = np.random.uniform(low=-5,high=5)+1j*np.random.uniform(low=-5,high=5)
# S = np.ones((5, 10))*1
# print(S)
# for sig in S:
#     energy = np.vdot(sig,sig)
#     print(f"signal energy: {energy}")
#     assert not energy == 1, "Energy should not be normalized"

# S_norm = normalize(S)
# print("Supposedly normalized:")
# print(S_norm)
# for sig in S_norm:
#     energy = np.vdot(sig,sig)
#     print(f"signal energy: {energy}")
#     epsilon = 1e-6
#     assert np.abs(1-energy) < epsilon, "Energy should be normalized"
# #----------------------------------#

#----------------------------------#
# round_bits
# max = 8
# min = -7
# S1 = np.array([
#     [1 for x in range(min,max+1)],
#     [-1 for x in range(min,max+1)],
#     [1j*x for x in range(min,max+1)],
#     [2*x+2j*x for x in range(min,max+1)],
#     [x for x in range(min,max+1)]
# ])
# print(round_bits(S1, B=4))

#multican:
# data = loadmat("can_test.mat")
# matlab_opt_sigs = np.transpose(data["Xcan"])
# X0 = data["X0"]
# print("running")
# python_opt_sigs = np.transpose(multican(20,5,X0=X0))
# print("done!")
# print(matlab_opt_sigs-python_opt_sigs)

# for m in range(5):
#     plot_2_cplx(matlab_opt_sigs[m],python_opt_sigs[m],20)

# corr_plot(matlab_opt_sigs, "Matlab CAN")
# corr_plot(python_opt_sigs, "Python CAN")

