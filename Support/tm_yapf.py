# -*- coding: utf-8 -*-

import os, re
from sys import stdout, stdin, exit, argv
from yapf.yapflib.yapf_api import FormatCode

source = stdin.read()
use_tabs = os.environ['TM_SOFT_TABS'] == 'NO'
soft_tab_size = os.environ['TM_TAB_SIZE']
filename = os.environ['TM_FILENAME']  # For showing the filename in the diff
lines_selected = None
print_diff = False

if use_tabs:
    indent_width = 1
else:
    indent_width = soft_tab_size

continuation_indent_width = indent_width

# $TM_SELECTION indicates the range of the current selection.
#
# Example value: "19:12-21:19"
#
# YAPF supports formatting only the selected lines with its
# lines-parameter.
#
# We strip the character indices as they are supported.
if 'TM_SELECTED_TEXT' in os.environ and 'TM_SELECTION' in os.environ:
    match = re.search(r'(\d+):*\d*-(\d*):*', os.environ['TM_SELECTION'])

    if match:
        lines_selected = [tuple(int(g) for g in match.groups())]

style_config = {
    'use_tabs': use_tabs,
    'dedent_closing_brackets': True,
    'indent_width': indent_width,
    'continuation_indent_width': continuation_indent_width,
}

if len(argv) > 1:
    if argv[1] == '--reformat_vertically':
        style_config.update({'column_limit': 1})
    if argv[1] == '--reformat_diff':
        print_diff = True

try:
    result = FormatCode(
        source,
        style_config=style_config,
        print_diff=print_diff,
        filename=filename,
        lines=lines_selected
    )
except:
    stdout.write("Error: \n%s" % result[1])
    exit(206)  # exiting with this code show's output in a tooltip
else:
    stdout.write(result[0])