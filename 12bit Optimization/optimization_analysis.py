import math
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io.wavfile
import os, sys
import datetime
os.chdir(sys.path[0])
from optimizationV2_12bit import preamble_optimization

# Set the default font size globally
rcParams['font.size'] = 24  # You can adjust the value to your preference


# Load in files
# ====================================================== #
M = 6
N = 200
timestamp = "2024-02-03_21-09-07"  # Replace with the timestamp from your files
pareto_filename = f"pareto-signals_M{M}-N{N}_{timestamp}.npy"
optimization_filename = f"optimization-data_{timestamp}.npy"

# Load the files
pareto_set = np.load(pareto_filename)
optimization_history = np.load(optimization_filename)

# Normalize the set
norm_pareto_set = np.copy(pareto_set.astype(np.float64))
for i in range(len(norm_pareto_set)):
    for j in range(len(norm_pareto_set[i])):
        sig = norm_pareto_set[i][j]
        norm_pareto_set[i][j] = sig / np.linalg.norm(sig)


# ====================================================== #

# Pareto analysis
# ====================================================== #
dummy_opt = preamble_optimization(M, N)
# form (worst_autocorr, worst_crosscorr)
pareto_data = [(-1*dummy_opt.autocorr_obj_fn(Si), dummy_opt.crosscorr_obj_fn(Si)) for Si in pareto_set]
# ====================================================== #
# rcParams['font.family'] = 'Liberation Sans'
# Create a Scatter plot to visualize the Pareto front
min_autocorr, max_crosscorr = zip(*pareto_data)
plt.scatter(min_autocorr, max_crosscorr)
plt.xlabel("min of max autocorrelation")
plt.ylabel("max of min cross-correlation")
plt.title("Pareto Front")
for i, (x, y) in enumerate(zip(min_autocorr, max_crosscorr)):
    plt.annotate(str(i), (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
plt.grid()
plt.show()

def plot_many(rows, cols, horiz_axis, data, main_title, x_label, y_label, plot_titles):

    for i in range(len(data)):
        plt.subplot(rows, cols, i+1)
        plt.stem(horiz_axis, data[i])
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(plot_titles[i])
    plt.suptitle(main_title)
    
    
    # ax.grid()
    # ax.set(xlabel='Sample [n]', ylabel='Autsocorrelation', tile=title)
    plt.show()

#Plot Normalized Signal info
#pareto set member:
k = 1

norm_autocorr = [signal.correlate(Sn, Sn) for Sn in norm_pareto_set[k]]

plot_many(2, 3, range(0, N), norm_pareto_set[k],  f"Pereto Signal Set {k} (normalized energy)", "sample index", 'Sample amplitude', [f"Signal {i}" for i in range(M)])

plot_many(2, 3, range(0, 2*N-1), norm_autocorr, f"Normalized Autocorrelation for Pareto Set {k}", "Lag", "Autocorrelation", [f"Autocorrelation of Signal {i}" for i in range(M)])

norm_xcorrs = []
xcorr_subtitles = []
for i in range(M):
    # start at i so we don't repeat unnecessary operations
    # Add 1 so we don't find autocorrelation.
    for j in range(i+1, M):
        xcorr_subtitles.append(f"Cross-correlation Between Signals {i} and {j}")
        norm_xcorrs.append(signal.correlate(norm_pareto_set[k][i], norm_pareto_set[k][j]))

#         x *y = (M^2-m)/2 (think matrices)
plot_many(5, 3, range(0, 2*N-1), norm_xcorrs, f"Normalized Crosscorrelations for Pareto Set {k}", "Lag", "Cross-correlation", xcorr_subtitles)

# 1. Evolution of auto and cross correction for
#    each member of each generation as scatter plot

optimization_history_coords = np.empty([len(optimization_history), 2, len(optimization_history[0])])
# print(testing1)
for i in range(len(optimization_history)):
    optimization_history_coords[i][0] = [pt[0] for pt in optimization_history[i]]
    optimization_history_coords[i][1] = [pt[1] for pt in optimization_history[i]]

print(optimization_history_coords)
# Create a color map that transitions from one color to another
# colors = np.arange(len(optimization_history))

# Create a scatter plot
generations = np.repeat(np.arange(len(optimization_history)), len(optimization_history[0]))
plt.scatter(optimization_history.flatten()[::2], optimization_history.flatten()[1::2], s=2, c=generations, cmap='viridis', marker='o')
# Add color bar
plt.colorbar(label='Generation')

# Set labels and title
plt.xlabel('Rho Values')
plt.ylabel('Alpha Values')
plt.title('Scatter Plot with Color Transition')

# Show the plot
plt.show()