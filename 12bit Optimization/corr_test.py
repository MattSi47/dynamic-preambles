import numpy as np
from scipy.signal import correlate
my_array_flat = np.array([1, 2, 3, 3, 1, 2, 3, 3, 4, 5, 6, 6, 4, 5, 6, 6, 7, 8, 9, 7, 7, 8, 9, 7])
my_array = np.array([[1, 2, 3, 3, 1, 2, 3, 3],
                     [4, 5, 6, 6, 4, 5, 6, 6],
                     [7, 8, 9, 7, 7, 8, 9, 7]])

gen_coeffs = np.array(np.reshape(my_array_flat, (3, 8)))
print(gen_coeffs)
print(gen_coeffs==my_array)
# Split into two rows 
arrays = np.hsplit(gen_coeffs, 2)
first_half = arrays[0]
second_half = arrays[1]

print(first_half)
print(second_half)
# x = [1,1,1,1]
# x.extend([1,1])
# print(x)
# print(correlate(x,x))
# print(range(1,1))

# def corr(x,y):
    
#     N = len(x)
#     r = [0]*N
#     for k in range(0, N):
#         r_k = 0
#         for n in range(k, N):
#             print(f'n={n}, k={k}')
#             r_k = r_k + x[n]*y[n-k]
#         r[k] = r_k
#         r_k = 0
    
#     return r

# print(corr(x,x))