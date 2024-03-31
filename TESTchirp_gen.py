import math
import numpy as np
import cmath
# output format: (complex(re1,im1),complex(re2,im2),...)
# length Fs * Tpreamble

import os
path = os.getcwd()
print(path)

Fs = 5e6
Ts = 1/Fs
f_limit = 1e6
Tpreamble = 40e-6
N = round(Fs*Tpreamble)
j = complex(0.0,1.0)
def chirp_fn(t, f=f_limit, T=Tpreamble):
    x = cmath.exp(2*j*math.pi*((f/T)*(t**2)+(-f)*t))
   # theta = 2*math.pi*(f/T)*t**2 + (-f)*T
    return f"({x.real}|{x.imag}),"

print(f"N={N}")

chirp_sig = ""
for n in range(N):
    chirp_sig += chirp_fn(n*Ts)

#remove last ","
chirp_sig = chirp_sig[:-1]


with open('chirp.csv', 'w') as f:
    f.write(chirp_sig)
