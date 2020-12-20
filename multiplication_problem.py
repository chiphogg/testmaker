import random

from pylatex import NoEscape, Tabular


class MultiplicationProblemFactory:
    """A factory for multiplication problems.

    Like any problem factory, the contract is:
        - We accept parsed command line arguments for configuration.
        - When called, the `generate_problem()` function will return a new problem,
          i.e., an object with `get_problem()` and `get_solution()` member functions.
    """

    def __init__(self, args):
        self.first_digits = args.first_digits
        self.second_digits = args.second_digits
        self.override_max = args.override_max

    def generate_problem(self):
        return MultiplicationProblem(
            first_num=self.generate_first_num(), second_num=self.generate_second_num()
        )

    def generate_first_num(self):
        return self._generate_num(num_digits=self.first_digits)

    def generate_second_num(self):
        return self._generate_num(num_digits=self.second_digits)

    def _generate_num(self, num_digits):
        bounds = (
            (1, self.override_max)
            if self.override_max
            else (int("1" + ("0" * (num_digits - 1))), int("9" * num_digits))
        )
        return random.randint(*bounds)


class MultiplicationProblem:
    def __init__(self, first_num, second_num):
        self.first_num = first_num
        self.second_num = second_num

    def _problem_tuple(self):
        """Return a tuple with the first multiplicand, the symbol for the operation, the
        second multiplicand, and the solution."""
        return (
            self.first_num,
            r"\times",
            self.second_num,
            self.first_num * self.second_num,
        )

    def render_problem(self, minipage, show_solution=False):
        top, op, bottom, *solution = map(str, self._problem_tuple())
        op_column = max(len(top), len(bottom)) + 1
        num_chars = max(op_column, len(str(int(top) * int(bottom))))

        minipage.append(NoEscape(r"\LARGE"))
        with minipage.create(Tabular(table_spec=r"p{1pt}" * num_chars)) as table:
            table.add_row(*tuple(_right_justify(top, num_chars)))
            table.add_row(
                *([""] * (num_chars - op_column)),
                NoEscape(fr"${op}$"),
                *tuple(_right_justify(bottom, (op_column - 1))),
            )
            table.add_hline()
            if show_solution:
                table.add_row(*tuple(_right_justify(*solution, num_chars)))


def _right_justify(string, width):
    return " " * (width - len(string)) + string
