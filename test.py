import pdf
import calendar
import re

myFile = pdf.PdfCal('A5', 2024)
#  myFile.left_page()
#  myFile.set_background('dodod')
myFile.annual_calendar_page()  # left page
myFile.title_page(myFile.year)  # right page
myFile.left_page()  # left page
for i in range(1,13):
    myFile.title_page(calendar.month_name[i])
    myFile.monthly_spread(i)
    myFile.left_page()
myFile.closePdf()
