# Trying out making a class for my pdf stuff

from fpdf import FPDF
import calendar
import re

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
        range_low = 1
        annual_data = []
        for quarter in self.year_info:
            month_names = [calendar.month_name[i] for i in range(range_low, range_low + 3)]
            annual_data.append([month_names, zip(quarter[0], quarter[1], quarter[2])])
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

    def closePdf(self, name='tester.pdf'):
        self.pdf.output(name)
