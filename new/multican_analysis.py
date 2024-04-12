import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from waveform_design_lib import *
from paretoset import paretoset
from matplotlib import cm


# def ambibuity_fn(filter, sig, B, freqs)
B = 5e6
T = 40e-6
chirp = chirp_fn(T,B,-50e3,50e3)
downchirp = chirp_fn(T,B,50e3,-50e2)
# plot_complex(chirp, "chirp fn")

n_freqs = 1000
f_max = 70e3
f_step = f_max/n_freqs
CFO_freqs = np.array(range(n_freqs,-n_freqs+1,-1))*f_step

#TODO: What are the specs of the chirp we are using
#TODO: Fix 2D CAF plot axis
#TODO: fix correlation
# plot_ambiguity(chirp, chirp, B, CFO_freqs, title="NLFM Chirp")
# plot_ambiguity(chirp, downchirp, B, CFO_freqs, title="CAF NLFM Up and Down Chirp")

# naive = np.ones(round(B*T))
# plot_ambiguity(naive, naive, B, CFO_freqs, "Naive Pulse Ambiguity Function")

# # Designed CAN Signals:
S_MC = np.load("./new/numpy_files/multican_montecarlo_1k_sigs.npy")


S_MC_rounded = [normalize_set(round_bits(S, 12)) for S in S_MC]

pts_round = gen_obj_scatter_pts(S_MC_rounded)
print(f"max_cc_val for 696: {max_cc_val(S_MC_rounded[696])}")
print(f"max_ac_sidelobe for 696: {max_ac_sidelobe(S_MC_rounded[696])}")
# Choose set 240
plot_pareto_scatter(pts_round)

S = S_MC_rounded[696]

corr_plot(S, "Correlations between signals in set #696")

# for m in range(len(S)):
#     for m2 in range(m, len(S)):
#         if m == m2:
#             title = f"Signal {m} AF"
#         else:
#             title_ = f"Signals {m} and {m2} CAF"
#         plot_ambiguity(S[m],S[m2], B, CFO_freqs, title=title_)

preamble_set_out(S_MC[696], "SigSet696_MonteCarlo1k")