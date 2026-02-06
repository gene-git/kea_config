# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
yaml helper functions
- yaml handles None values as "null"
- we can keep or strip from dictionary
"""
# pylint disable=duplicate-code
from typing import (Any)
from io import StringIO
from ruamel.yaml import (YAML, YAMLError)


from .read_write import (write_path_atomic)
from .read_write import read_file_path
from .file_tidy import dict_remove_none


def dict_to_yaml_string(dic: dict[str, Any],
                        flow_style: bool | None = False,
                        drop_empty: bool = False
                        ) -> str:
    """
    Returns a yaml formatted string from a dictionary
      - drop_empty: Keys with None values are removed/ignored
     - default_flow_style :
        False (Default): Forces all collections to use block style.
        True: Forces all collections to use JSON-style flow, with brackets and braces.
        None: Uses flow style for simple collections (only scalar values) and
              block style for nested collections.
        round_trip_mode: Preserves the existing flow/block style of the input YAML,
              which is the primary feature of ruamel.yaml.
        Individual Flow Control: To force a specific list or dictionary to be in flow style
              while others remain in block, set_flow_style() can be applied to specific
              CommentedSeq or CommentedMap objects.
     - Configure indentation:
        - mapping: indent of block mappings (dictionaries)
        - sequence: indent of block sequences (lists)
        - offset: offset of the dash '-' within the sequence indentation

    """
    clean_dict = dic.copy()
    if drop_empty:
        clean_dict = dict_remove_none(dic)

    yaml = YAML()
    try:
        yaml.explicit_start = True
        yaml.indent(mapping=2, sequence=2, offset=2)
        yaml.default_flow_style = flow_style

        with StringIO() as string_stream:
            yaml.dump(clean_dict, string_stream)
            txt = string_stream.getvalue()

    except YAMLError as _exc:
        # print(f' Error yaml.dump: {_exc}')
        pass
    return txt


def read_yaml_file(fpath: str) -> dict[str, Any]:
    """
    read yaml file and return a dictionary
    """
    this_dict: dict[str, Any] = {}
    data: str = ''
    data = read_file_path(fpath)
    if data:
        try:
            yaml = YAML()
            this_dict = yaml.load(data)
        except YAMLError as _exc:
            # print(f'File format error {_exc}')
            this_dict = {}
    return this_dict


def write_yaml_file(dic: dict[str, Any], fpath: str, flow_style: bool = False
                    ) -> bool:
    """
    write yaml file and return success/fail
    flow style defaults to block
    """
    okay = True
    if not dic or not fpath:
        return okay

    txt = dict_to_yaml_string(dic, flow_style=flow_style)

    if txt and not write_path_atomic(txt, fpath):
        okay = False
    return okay
