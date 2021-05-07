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


data = {
    "arr": [
        ["Monday", {"time": "14:00-15:00", "column": "Court1"},
            {"time": "15:00-16:00", "column": "Court1"}],
        ["Tuesday"],
        ["Wednesday"],
        ["Thursday", {"time": "16:00-17:00", "column": "Court1"},
            {"time": "17:00-18:00", "column": "Court1"}],
        ["Friday"],
        ["Saturday"],
        ["Sunday", {"time": "18:00-19:00", "column": "Court1"},
            {"time": "19:00-20:00", "column": "Court1"}]
    ]
}

booking = data['arr']
for value in booking:
    print(value[0])
    for i in range(len(value)-1):
        test = value[i+1]['time']
        print(test)


# for value in booking:
#     court = int(value['column'][5:])
#     mytime = int(value['time'][:2])

#     strday = value['weekday']
#     mydate = datetime.strptime(year_month, '%Y-%m').date()
#     day_of_week = list(calendar.day_name).index(strday)

#     thismonth_day = calendar.monthcalendar(
#         dt_now.year, dt_now.month)[1][day_of_week]
#     thismonth_date = datetime(
#         dt_now.year, dt_now.month, thismonth_day)
#     thismonth_date = timezone.make_aware(thismonth_date)

#     valid_history = book.check_valid_group_history(
#         court=court, mydate=thismonth_date, mytime=mytime)
#     valid_yourhsitory = book.check_valid_group_history_for_booking(
#         court=court, mydate=thismonth_date, mytime=mytime, mygroup=q_group)
#     valid_thismonth = valid_history or valid_yourhsitory

#     for day in calendar.monthcalendar(mydate.year, mydate.month):
#         if day[day_of_week] != 0:
#             booking_date = date(
#                 mydate.year, mydate.month, day[day_of_week])
#             booking_date_list.append(booking_date)
#             book.check_valid_group(
#                 court=court, mytime=mytime, mydate=booking_date)
#             if book.check_valid_group(court=court, mytime=mytime, mydate=booking_date) and valid_thismonth:
#                 booking_datetime = timezone.make_aware(
#                     datetime.combine(booking_date, time(mytime)))
#                 bookingid = uuid4().hex
#                 q_court = models.EachCourtInfo.objects.get(
#                     court_number=court)
#                 price_normal = q_court.price_normal
#                 ds_group = q_court.price_ds_group
#                 ds_time = q_court.price_ds_time
#                 ds_time_start = q_court.time_ds_start.hour
#                 ds_time_end = q_court.time_ds_end.hour

#                 if not mytime in range(int(ds_time_start), int(ds_time_end)):
#                     ds_time = 0

#                 booking_obj, booking_created = models.Booking.objects.get_or_create(
#                     name=name,
#                     email=email,
#                     tel=tel,
#                     member=member,
#                     group=q_group,
#                     court=q_court,
#                     booking_datetime=booking_datetime,
#                     exp_datetime=dt_exp,
#                     price_normal=price_normal,
#                     price_ds=ds_group+ds_time,
#                     price_pay=price_normal-ds_group-ds_time,
#                     bookingid=bookingid)

#                 if booking_created:
#                     booking_obj_list.append(booking_obj)
#                     all_price_normal += price_normal
#                     all_ds_group += ds_group
#                     all_ds_time += ds_time
#                 else:
#                     booking_obj.delete()
#                     break
#             else:
#                 break
#     else:
#         continue
#     break
# else:
