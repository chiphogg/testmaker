"""Generate multiplication tests."""

import argparse
import os
import pathlib
import sys

from pylatex import Document, Math, MiniPage, NoEscape, Section, Tabular


def main(argv):
    args = _parse_command_line_args(argv)

    doc = _create_test_document(num_cols=args.num_cols)

    sep = None
    for _ in range(args.num_rows):
        if sep:
            doc.append(sep)
        sep = NoEscape(r'\linebreak')

        for _ in range(args.num_cols):
            doc.append(
                    _generate_problem(
                        relative_width=1.0 / args.num_cols,
                        relative_height=1.0 / args.num_rows,
                        )
                    )

    _publish_document(doc, args.output_file)

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


def _create_test_document(num_cols):
    doc = Document(
            indent=False,
            page_numbers=False,
            geometry_options={
                'margin': NoEscape(r'0.5in'),
                },
            )

    return doc


def _generate_problem(relative_width, relative_height):
    table_spec = 'c@{}c@{}c@{}c@{}'
    minipage = MiniPage(
            width=r'{}\textwidth'.format(relative_width),
            height=r'{}\textheight'.format(relative_height * 0.99),
            align='c',
            pos='t',
            )

    minipage.append(NoEscape(r'\LARGE'))
    with minipage.create(
            Tabular(table_spec=table_spec),
            ) as table:
        table.add_row('', 3, 1, 4)
        table.add_row(NoEscape(r'$\times$'), '', 5, 7)
        table.add_hline()

    return minipage


def _publish_document(doc, output_file):
    _ensure_folder_exists(os.path.dirname(output_file))
    doc.generate_pdf(output_file)
    doc.generate_tex(output_file)


################################################################################
# Level 2


def _ensure_folder_exists(folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    sys.exit(main(argv=sys.argv))
