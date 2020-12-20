from pylatex import MiniPage, NoEscape


class Page:
    def __init__(self, num_rows, num_cols):
        self.page = MiniPage(width=r"\textwidth", height=r"\textheight")
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.row = 0
        self.col = 0

    def next_minipage(self):
        self._increment_position()
        minipage = MiniPage(
            width=fr"{1.0 / self.num_cols}\textwidth",
            height=fr"{0.99 / self.num_rows}\textheight",
            align="c",
            pos="t",
        )
        self.page.append(minipage)
        return minipage

    def _increment_position(self):
        if self.col == self.num_cols:
            self.row += 1
            self.col = 0
            self.page.append(NoEscape(r"\linebreak"))
        self.col += 1
