# This is a Bullet Journal page generator

import calendar
from fpdf import FPDF
import itertools


def left_page(pdf_in):
    pdf_in.set_margins(7, 7, 10.5)  # set left and top margins to 7mm, right margin to 10.5mm
    pdf_in.add_page()  # add new page to pdf
    pdf_in.set_margins(7, 7, 10.5)  # set left and top margins to 7mm, right margin to 10.5mm


def right_page(pdf_in):
    pdf_in.set_margins(10.5, 7, 7)  # set left margin to 10.5mm, top and right margins to 7mm
    pdf_in.add_page()  # add new page to pdf
    pdf_in.set_margins(10.5, 7, 7)  # set left margin to 10.5mm, top and right margins to 7mm


def title_page(pdf_in, title):
    right_page(pdf)
    pdf.set_font('Arial', 'B', 54)
    pdf.ln(12 * GRID_SIZE)
    pdf.cell(9 * GRID_SIZE)
    pdf.cell(8 * GRID_SIZE, 6 * GRID_SIZE, str(title), 0, 1, 'C')


def print_week(week, pdf_in):
    if (week != None):
        for day in week:
            if day != 0:
                pdf_in.cell(GRID_SIZE, GRID_SIZE, str(day), 0, 0, 'C')
            else:
                pdf_in.cell(GRID_SIZE, GRID_SIZE)
        pdf_in.cell(GRID_SIZE, GRID_SIZE)
    else:
        pdf_in.cell(8 * GRID_SIZE, GRID_SIZE)


def annual_calender(pdf_in, zip_yr_info, year):
    left_page(pdf_in)
    pdf_in.set_font('Arial', 'B', 16)
    pdf_in.cell(11 * GRID_SIZE, 1 * GRID_SIZE)  # center on page and go down one row
    pdf_in.cell(4 * GRID_SIZE, 2 * GRID_SIZE, str(year), 0, 0, 'C')
    pdf_in.ln(3 * GRID_SIZE)
    pdf_in.set_font('Arial', '', 9)
    for yr, title in zip_yr_info:
        pdf_in.cell(GRID_SIZE, GRID_SIZE)
        for t in title:
            pdf_in.cell(7 * GRID_SIZE, 1 * GRID_SIZE, t, 0, 0, 'R')
            pdf_in.cell(GRID_SIZE, GRID_SIZE, "", 0, 0)
        pdf_in.ln(GRID_SIZE)
        for m1, m2, m3 in itertools.zip_longest(yr[0], yr[1], yr[2]):
            pdf_in.cell(GRID_SIZE, GRID_SIZE)
            print_week(m1, pdf_in)
            print_week(m2, pdf_in)
            print_week(m3, pdf_in)
            pdf_in.ln(GRID_SIZE)
        pdf_in.ln(GRID_SIZE * 2)


def split_weeks(month):
    left_side = []
    right_side = []
    for week in month:
        left_side.append(week[:4])
        right_side.append(week[4:])
    return left_side, right_side


def print_month_side(pdf_in, side):
    for w1 in side:
        if sum(w1) == 0:
            continue
        pdf_in.cell(GRID_SIZE)
        for d1 in w1:
            if d1 != 0:
                pdf_in.cell(6*GRID_SIZE, 6*GRID_SIZE, '', 1, 0)
                pdf_in.cell(-1*GRID_SIZE, GRID_SIZE)
                pdf_in.cell(GRID_SIZE, GRID_SIZE, str(d1), 0, 0)
            else:
                pdf_in.cell(6*GRID_SIZE, 6*GRID_SIZE)
        pdf_in.ln(GRID_SIZE*6)


def print_notes_box(pdf_in):
    pdf_in.set_xy(10.5 + GRID_SIZE, 7 + (31 * GRID_SIZE))
    pdf_in.cell(26 * GRID_SIZE, 8 * GRID_SIZE, '', 1)
    pdf_in.set_xy(10.5 + GRID_SIZE, 7 + (31 * GRID_SIZE))
    pdf_in.cell(GRID_SIZE, GRID_SIZE, 'Notes', 0, 0, 'L')


def print_month_title(pdf_in, mname):
    pdf_in.set_xy(10.5 + GRID_SIZE, 7 + (8 * GRID_SIZE))
    pdf_in.rotate(270, 10.5 + (13 * GRID_SIZE), 7 + (19 * GRID_SIZE))
    pdf_in.set_font('Arial', '', 60)
    pdf_in.cell(18 * GRID_SIZE, GRID_SIZE, mname, 0, 0, 'C')
    pdf_in.rotate(0)
    pdf_in.set_font('Arial', '', 50)


