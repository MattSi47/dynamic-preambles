import numpy as np
import matplotlib.pyplot as plt


# Parameters
T = 40e-6  # signal time
B = 4e6  # bandwidth of signal (samples/sec)
N = round(T * B)  # Number of samples
amplitude = 1  # Amplitude of the signal

# Generate chirp function
t = np.linspace(0, 40e-6, 1000)

upchirp = np.exp(1j*2*np.pi*(-2e6*t+2e6*t**2/4e7))
downchirp = np.exp(1j*2*np.pi*(2e6*t-2e6*t**2/4e7))



# Calculate autocorrelation
autocorrelation = np.correlate(upchirp, upchirp, mode='full')


# Plot autocorrelation
plt.plot(autocorrelation)
plt.xlabel("Lag")
plt.ylabel("Autocorrelation")
plt.title("Autocorrelation of Chirp Function")
plt.show()