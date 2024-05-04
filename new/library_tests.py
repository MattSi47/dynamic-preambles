import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from waveform_design_lib import *
from paretoset import paretoset
from matplotlib import cm

M = 5
N = 10
rng = np.random.default_rng()

S_test = (rng.random((M,N))+1j*rng.random((M,N)))*10
# print(S_test)
def normalize(sig):
    #mag = np.sqrt(np.vdot(sig,sig))
    mag = np.linalg.norm(sig)
    return sig/mag

def normalize_set_(S_in):
    S_norm = np.zeros((len(S_in),len(S_in[0])))
    for m in range(len(S_in)):
        S_norm[m] = normalize(S_in[m])
        # print(f"from norm set: {np.linalg.norm(S_norm[m])}")
    return S_norm
    # return np.array([normalize(sig) for sig in S_in])


print("Using normalize_set")
S_norm1 = normalize_set(S_test)
# print(S_norm1)
for Si in S_norm1:
    print(np.linalg.norm(Si))

# print()
# print()
# print("Using normalize")
# S_norm2 = [normalize(Si) for Si in S_test]
# for Si in S_norm2:
#     print(np.linalg.norm(Si))

# print()
# print()
# print("copied version of normalize_set")

# S_norm3 = np.zeros((len(S_test),len(S_test[0])))

# for m in range(len(S_test)):
#     S_norm3[m] = normalize(S_test[m])
# print(S_norm3)
# for Si in S_norm2:
#     print(np.linalg.norm(Si))

# plot_corr(S_test,S_test,"S","S","not normalized")

# S_test_norm = normalize(S_test)
# new_norm = np.vdot(S_test_norm, S_test_norm)
# print(f"After normalizing: {new_norm}")

# plot_corr(S_test_norm,S_test_norm,"S","S","normalized")