# for i in range(5):
#     for j in range(5):
#         if i == 7:
#             break
#         else:
#             print(i, j)
#     else:
#         continue
#     break

# from itertools import product
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
# l = [0, 1, 2, 3, 4]

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


# for i in range(5):
#     print(i)
#     if i == 2:
#         pass
# else:
#     continue

# request.GET.__init__(mutable=True)
# request.GET.appendlist('q', 0)
# print(request.GET)
# # request.GET.__init__(mutable=False)
# request.GET.__setitem__('test3', 0)
# print(request.GET)


# data = {
#     "arr": [
#         ["Monday", {"time": "14:00-15:00", "column": "Court1"},
#             {"time": "15:00-16:00", "column": "Court1"}],
#         ["Tuesday"],
#         ["Wednesday"],
#         ["Thursday", {"time": "16:00-17:00", "column": "Court1"},
#             {"time": "17:00-18:00", "column": "Court1"}],
#         ["Friday"],
#         ["Saturday"],
#         ["Sunday", {"time": "18:00-19:00", "column": "Court1"},
#             {"time": "19:00-20:00", "column": "Court1"}]
#     ]
# }

# booking = data['arr']

# mybooking = list()
# for value in booking:
#     if len(value) == 1:
#         continue
#     print(value[0])
#     for i in range(len(value)-1):
#         mybooking.append(
#             {'weekday': value[0], 'column': value[i+1]['column'], 'time': value[i+1]['time']})
