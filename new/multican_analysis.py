import numpy as np
import matplotlib.pyplot as plt
from waveform_design_lib import *
from paretoset import paretoset



S_MC = np.load("./new/numpy_files/multican_montecarlo_1k_sigs.npy")
pts = gen_obj_scatter_pts(S_MC)
plot_pareto_scatter(pts)

S_MC_rounded = [round_bits(S, 2) for S in S_MC]
pts_round = gen_obj_scatter_pts(S_MC_rounded)
plot_pareto_scatter(pts_round)

print(f"out: {S_MC_rounded[0]}")
