# for i in range(5):
#     for j in range(5):
#         if i == 7:
#             break
#         else:
#             print(i, j)
#     else:
#         continue
#     break

from itertools import product
# ii = 1
# for i, j in product(range(5), range(5)):
#     print(ii)
#     ii += 1
#     # if i == 2 and j == 2:
#     #     break
#     # print(i, j)
#     # break

for i in zip(range(5), range(5, 10)):
    print(i)
    print(i[0])
    print(i[1])
