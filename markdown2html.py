#!/usr/bin/python3
"""
Receives two string arguments
"""
import os
import sys


def create_heading(line, htmlfile):
    """
    Parses Headings Markdown syntax for generating HTML

    args:
        line (string): String of text to transform to header
        htmlfile (file descriptor): file descriptor
    """
    # Remove leading/trailing spaces
    line = line.strip()
    count = 0

    while count < len(line) and line[count] == '#':
        count += 1

    if line[count] == ' ':
        heading_text = line[count + 1:]

        htmlfile.write(f'<h{count}>{heading_text}</h{count}>\n')


def bold_emphasis(line, markdown):
    """
    Transforms text to bold or emphasis based on specified string

    Args:
        line (string): Text string to convert to bold or emphasis
        markdown (string): Can be '**' for bold or '__' for emphasis

    Return: Modified text
    """
    parts = line.split(markdown)
    tag = 'b' if markdown == '**' else 'em'

    for index in range(1, len(parts), 2):
        parts[index] = f'<{tag}>{parts[index]}</{tag}>'

    modified_line = ''.join(parts)

    return modified_line


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

    with open(markdown_file) as mdfile:
        with open(html_file, 'a') as htmlfile:
            # Flag to track opening and closing of list items
            list_started = False

            # Flag to track opening and closing of paragraph
            paragraph_started = False

            # Holds either OL or UL
            list_type = ''

            for line in mdfile:
                # Heading section
                if line.startswith('#'):
                    # If there is an open list, close it first
                    if list_started:
                        htmlfile.write(f'</{list_type}>\n')
                        list_started = False

                    # If there is an open paragraph, close it first
                    if paragraph_started:
                        htmlfile.write('</p>\n')
                        paragraph_started = False

                    create_heading(line, htmlfile)

                # Listing section
                elif line.startswith('- ') or line.startswith('* '):
                    # If there is an open paragraph, close it first
                    if paragraph_started:
                        htmlfile.write('</p>\n')
                        paragraph_started = False

                    # Remove leading/trailing spaces
                    line = line.strip()

                    if line.startswith('- '):
                        list_type = 'ul'
                    elif line.startswith('* '):
                        list_type = 'ol'

                    ultext = line[2:]

                    if not list_started:
                        htmlfile.write(f'<{list_type}>\n')
                        list_started = True

                    if '**' in ultext:
                        bold_text = bold_emphasis(ultext, '**')
                        htmlfile.write(f'<li>{bold_text}</li>\n')
                    elif '__' in ultext:
                        em_text = bold_emphasis(ultext, '__')
                        htmlfile.write(f'<li>{em_text}</li>\n')
                    else:
                        htmlfile.write(f'<li>{ultext}</li>\n')

                # Paragraph section
                elif (line and line[0].isalpha()) or line.isspace()\
                    or line.startswith('**') or line.startswith('__'):
                    # If there is an open list, close it first
                    if list_started:
                        htmlfile.write(f'</{list_type}>\n')
                        list_started = False

                    if not paragraph_started:
                        if not line.isspace():
                            paragraph_started = True
                            htmlfile.write('<p>\n')
                    elif paragraph_started:
                        if line.isspace():
                            htmlfile.write('\n</p>\n')
                            paragraph_started = False
                        else:
                            htmlfile.write('\n<br/>\n')

                    line = line.strip()

                    if '**' in line:
                        bold_text = bold_emphasis(line, '**')
                        htmlfile.write(bold_text)
                    elif '__' in line:
                        em_text = bold_emphasis(line, '__')
                        htmlfile.write(em_text)
                    else:
                        htmlfile.write(line)

            if list_started:
                htmlfile.write(f'</{list_type}>\n')

            if paragraph_started:
                htmlfile.write('\n</p>\n')