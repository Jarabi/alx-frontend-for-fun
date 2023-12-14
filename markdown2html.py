#!/usr/bin/python3
"""
Receives two string arguments
"""
import os
import sys


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) < 2:
        err = "Usage: ./markdown2html.py README.md README.html"
        print(err, file=sys.stderr)
        exit(1)

    markdown_file = args[0]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)