# create monthly calendar view
# consists of 3 pages:
# right page: title of month only
# left page : half of month spread
# right page : other half of month spread
def monthly_spread(pdf_in, month):
    # get data for month
    m_data = obj.monthdayscalendar(2023, month)
    name = calendar.month_name[month]
    title_page(pdf_in, name)
    left_page(pdf_in)
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    pdf_in.set_font('Arial', '', 10)
    pdf_in.cell(GRID_SIZE)
    for wd in weekdays[:4]:
        pdf_in.cell(6*GRID_SIZE, GRID_SIZE, wd, 1, 0, 'C')
    left, right = split_weeks(m_data)
    pdf_in.ln(GRID_SIZE)
    # jump down a line of grids if sum(right[0]) <= 6 and len(month) < 6
    space_down = ((sum(right[0]) <= 6) and (sum(right[0]) > 0))
    if space_down:
        pdf_in.cell(6 * GRID_SIZE)
        pdf_in.ln(6 * GRID_SIZE)
    print_month_side(pdf_in, left)
    pdf_in.set_xy(7+GRID_SIZE, 7)
    pdf_in.cell(24*GRID_SIZE, 7*GRID_SIZE, '', 1)

    right_page(pdf_in)
    pdf_in.cell(GRID_SIZE)
    for wd in weekdays[4:]:
        pdf_in.cell(6*GRID_SIZE, GRID_SIZE, wd, 1, 0, 'C')
    pdf_in.ln(GRID_SIZE)
    print_month_side(pdf_in, right)
    pdf_in.set_xy(10.5+GRID_SIZE, 7)
    pdf_in.cell(GRID_SIZE, 7*GRID_SIZE, '', 'L')
    # add notes box
    print_notes_box(pdf_in)
    # add title on side of page
    print_month_title(pdf_in, name)


def monthly_bills(pdf_in):
    left_page(pdf_in)


def weekly_spread(pdf_in, months, week_data):
    pdf_in.set_font('Arial', '', 26)

    left_page(pdf_in)
    header = calendar.month_name[months[0]] + " " + str(week_data[0]) + " - " + calendar.month_name[months[1]] + " " + str(week_data[-1])
    pdf_in.cell(GRID_SIZE*26, GRID_SIZE*4, header, 0, 0, 'C')
    pdf_in.ln(4*GRID_SIZE)
    pdf_in.set_font('Arial', '', 12)
    x = 0
    y = 0
    for dayname1, day1 in zip(calendar.day_name[:4], week_data[:4]):
        pdf_in.cell(GRID_SIZE*13, GRID_SIZE*17, '', 1)
        x = pdf_in.get_x()
        y = pdf_in.get_y()
        pdf_in.set_xy(x-(GRID_SIZE*13), y)
        pdf_in.cell(GRID_SIZE*13, GRID_SIZE, str(dayname1) + " " + str(day1), 0, 0, 'C')
        pdf_in.set_xy(x, y)
        if pdf_in.get_x() > 26*GRID_SIZE:
            pdf_in.ln(GRID_SIZE*17)

    right_page(pdf_in)
    pdf_in.ln(4*GRID_SIZE)
    for dayname2, day2 in zip(calendar.day_name[4:], week_data[4:]):
        pdf_in.cell(13*GRID_SIZE, 17*GRID_SIZE, '', 1)
        x = pdf_in.get_x()
        y = pdf_in.get_y()
        pdf_in.set_xy(x - (GRID_SIZE * 13), y)
        pdf_in.cell(GRID_SIZE * 13, GRID_SIZE, str(dayname2) + " " + str(day2), 0, 0, 'C')
        pdf_in.set_xy(x, y)
        if pdf_in.get_x() > 26*GRID_SIZE:
            pdf_in.ln(GRID_SIZE*17)

    pdf_in.cell(13 * GRID_SIZE, 17 * GRID_SIZE, '', 1)
    x = pdf_in.get_x()
    y = pdf_in.get_y()
    pdf_in.set_xy(x - (GRID_SIZE * 13), y)
    pdf_in.cell(GRID_SIZE * 13, GRID_SIZE, "Notes", 0, 0, 'C')


GRID_SIZE = 5  # constant for size of grid square - both height and width
LIST_INDENT_L = 7 + (5*GRID_SIZE)
if __name__ == '__main__':

    annual_titles = [['January', 'February', 'March'],
                ['April', 'May', 'June'],
                ['July', 'August', 'September'],
                ['October', 'November', 'December']]
    year = 2023  # temporary placeholder
    obj = calendar.Calendar()
    obj.setfirstweekday(calendar.SUNDAY)
    year_info = obj.yeardayscalendar(year)  # creates data for entire year. 4 groups of 3 months worth of data
    zip_yr_info = zip(year_info, annual_titles)
    
    # create the pdf file now that we have info on the year
    pdf = FPDF('P', 'mm', 'A5')  # set pdf to be portrait mode, in mm, and on A5 paper
    pdf.set_auto_page_break(False)
    title_page(pdf, year)
    annual_calender(pdf, zip_yr_info, year)

    rollover_list = []
    rollunder_list = []
    for index in range(1, 13):
        if len(rollover_list) != 0:
            num = 1
            while len(rollover_list) < 7:
                rollover_list.append(num)
                num += 1
            #weekly_spread(pdf, [index-1, index], rollover_list)
            rollover_list.clear()
        obj.setfirstweekday(calendar.SUNDAY)
        #monthly_spread(pdf, index)
        if len(rollunder_list) != 0:
            num = 1
            while len(rollunder_list) < 7:
                rollunder_list.append(num)
                num += 1
            weekly_spread(pdf, [index-1, index], rollunder_list)
            rollunder_list.clear()
        obj.setfirstweekday(calendar.MONDAY)
        for week in obj.monthdayscalendar(year, index):
            if week.count(0) == 0:
                rollunder_list = []
                weekly_spread(pdf, [index, index], week)
            elif week.count(0) < 4:
                rollover_list = week[:week.index(0)]
            else:  # this is if there are less than 4 "leftover days"
                rollunder_list = week[:week.index(0)]

    pdf.output("C:\\Users\\henge\\Documents\\Bullet Journal Templates\\tuto1.pdf", 'F')
    print('Generation complete')




