"""Generate multiplication tests."""

import argparse
import os
import pathlib
import sys

from pylatex import Document, MiniPage, NoEscape, Tabular


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
            '--num-cols',
            default=5,
            )

    parser.add_argument(
            '--num-rows',
            default=6,
            )

    parser.add_argument(
            '--output-file',
            default='output/test',
            )

    return parser.parse_args()


def _create_test_document(args):
    doc = Document(
            indent=False,
            page_numbers=False,
            geometry_options={
                'margin': NoEscape(r'0.5in'),
                },
            )

    return doc


def _generate_problems(args):
    return ((314, r'\times', 57) for _ in range(args.num_rows * args.num_cols))


def _layout_problems(problems, doc, args):
    sep = None
    for _ in range(args.num_rows):
        if sep:
            doc.append(sep)
        sep = NoEscape(r'\linebreak')

        for _ in range(args.num_cols):
            doc.append(
                    _layout_problem(
                        problem=next(problems),
                        relative_width=1.0 / args.num_cols,
                        relative_height=1.0 / args.num_rows,
                        )
                    )


def _layout_problem(problem, relative_width, relative_height):
    top, op, bottom = map(str, problem)
    width = max(len(top), len(bottom)) + 1

    minipage = MiniPage(
            width=r'{}\textwidth'.format(relative_width),
            height=r'{}\textheight'.format(relative_height * 0.99),
            align='c',
            pos='t',
            )

    minipage.append(NoEscape(r'\LARGE'))
    with minipage.create(
            Tabular(table_spec='c@{}' * width),
            ) as table:
        table.add_row(*tuple(_right_justify(top, width)))
        table.add_row(
                NoEscape(r'${}$'.format(op)),
                *tuple(_right_justify(bottom, (width - 1))),
                )
        table.add_hline()

    return minipage


def _right_justify(string, width):
    return ' ' * (width - len(string)) + string


def _publish_document(doc, args):
    _ensure_folder_exists(os.path.dirname(args.output_file))
    doc.generate_pdf(args.output_file)
    doc.generate_tex(args.output_file)


################################################################################
# Level 2


def _ensure_folder_exists(folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    sys.exit(main(argv=sys.argv))
