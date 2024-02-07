import math
import numpy as np

# data of form:
# [
#     [[beta1, alpha1], [beta2, alpha2],..], #gen 0
#     [[beta1, alpha1], [beta2, alpha2],..], #gen 1
#     ...
# ]

# signal sets of form:
# [
#     [[s0, s1, s2,..., sN], [s0, s1, s2,..., sN],..], #sig set 0
#     [[s0, s1, s2,..., sN], [s0, s1, s2,..., sN],..], #sig set 1
#     ...
# ]

# test_data = np.array([
#     [[1,2,3,4.6], [1,2,3,4], [1,2,3,4]],
#     [[5,6,7,8], [5,6,7,8], [5,6,7,8]],
#     [[4,3,2,1], [4,3,2,1], [4,3,2,1]]
# ], dtype=np.float80)

# test_data[0][0] = np.array([10, 20, 30, 40])
# print(test_data)
# print("---------------------")
# y = np.asarray(test_data[0][0]/np.linalg.norm(test_data[0][0]))
# test_data[0,0]=y
# print("---------------------")
# print(test_data)

# norm_pareto_set = np.copy(test_data)
# for i in range(len(test_data)):
#     for j in range(len(test_data[i])):
#         norm_pareto_set[i][j] = norm_pareto_set[i][j] / np.linalg.norm(norm_pareto_set[i][j])
# print("---------------")
# print(norm_pareto_set)

testing = np.array([
    [[1, 2], [1, 2], [1, 2], [1, 2], [1, 2]],
    [[3, 4], [3, 4], [3, 4], [3, 4], [3, 4]],
    [[5, 6], [5, 6], [5, 6], [5, 6], [5, 6]]
])

testing1 = np.empty([len(testing), 2, len(testing[0])])
# print(testing1)
for i in range(len(testing)):
    testing1[i][0] = [pt[0] for pt in testing[i]]
    testing1[i][1] = [pt[1] for pt in testing[i]]


print(testing1)