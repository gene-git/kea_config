# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Support tools for kea configurator
"""

def list_to_strings (vec):
    """
    list_to_strings()
    Kea needs some things as list inside quotes: "aaa, nnn, ccc, ..."
    convert python list to this format
    """
    strings = None

    if not isinstance(vec, list):
        return f'"{vec}"'

    first = True
    for elem in vec:
        if first:
            strings = '"' + elem
            first = False
        else:
            strings = strings + ', ' + elem

    if not first:
        strings = strings + '"'

    return strings

def open_file(path, mode):
    """
    Open a file and return file object
    """
    # pylint: disable=W1514,R1732
    try:
        fobj = open(path, mode)
    except OSError as err:
        print(f'Error opening file {path} : {err}')
        fobj = None
    return fobj
