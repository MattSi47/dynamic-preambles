import numpy as np
import matplotlib.pyplot as plt
import tftb as tftb
from mpl_toolkits.mplot3d import Axes3D
import tftb.processing.ambiguity
from waveform_design_lib import *
from paretoset import paretoset
from matplotlib import cm

S_MC = np.load("./new/numpy_files/multican_montecarlo_1k_sigs.npy")

S_MC_rounded = [normalize_set(round_bits(S, 12)) for S in S_MC]

S = S_MC_rounded[864]

af = ambiguity_fn(S[0],S[0],range(-100**3, 0, 1000),5e6)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Grab some test data.
# X, Y, Z = Axes3D.get_test_data(0.05)

# Plot a basic wireframe.
ax.plot_wireframe(np.array(range(len(af))), np.array(len(af[0])), af, rstride=10, cstride=10)

plt.show()