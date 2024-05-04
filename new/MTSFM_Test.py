import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from waveform_design_lib import *
from paretoset import paretoset
from matplotlib import cm

T = 40e-6
B = 5e6
N = round(T*B)

a = [10, 1]
b = [0, 0]
freqs = [100e3, 200e3]
MTSFM = mtsfm_generator(a, b, freqs, B, N)

plot_complex(MTSFM)