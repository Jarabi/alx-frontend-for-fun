#!/usr/bin/python3
"""
Receives two string arguments
"""
import os
import sys

def create_headings(line, htmlfile):
    count = 0
    
    while count < len(line) and line[count] == '#':
        count += 1
    
    if line[count] == ' ':
        headingtext = line[count + 1:]
        
        with open(htmlfile, 'a') as file:
            file.write(f'<h{count}>{headingtext}</h{count}>\n')


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) < 2:
        err = "Usage: ./markdown2html.py README.md README.html"
        print(err, file=sys.stderr)
        exit(1)

    markdownfile = args[0]
    htmlfile = args[1]

    if not os.path.isfile(markdownfile):
        print(f"Missing {markdownfile}", file=sys.stderr)
        exit(1)

    with open(markdownfile) as file:
        for line in file:
            # Remove leading/trailing spaces
            line = line.strip()

            if line.startswith('#'):
                create_headings(line, htmlfile)
