# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
toml support
"""
from typing import (Any)
import os
import tomllib as toml


def read_toml_file(fpath: str) -> dict[str, Any]:
    """
    read toml file and return a dictionary
    """
    this_dict: dict[str, Any] = {}
    if not fpath:
        return this_dict

    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf=8') as fob:
            data = fob.read()
            try:
                this_dict = toml.loads(data)
            except toml.TOMLDecodeError:
                this_dict = {}
    return this_dict
