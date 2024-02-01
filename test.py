import pdf
import calendar
import re

myFile = pdf.PdfCal('A5', 2024)
myFile.annual_calendar_page()  # left page
myFile.title_page(myFile.year)  # right page
myFile.left_page()  # left page
myFile.title_page(calendar.month_name[1])
myFile.monthly_spread(1)
myFile.closePdf()
