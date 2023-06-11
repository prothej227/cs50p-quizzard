from fpdf import FPDF
from datetime import datetime
import calendar

class Certificate(FPDF):

    def __init__(self, username, score: int) -> None:
        super().__init__(orientation='L', unit='pt')
        self.username = username
        self.score = score

        self.add_page()
        self.y_cur = 0
        self.set_text_color(255, 255, 255)

        self.image('./assets/background.png', 0, 0, self.w, self.h)
        self.set_name_text()
        self.set_sub_text1()
        self.set_sub_text2()

    def set_name_text(self) -> None:
        self.set_font('Helvetica', 'B', 35)
        self.y_cur += ((self.h - self.font_size) / 2 + self.font_size)
        self.set_xy((self.w - self.get_string_width(self.username)) / 2, (self.h - self.font_size) / 2)
        self.cell(self.get_string_width(self.username), self.font_size, self.username, align='C')

    def set_sub_text1(self) -> None:
        _text = "for active participation and successfully passing the Quizzard assessment, "
        self.set_font('Helvetica', '', 16)
        self.y_cur += self.font_size + 10
        self.set_xy((self.w - self.get_string_width(_text)) / 2, self.y_cur)
        self.cell(self.get_string_width(_text), self.font_size, _text, align='C')
        _text = f"garnering a score of {self.score} out of 100."
        self.set_font('Courier', 'B', 14)
        self.y_cur += self.font_size + 1
        self.set_xy((self.w - self.get_string_width(_text)) / 2, self.y_cur)
        self.cell(self.get_string_width(_text), self.font_size, _text, align='C')

    def set_sub_text2(self) -> None:
        _text = f"Given on this day: {self.transform_date(datetime.now())}"
        self.set_font('Helvetica', '', 13)
        self.y_cur += self.font_size + 15
        self.set_xy((self.w - self.get_string_width(_text)) / 2, self.y_cur)
        self.cell(self.get_string_width(_text), self.font_size, _text, align='C')

    def transform_date(self, date: datetime) -> str:
        ord_suff = 'th' if (11 <= date.day <= 13) else {1: 'st', 2: 'nd', 3: 'rd'}.get(date.day % 10, 'th')
        month_name = calendar.month_name[date.month]
        return f"{date.day}{ord_suff} of {month_name}, {date.year}"


if __name__ == '__main__':
    cert = Certificate(username="David J. Malan", score=100)
    cert.output('certificate.pdf')