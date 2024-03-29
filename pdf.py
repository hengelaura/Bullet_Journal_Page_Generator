# Trying out making a class for my pdf stuff

from fpdf import FPDF
import calendar
import re
import itertools

class PdfCal:
    def __init__(self, page_size, year):
        self.pdf = FPDF('P', 'mm', page_size)
        self.pdf.set_auto_page_break(False)
        self.pdf.add_font('Arial', '', r"C:\\Windows\\Fonts\\Arial.ttf")
        self.pdf.add_font('Arial', 'b', r"C:\\Windows\\Fonts\\Arial.ttf")
        self.year = year
        self.cal = calendar.Calendar()
        self.cal.setfirstweekday(calendar.SUNDAY)
        self.year_info = self.cal.yeardayscalendar(year)
        self.month_titles = (('January', 'February', 'March'),
                             ('April', 'May', 'June'),
                             ('July', 'August', 'September'),
                             ('October', 'November', 'December'))
        self.GRID_SIZE = 5

    def left_page(self):
        self.pdf.set_margins(7, 7, 10.5)  # set left and top margins to 7mm, right margin to 10.5mm
        self.pdf.add_page()  # add new page to pdf

    def right_page(self):
        self.pdf.set_margins(10.5, 7, 7)  # set left and top margins to 7mm, right margin to 10.5mm
        self.pdf.add_page()  # add new page to pdf

    def title_page(self, title):
        self.right_page()
        self.pdf.set_font('Arial', 'B', 54)
        self.pdf.ln(12 * self.GRID_SIZE)
        self.pdf.cell(9 * self.GRID_SIZE)
        self.pdf.cell(8 * self.GRID_SIZE, 6 * self.GRID_SIZE, str(title), 0, 1, 'C')

    def annual_calendar_page(self):
        self.pdf.set_font('Arial', '', 9)
        self.left_page()
        self.set_background("uwu")
        range_low = 1
        annual_data = []
        for quarter in self.year_info:
            month_names = [calendar.month_name[i] for i in range(range_low, range_low + 3)]
            annual_data.append([month_names, itertools.zip_longest(quarter[0], quarter[1], quarter[2], fillvalue=[0,0,0,0,0,0,0])])
            range_low += 3
        for quart in annual_data:
            for name in quart[0]:
                self.pdf.cell(7*self.GRID_SIZE, self.GRID_SIZE, name, 0, 0, 'C')
                self.pdf.cell(2*self.GRID_SIZE, self.GRID_SIZE, '', 0, 0)
            self.pdf.ln()
            for week in quart[1]:
                for w in week:
                    for d in w:
                        if d==0:
                            self.pdf.cell(self.GRID_SIZE, self.GRID_SIZE, '', 0, 0, 'C')
                        else:
                            self.pdf.cell(self.GRID_SIZE, self.GRID_SIZE, str(d), 0, 0, 'C')
                    self.pdf.cell(2*self.GRID_SIZE, self.GRID_SIZE, '')
                self.pdf.ln()
            self.pdf.ln()

    def monthly_spread(self, month_num):
        month_name = calendar.month_name[month_num]
        month = self.cal.monthdayscalendar(self.year, month_num)
        left_month = [w[:4] if 0 not in w[:4] else [d if d!=0 else '' for d in w[:4]] for w in month]
        right_month = [w[4:] if 0 not in w[4:] else [d if d!=0 else '' for d in w[4:]] for w in month]
        # size of the day is 6 grids high, 6 grids wide
        self.left_page()
        self.pdf.set_font_size(9)
        calendar.setfirstweekday(calendar.SUNDAY)
        for i in [6,0,1,2]:
            self.pdf.cell(6*self.GRID_SIZE, self.GRID_SIZE, calendar.day_name[i], 1, 0, 'C')
        self.pdf.ln()
        for w in left_month:
            for d in w:
                x = self.pdf.get_x() + (6*self.GRID_SIZE)
                y = self.pdf.get_y()
                self.pdf.multi_cell(6*self.GRID_SIZE, self.GRID_SIZE, str(d)+'\n\n\n\n\n\n', 1, 'R')
                self.pdf.set_xy(x,y)
            self.pdf.ln(6*self.GRID_SIZE)
        self.right_page()
        for i in [3,4,5]:
            self.pdf.cell(6*self.GRID_SIZE, self.GRID_SIZE, calendar.day_name[i], 1, 0, 'C')
        self.pdf.ln()
        for w in right_month:
            for d in w:
                x = self.pdf.get_x() + (6*self.GRID_SIZE)
                y = self.pdf.get_y()
                self.pdf.multi_cell(6*self.GRID_SIZE, self.GRID_SIZE, str(d)+'\n\n\n\n\n\n', 1, 'R')
                self.pdf.set_xy(x,y)
            self.pdf.ln(6*self.GRID_SIZE)

    def set_background(self, image_path):
        x = self.pdf.get_x()
        y = self.pdf.get_y()
        # self.pdf.set_xy(0,0)
        self.pdf.image("C:\\Users\\henge\\PycharmProjects\\Bullet_Journal_Generator\\background1.jpg", 0, 0, w=150, h=210)
        self.pdf.set_xy(x,y)

    def closePdf(self, name='tester.pdf'):
        self.pdf.output(name)
