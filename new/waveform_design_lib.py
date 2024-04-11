import numpy as np
from scipy import signal
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from paretoset import paretoset
from adjustText import adjust_text

#### Signal modification tools ####
def xcorr(x, y):
    corr = signal.correlate(x, y, mode='full', method='fft')
    return np.abs(corr)

def normalize(S):
    S_norm = np.zeros_like(S)
    for m in range(len(S)):
        energy = np.vdot(S[m],S[m])
        S_norm[m] = S[m]/np.sqrt(energy)
    return S_norm

# Treat Im and Re components seperately due to SDR hardware
def round_bits(S, B, S_range_pm1=False):
    S_cplx = S.astype(np.complex64)
    S_re = S_cplx.real.copy()
    S_im = S_cplx.imag.copy()

    # max mag im or re value is 1 for each signal
    if not S_range_pm1:
        for m in range(len(S)):
            S_re_m = S_re[m]
            S_im_m = S_im[m]
            max_re = np.max(np.abs(S_re[m]))
            max_im = np.max(np.abs(S_im[m]))
            sig_max = np.max([max_re, max_im])
            S_re[m] = S_re_m/sig_max
            S_im[m] = S_im_m/sig_max

    min_val = int(-(2**B)/2 + 1)
    max_val = int((2**B)/2)
    discrete_bins = np.array(range(min_val, max_val+1))
    
    
    # print(f"discrete bins: {discrete_bins}")

    S_digitized = np.zeros_like(S)
    for m in range(len(S)):
        S_re_ind = np.digitize(max_val*S_re[m], discrete_bins, right=True)
        S_im_ind = np.digitize(max_val*S_im[m], discrete_bins, right=True)
        # print(f"Real index: {S_re_ind}")
        # print(f"Im index: {S_im_ind}")

        # print(f"Digitized real: {discrete_bins[S_re_ind]}")
        S_re_digitized = discrete_bins[S_re_ind]
        S_im_digitized = discrete_bins[S_im_ind]
        S_digitized[m] = S_re_digitized + 1j*S_im_digitized
        #print(f"Fully digitized: {S_digitized[m]}")
    
    # print(f"returning: {S_digitized}")
    return S_digitized

#### Objective functions and measures ####

# from 10.6 of "Basic Radar Analysis" (2e):
# u is incoming signal, v is filter
def doppler_af_slice(u, v, f_cfo):
    cfo_mod = np.exp(1j*2*np.pi*f_cfo*np.arange(len(u)))
    Fv = np.fft.fft(v)
    Fu_cfo = np.fft.fft(u*cfo_mod)
    AF_cfo_slice = np.abs(np.fft.ifft(Fu_cfo*Fv))
    return np.fft.fftshift(AF_cfo_slice)

def psl(S,i,j, S_is_normalized=False):
    S_=None
    if not S_is_normalized:
        S_ = normalize(S)
    else:
        S_ = S
     
    Rij = np.abs(np.correlate(S[i], S[j], mode='full'))
    
    if i == j:
        middle_index = len(S[i])-1
        Rij[middle_index] = 0

    return max(Rij)

def max_cc_val(S, S_is_normalized=False):
    S_=None
    if not S_is_normalized:
        S_ = normalize(S)
    else:
        S_ = S
    M = len(S_)
    running_max = -1
    # ignore autocorrelations:
    for m in range(1, M):
        for j in range(m+1, M):
            running_max = np.max([psl(S_,m,j,S_is_normalized=True), running_max])
    return running_max

def max_ac_sidelobe(S, S_is_normalized=False):
    S_=None
    if not S_is_normalized:
        S_ = normalize(S)
    else:
        S_ = S
    M = len(S_)

    running_max = -1
    for m in range(M):
        running_max = np.max([psl(S_,m,m,S_is_normalized=True), running_max])
    return running_max

def gen_obj_scatter_pts(S):
    L = len(S)
    ac_pts = np.zeros(L)
    cc_pts = np.zeros(L)
    #[AC, CC]
    for j in range(L):
        ac_pts[j] = max_ac_sidelobe(S[j])
        cc_pts[j] = max_cc_val(S[j])
    return np.array([ac_pts, cc_pts])


#### plotting tools ####

