# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Command Line
"""
from typing import Any
import argparse


def options(config_file: str) -> dict[str, Any]:
    """
    Command line options
    """
    par = argparse.ArgumentParser(description='kea_config')

    par.add_argument(
            '-c', '--config',
            default=config_file,
            help=f'Config file ({config_file})'
            )

    parsed = par.parse_args()
    parsed_dict = vars(parsed)
    return parsed_dict
