import math
import numpy as np
# output format: (complex(re1,im1),complex(re2,im2),...)
# length Fs * Tpreamble

Fs = 5e6
Ts = 1/Fs
f_start = 1e5
f_end = 1e6
Tpreamble = 40e-6
N = round(Fs*Tpreamble)
def chirp_fn(t, f0=f_start, f1=f_end, T=Tpreamble):
    theta = 2*math.pi*((f0-f1)/T)*t**2 + f0*T
    return f"complex({np.float32(math.cos(theta))},{np.float32(math.sin(theta))}),"

print(f"N={N}")

chirp_sig = "("
for n in range(N):
    chirp_sig += chirp_fn(n*Ts)

#remove last ","
chirp_sig = chirp_sig[:-1]
chirp_sig += ")"

with open('chirp.txt', 'w') as f:
    f.write(chirp_sig)