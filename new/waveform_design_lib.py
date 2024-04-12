import numpy as np
from scipy import signal
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from paretoset import paretoset
from adjustText import adjust_text
from matplotlib import cm

#### Signal modification tools ####

def chirp_fn(T, B, f0, f1):
    Ts = 1/B
    N = round(T*B)
    chirp_sig = np.zeros(N, dtype=np.complex64)
    for n in range(N):
        chirp_sig[n] = np.exp(1j*2*np.pi*((f0-f1)/T)*(n*Ts)**2 + f0*T)
    return chirp_sig

def preamble_set_out(S, title):
    N = len(S[0])
    S_txt = ""
    for m in range(len(S)):
        S_txt = ""
        for n in range(N):
            S_txt += f"({np.real(S[m][n])}|{np.imag(S[m][n])})"
            if not n == N-1:
                S_txt += ","
        with open(f'{title}_{m}.csv', 'w') as f:
            f.write(S_txt)

def xcorr(x, y):
    corr = np.abs(signal.correlate(x, y, mode='full', method="fft"))
    return corr

def normalize(sig):
    #mag = np.sqrt(np.vdot(sig,sig))
    mag = np.linalg.norm(sig)
    x = sig/mag
    # print(f"Max of norm sig:{max(x)}")
    return x

def normalize_set(S):
    S_norm = np.zeros((len(S),len(S[0])))
    for m in range(len(S)):
        S_norm[m] = normalize(S[m])
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
def ambiguity_fn(filt_in, sig_in, freqs, B, norm_inputs=False):
    #print(f"filt_in: {filt_in}")
    if not norm_inputs:
        filt = normalize(filt_in)
        sig = normalize(sig_in)
    else:
        filt = filt_in
        sig = sig_in
    #print(f"filt: {filt}")
    Ts = 1/B
    K = len(filt)+len(sig)-1
    I = len(freqs)
    af = np.zeros((I,K))
    n = np.arange(len(sig))
    for i in range(I):
        sig_CFO = sig*np.exp(1j*2*np.pi*freqs[i]*n*Ts)
        # plot_complex(sig_CFO, f"sig_CFO {i}, cfo={freqs[i]}")
        #print(f"dot: {np.vdot(sig_CFO,filt)}")
        af[i] = xcorr(filt, sig_CFO) #np.abs(signal.correlate(filt, sig_CFO, mode='full', method="fft"))
        # plot_complex(af[i], f"CC mag {i}")
    
    return af

def psl(S,i,j, S_is_normalized=False):
    S_=None
    if not S_is_normalized:
        S_ = normalize_set(S)
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
        S_ = normalize_set(S)
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
        S_ = normalize_set(S)
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
    adjust_text(labels, arrowprops=dict(arrowstyle='->', color='black'))

    # Labels and title 
    plt.xlabel("Max autocorrelation sidelobe value")
    plt.ylabel("Max crosscorrelation value")
    plt.title("Pareto analysis of signal sets")

    plt.show()


def plot_complex(complex_signal,title=""):
    # Extract real and imaginary parts
    real_part = np.real(complex_signal)
    imaginary_part = np.imag(complex_signal)

    # Create sample indices
    samples = np.arange(len(complex_signal))

    # Plot stacked stem plots for real and imaginary parts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Plot real part
    ax1.plot(samples, real_part)
    ax1.set_ylabel('Real Part')
    ax1.grid(True)

    # Plot imaginary part
    ax2.plot(samples, imaginary_part)
    ax2.set_xlabel('Sample Index')
    ax2.set_ylabel('Imaginary Part')
    ax2.grid(True)

    plt.suptitle(title)
    plt.show()

    


def corr_plot(S, title):
    M = len(S)
    N = len(S[0])
    fig, axs = plt.subplots(M, M, figsize=(10, 10))  # Create a grid of subplots
    
    for m in range(M):
        for j in range(M):
            if m <= j:  # Only plot upper triangular part to avoid duplication
                corr_fn = xcorr(normalize(S[m]), normalize(S[j])) # np.abs(signal.correlate(S[m], S[j], mode='full', method="fft"))
                print(f"Max of corr {m}, {j}:{max(corr_fn)}")
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

def plot_ambiguity(filter, sig, B, cfo_freqs,title=""):
    # Length of the correlation operation
    K = len(filter) + len(sig) - 1
    
    # since 0 is assumed to be first full overlap between 2 signals
    if K%2 == 0:
        k_upper = K/2
        k_lower = -k_upper + 1
    else:
        k_upper = (K-1)/2
        k_lower = -k_upper
        
    delay = np.linspace(k_lower, k_upper, num=K)  # Time axis for the signal
    cfo_freqs = np.linspace(cfo_freqs[-1], cfo_freqs[0], num=len(cfo_freqs))  # Frequency axis

    Ts = 1/B
    # Compute the ambiguity function surface
    AF = ambiguity_fn(filter, sig, np.array(cfo_freqs), B)

    #===========================#
    # Plotting the surface
    fig = plt.figure(figsize=(10,20))
    fig.clf()

    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.clear()

    x_coords = delay
    y_coords = cfo_freqs/1000
    mesh_z = AF
    (mesh_x, mesh_y) = np.meshgrid(x_coords, y_coords)

    surface_z = np.vstack((np.zeros(len(AF[0])), AF[-1])) #don't know
    (surface_x, surface_y) = np.meshgrid(x_coords, [0,0])
    # makes the "front cover" of the plot
    ax3d.plot_surface(surface_x, surface_y, surface_z, linewidth=0, edgecolor="black", color="black", shade=False, alpha=1)
    
    #plot AF
    ax3d.plot_surface(mesh_x, mesh_y, mesh_z, linewidth=1, color="whitesmoke", edgecolor="black", shade=True, alpha=1)

    # visual stuff
    ax3d.view_init(elev=35, azim=135)
    ax3d.set_zlim([0, 1])

    ax3d.set_xlabel(' Sample lag $ \\it k$ ', fontsize=12)
    ax3d.set_ylabel(' CFO (kHz), $\\it f$ ', fontsize=12)
    ax3d.set_zlabel(' $|\\it\\chi(\\it\\k,\\it f)|$ ', fontsize=12)
    fig.suptitle(f"{title}", fontsize=18, )
    # Adjusting plot layout to center the plot and title
    plt.subplots_adjust(top=0.95, left=0.05, right=0.95)
    plt.show()
    fig.savefig(f"{title}.png", format="png")

    # Plotting the 2D colormap
    plt.figure(figsize=(8, 6))  # Set the figure size (width, height)
    plt.imshow(AF.T, extent=[min(delay), max(delay), min(cfo_freqs), max(cfo_freqs)/1000], aspect='auto', cmap='viridis')
    plt.colorbar(label='Magnitude')
    plt.xlabel('Sample lag $ \\it k$')
    plt.ylabel('CFO (kHz), $\\it f$ (kHz)')
    plt.title(f"Ambiguity Function: {title}")
    plt.grid(True)

    # Saving and displaying the plot
    plt.tight_layout()
    plt.show()
    plt.savefig(f"{title}_2D.png", format="png")

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