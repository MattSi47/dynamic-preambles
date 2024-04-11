import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_complex_stem(complex_signal):
    # Extract real and imaginary parts
    real_part = np.real(complex_signal)
    imaginary_part = np.imag(complex_signal)

    # Create sample indices
    samples = np.arange(len(complex_signal))

    # Plot stacked stem plots for real and imaginary parts
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Plot real part
    ax1.stem(samples, real_part, linefmt='b-', markerfmt='bo', basefmt=' ')
    ax1.set_ylabel('Real Part')
    ax1.grid(True)

    # Plot imaginary part
    ax2.stem(samples, imaginary_part, linefmt='r-', markerfmt='ro', basefmt=' ')
    ax2.set_xlabel('Sample Index')
    ax2.set_ylabel('Imaginary Part')
    ax2.grid(True)

    plt.suptitle('Stacked Stem Plots of Real (Blue) and Imaginary (Red) Components')
    plt.show()

def plot_complex_3d(complex_signal, space):
    # Extract real and imaginary parts
    real_part = np.real(complex_signal)
    imaginary_part = np.imag(complex_signal)

    # Create 3D plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot real and imaginary parts in 3D
    ax.plot(space, real_part, imaginary_part, label='Analytic Signal', marker='o')

    ax.set_xlabel('Time')
    ax.set_ylabel('Real Part')
    ax.set_zlabel('Imaginary Part')
    ax.set_title('3D Plot of Analytic Signal')
    ax.legend()

    plt.show()

# Parameters
T = 40e-6  # signal time
B = 4e6  # bandwidth of signal (samples/sec)
N = round(T * B)  # Number of samples
amplitude = 1  # Amplitude of the signal

# Generate complex signal
n = np.linspace(0, N-1, N)
phi_up = np.pi*(n**2/N - n)
phi_down = np.pi*(-n**2/N + n)


upchirp = np.exp(1j*2*np.pi*phi_up)
downchirp = np.exp(1j*2*np.pi*phi_down)

plot_complex_stem(upchirp)
plot_complex_stem(downchirp)

# phi = 0*n
# for k in range(1,round(N/2)):
#     phi = phi + (((4/(np.pi*k)) * N) / k) * np.sin(2*np.pi*k*n/N)
               


# # Plot 3D plot of the analytic signal using the function
# plot_complex_stem(analytic_signal)
# plot_complex_3d(analytic_signal, n)

# # continuous:
# t = np.linspace(0,T,10000)
# f_m=2e6
# #phi = f_m*t**2/T - f_m*t
# phi = np.cos(2*np.pi*1e6*t)
# cont_sig = np.exp(1j*2*np.pi*phi)
# plot_complex_stem(cont_sig)
# plot_complex_3d(cont_sig, t)