def plot_pareto_scatter(data):
    x_coords = data[0]
    y_coords = data[1]
    highlight_color = "red"

    pareto_pts = paretoset(np.transpose(data), sense=["min", "min"])

    # Create boolean mask for highlight
    pareto_mask = np.zeros_like(x_coords, dtype=bool)
    pareto_mask[pareto_pts] = True

    # Plot non-pareto points
    plt.scatter(x_coords[~pareto_mask], y_coords[~pareto_mask])

    # Plot pareto-optimal points and lines
    pareto_x = x_coords[pareto_mask]
    pareto_y = y_coords[pareto_mask]

    # Sort Pareto points based on x-coordinate
    sort_indices = np.argsort(pareto_x) 
    pareto_x = pareto_x[sort_indices]
    pareto_y = pareto_y[sort_indices]

    plt.scatter(pareto_x, pareto_y, color=highlight_color)
    plt.plot(pareto_x, pareto_y, color=highlight_color)

    # indices of all pareto points:
    pareto_ind = np.where(pareto_mask)[0].tolist()
    # Add index labels
    labels = [plt.text(x_coords[i], y_coords[i], str(i), ha="right", va="top", color="black") for i in pareto_ind]
    adjust_text(labels, force_points=1)

    # Labels and title 
    plt.xlabel("Max autocorrelation sidelobe value")
    plt.ylabel("Max crosscorrelation value")
    plt.title("Pareto analysis of signal sets")

    plt.show()


def plot_complex(complex_signal):
    # Extract real and imaginary parts
    real_part = np.real(complex_signal)
    imaginary_part = np.imag(complex_signal)

    # Create sample indices
    samples = np.arange(len(complex_signal))

    # Plot stacked stem plots for real and imaginary parts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Plot real part
    ax1.plot(samples, real_part, linefmt='b-', markerfmt='bo', basefmt=' ')
    ax1.set_ylabel('Real Part')
    ax1.grid(True)

    # Plot imaginary part
    ax2.stem(samples, imaginary_part, linefmt='r-', markerfmt='ro', basefmt=' ')
    ax2.set_xlabel('Sample Index')
    ax2.set_ylabel('Imaginary Part')
    ax2.grid(True)

    plt.suptitle('Stacked Stem Plots of Real (Blue) and Imaginary (Red) Components')
    plt.show()


def corr_plot(S, title):
    M = len(S)
    N = len(S[0])
    fig, axs = plt.subplots(M, M, figsize=(10, 10))  # Create a grid of subplots
    
    for m in range(M):
        for j in range(M):
            if m <= j:  # Only plot upper triangular part to avoid duplication
                corr_fn = np.abs(np.correlate(S[m], S[j], mode='full'))
                lag_range = np.arange(-N + 1, N)
                axs[m, j].plot(lag_range, corr_fn)
                axs[m, j].set_xlabel("Lag (k)")
                axs[m, j].set_ylabel(r"$|R_{{{},{}}}(k)|$".format(m, j), fontsize=12)  # Using LaTeX for subscript
                axs[m, j].set_title(f"Correlation of signals {m} and {j}")
            else:
                axs[m, j].axis('off')  # Turn off axis for unused subplots
    
    plt.suptitle(title)
    plt.subplots_adjust(
        wspace=0.3,
        hspace=0.6,
        left=0.03,
        right=1-0.03
    )
    plt.show()

def plot_2_cplx(signal1,signal2,N):
    n = np.arange(N)  # Discrete time index
    # Combined plot for real and imaginary parts
    fig, axs = plt.subplots(2, 1, sharex=True)
    fig.suptitle('Signals 1 and 2')

    # Signal 1
    axs[0].plot(n, signal1.real, 'r-', linewidth=2, label='Signal 1')
    axs[0].set_ylabel('Real Part')
    axs[0].grid(True)

    axs[1].plot(n, signal1.imag, 'r-', linewidth=2)
    axs[1].set_xlabel('Sample Index (n)')
    axs[1].set_ylabel('Imaginary Part')
    axs[1].grid(True)

    # Signal 2
    axs[0].plot(n, signal2.real, 'b--', linewidth=2, label='Signal 2')
    axs[1].plot(n, signal2.imag, 'b--', linewidth=2)

    plt.legend()
    plt.show()

#### No work ####
# def multican(N,M,X0=None,epsilon=1e-3):
#     X = None
#     if X0 is None:
#         X = np.exp(1j * 2 * np.pi * np.random.rand(N, M))
#     else:
#         X = X0.copy()

#     XPrev = np.zeros((N, M), dtype=complex)
#     iter_diff = np.linalg.norm(X - XPrev, ord='fro')
#     Y = np.zeros((2 * N, M), dtype=complex)
#     V = np.zeros((2 * N, M), dtype=complex)

#     while(iter_diff > epsilon):
#         XPrev = X

#         # Step 1:
#         Y[0:N,:] = X
#         fftY = np.fft.fft(Y) / np.sqrt(2 * N)
#         for k in range(2*N):
#             V[k, :] = fftY[k, :] / np.linalg.norm(fftY[k, :]) * np.sqrt(2)

#         #step 2:
#         ifftV = np.sqrt(2*N)*np.fft.ifft(V)
#         X = np.exp(1j*np.angle(ifftV[:N, :]))

#         iter_diff = np.linalg.norm(X - XPrev, ord='fro')
    
#     return X

# if __name__ == "__main__":
#     sigs = np.transpose(loadmat("sigs.mat")['Xcan'])
#     print(len(sigs))
#     corr_plot(sigs, "MultiCAN Sig Set Correlations")