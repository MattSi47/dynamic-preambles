import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from waveform_design_lib import *
from paretoset import paretoset
from matplotlib import cm


# def ambibuity_fn(filter, sig, B, freqs)
B = 5e6
T = 40e-6
upchirp = chirp_fn(T,B,-50e3,50e3)
downchirp = chirp_fn(T,B,50e3,-50e3)

# plot_corr(upchirp,upchirp,"UC","UC","Autocorrelation of upchirp function")
# plot_corr(upchirp,downchirp,"UC","DC","Autocorrelation of upchirp function")

# plot_complex(upchirp, "chirp fn")
# plot_complex(downchirp, "chirp fn")


n_freqs = 500
f_max = 70e3
f_step = f_max/n_freqs
CFO_freqs = np.array(range(n_freqs,-n_freqs+1,-1))*f_step

# plot_ambiguity(upchirp, upchirp, B, CFO_freqs, title="LFM Chirp")
# plot_ambiguity(upchirp, downchirp, B, CFO_freqs, title="CAF LFM Up and Down Chirp")

# naive = np.ones(round(B*T))
# # plot_ambiguity(naive, naive, B, CFO_freqs, "Naive Pulse Ambiguity Function")

# Designed CAN Signals:
S_MC = np.load("./new/numpy_files/multican_montecarlo_1k_sigs.npy")

S_MC_rounded = [normalize_set(round_bits(S, 12)) for S in S_MC]

# Choose set 864
pts_round = gen_obj_scatter_pts(S_MC_rounded)
plot_pareto_scatter(pts_round)

S = normalize_set(S_MC[864])

# plot_ambiguity(S[0],S[0], B, CFO_freqs, plot_3D=False, title="Signal 0")
corr_plot(S, "Signal Set 864 Correlations")
plot_pareto_scatter(pts_round)
# plot_ambiguity_triangle(S, B, CFO_freqs, title="Signal Set 864 Ambiguity")

print(f"Set 864 max AC: {max_ac_sidelobe(S)}")
print(f"Set 864 max CC: {max_cc_val(S)}")

# plot_corr(S[0],S[0],"0","0","Autocorrelation of Preamble 0")
print(np.shape(S))
print(f"PSL of 0, 0 {psl(S,0,0,S_is_normalized=True)}")
# for m in range(len(S)):
#     for m2 in range(m, len(S)):
#         if m == m2:
#             title_ = f"Signal {m} AF"
#         else:
#             title_ = f"Signals {m} and {m2} CAF"
#         plot_ambiguity(S[m],S[m2], B, CFO_freqs, title=title_, plot_3D=False, display=True)

preamble_set_out(S_MC[864], "SigSet864_MonteCarlo1k")