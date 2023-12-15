#!/usr/bin/python3
"""
Receives two string arguments
"""
import os
import sys


def create_heading(line, htmlfile):
    """
    Parses Headings Markdown syntax for generating HTML
    """
    count = 0

    while count < len(line) and line[count] == '#':
        count += 1

    if line[count] == ' ':
        heading_text = line[count + 1:]

        htmlfile.write(f'<h{count}>{heading_text}</h{count}>\n')


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) < 2:
        err = "Usage: ./markdown2html.py README.md README.html"
        print(err, file=sys.stderr)
        exit(1)

    markdown_file = args[0]
    html_file = args[1]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)

    # Flag to track opening and closing of list items
    list_started = False

    with open(markdown_file) as mdfile:
        with open(html_file, 'a') as htmlfile:

            for line in mdfile:
                # Remove leading/trailing spaces
                line = line.strip()

                if line.startswith('#'):
                    create_heading(line, htmlfile)

                elif line.startswith('- '):
                    if not list_started:
                        htmlfile.write('<ul>\n')
                        list_started = True

                    ultext = line[2:]
                    htmlfile.write(f'\t<li>{ultext}</li>\n')

            if list_started:
                htmlfile.write('</ul>\n')
