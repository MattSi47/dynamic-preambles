import numpy as np
from scipy.io import loadmat 
# import h5py

# with h5py.File('montecarlo_10k_trials.mat', 'r') as file:
#     # Assuming the arrays are named 'array1' and 'array2'
#     sig_sets = file['sig_sets'][:]
#     inits = file['X0_mat'][:]

data = loadmat("./new/mat_files/multican_montecarlo_1k.mat")
sig_sets = data["sig_sets"]
inits = data['init_sets']

# form: sig_sets_[K][M][N]


np.save("./new/numpy_files/multican_montecarlo_1k_sigs.npy", sig_sets)
np.save("./new/numpy_files/multican_montecarlo_1k_inits.npy", inits)