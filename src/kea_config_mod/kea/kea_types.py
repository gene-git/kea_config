# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Shared types
"""
from typing import IO

#
# Multiple file objects by name
#
type FobConf = dict[str, IO | None]
