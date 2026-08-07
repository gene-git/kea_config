# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Project kea-config
"""
__version__ = "6.4.0"
__date__ = "2026-08-07"
__reldev__ = "release"


def version() -> str:
    """ report version and release date """
    vers = f'wg-client: version {__version__} ({__reldev__}, {__date__})'
    return vers
