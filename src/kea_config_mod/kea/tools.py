# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for kea configurator
"""


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
