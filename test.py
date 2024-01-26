
import calendar


home = calendar.Calendar()
home.setfirstweekday(calendar.SUNDAY)
home.setfirstweekday(calendar.MONDAY)
for item in home.monthdayscalendar(2023, 1):
    print(item)

# print(home.yeardays2calendar(2023))
# print(calendar.month_name)

for month in calendar.month_name:
    pass
    # print(month)


# print(calendar.month_name[3])
home.setfirstweekday(calendar.SUNDAY)
for thing in home.itermonthdates(2022, 1):
    pass
    #print(thing)