# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for kea configurator
"""
from typing import IO


def list_to_strings(vec: list[str]) -> str:
    """
    list_to_strings()
    Kea needs some things as list inside quotes: "aaa, nnn, ccc, ..."
    convert python list to this format
    """
    strings: str = ''

    if not isinstance(vec, list):
        return f'"{vec}"'

    for elem in vec:
        if strings:
            strings += ', ' + elem
        else:
            strings = elem

    strings = '"' + strings + '"'
    return strings


def open_file(path: str, mode: str) -> IO | None:
    """
    Open a file and return file object
    """
    # pylint: disable=unspecified-encoding, consider-using-with
    try:
        fob = open(path, mode)
        return fob

    except OSError as err:
        print(f'Error opening file {path} : {err}')
        return None
