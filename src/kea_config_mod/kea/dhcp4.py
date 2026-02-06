# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint disable=too-many-statements, too-many-locals
# pylint disable=duplicate-code

from kea_config_mod.data import KeaData

from .dhcp4_top import dhcp4_write_top_section
from .dhcp4_hooks import dhcp4_write_hooks_libs
from .dhcp4_global import dhcp4_write_global_options
from .dhcp4_nets import dhcp4_write_subnets
from .dhcp4_loggers import dhcp4_write_loggers


def dhcp4_write(data: KeaData):
    """
    Write out the kea dhcp4 files
    """
    dhcp4_write_top_section(data)
    dhcp4_write_hooks_libs(data)
    dhcp4_write_global_options(data)
    dhcp4_write_subnets(data)
    dhcp4_write_loggers(data)
