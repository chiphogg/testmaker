"""Generate multiplication tests."""

import argparse
import os
import pathlib
import random
import sys

from pylatex import Command, Document, MiniPage, NoEscape, Tabular

from multiplication_problem import MultiplicationProblemFactory


def main(argv):
    args = _parse_command_line_args(argv)

    doc = _create_test_document(args)

    problems = _generate_problems(args)
    _layout_problems(problems, doc, args)

    _publish_document(doc, args)

    return 0


################################################################################
# Level 1


def _parse_command_line_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--num-cols", type=int, default=4,
    )

    parser.add_argument(
        "--num-rows", type=int, default=5,
    )

    parser.add_argument(
        "--output-file", default="output/test",
    )

    parser.add_argument(
        "--seed", default=1, type=int,
    )

    parser.add_argument(
        "--first-digits", default=3, type=int,
    )

    parser.add_argument(
        "--second-digits", default=2, type=int,
    )

    parser.add_argument("--override-max", type=int)

    return parser.parse_args()


def _create_test_document(args):
    doc = Document(
        indent=False,
        page_numbers=False,
        textcomp=False,
        geometry_options={"margin": NoEscape(r"0.5in"),},
    )
    doc.preamble.append(Command("usepackage", "kpfonts"))

    return doc


def _generate_problems(args):
    random.seed(args.seed)
    factory = MultiplicationProblemFactory(args=args)
    return (factory.generate_problem() for _ in range(args.num_rows * args.num_cols))


def _layout_problems(problems, doc, args):
    problem_page = _make_full_page_minipage()
    solution_page = _make_full_page_minipage()

    for (problem, layout) in zip(problems, _problem_layoutters(args)):
        layout(problem.get_problem(), problem_page)
        layout(problem.get_solution(), solution_page)

    doc.append(problem_page)
    doc.append(NoEscape(r"\linebreak"))
    doc.append(solution_page)


def _publish_document(doc, args):
    _ensure_folder_exists(os.path.dirname(args.output_file))
    doc.generate_pdf(args.output_file)
    doc.generate_tex(args.output_file)


################################################################################
# Level 2


def _make_full_page_minipage():
    return MiniPage(width=r"\textwidth", height=r"\textheight")


def _problem_layoutters(args):
    for row in range(args.num_rows):
        for col in range(args.num_cols):

            def func(p, doc):
                if row > 0 and col == 0:
                    doc.append(NoEscape(r"\linebreak"))
                doc.append(
                    _layout_problem(
                        p,
                        relative_width=1.0 / args.num_cols,
                        relative_height=1.0 / args.num_rows,
                    ),
                )

            yield func


def _ensure_folder_exists(folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)


################################################################################
# Level 3


def _layout_problem(problem, relative_width, relative_height):
    top, op, bottom, *solution = map(str, problem)
    op_column = max(len(top), len(bottom)) + 1
    num_chars = max(op_column, len(str(int(top) * int(bottom))))

    minipage = MiniPage(
        width=fr"{relative_width}\textwidth",
        height=fr"{relative_height * 0.99}\textheight",
        align="c",
        pos="t",
    )

    minipage.append(NoEscape(r"\LARGE"))
    with minipage.create(Tabular(table_spec=r"p{1pt}" * num_chars)) as table:
        table.add_row(*tuple(_right_justify(top, num_chars)))
        table.add_row(
            *([""] * (num_chars - op_column)),
            NoEscape(fr"${op}$"),
            *tuple(_right_justify(bottom, (op_column - 1))),
        )
        table.add_hline()
        if solution:
            table.add_row(*tuple(_right_justify(*solution, num_chars)))

    return minipage


################################################################################
# Level 4


def _right_justify(string, width):
    return " " * (width - len(string)) + string


################################################################################
# Main logic


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv))
