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

# for i in zip(range(5), range(5, 10)):
#     print(i)
#     print(i[0])
#     print(i[1])
l = [0, 1, 2, 3, 4]

# for i in range(10):
#     print('********', i)
#     for value in l:
#         if value < 5:
#             print(value)
#             if value % 2 == 0:
#                 print('in')
#                 if value != 2:
#                     print('in2')
#                 else:
#                     break
#             else:
#                 break

#     else:
#         continue
# break


for i in range(5):
    print(i)
    if i == 2:
        pass
else:
    continue
