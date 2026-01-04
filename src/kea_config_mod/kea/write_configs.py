# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Write kea dhcp4 configs
"""

from .agent import write_ctrl_agent
from .dhcp4 import dhcp4_write_top_section
from .dhcp4 import dhcp4_write_hooks_libs
from .dhcp4 import dhcp4_write_global_options
from .dhcp4 import dhcp4_write_subnets
from .dhcp4 import dhcp4_write_reserved
from .dhcp4 import dhcp4_write_loggers
from .kea_data import KeaConfigData
from .tools import open_file

from .kea_types import FobConf


def _open_output_files(conf: KeaConfigData) -> tuple[FobConf, FobConf]:
    """
    Open the kea config files for writing
    """
    conf_base = conf.conf_base
    agent_base = conf.agent_base

    fob_conf: FobConf = {}
    fob_agent: FobConf = {}

    for stype in conf.server_types:
        fob_conf[stype] = None
        fob_agent[stype] = None

        fname = f'{conf_base}-{stype}.conf'
        fob_conf[stype] = open_file(fname, 'w')

        fname = f'{agent_base}-{stype}.conf'
        fob_agent[stype] = open_file(fname, 'w')

    return (fob_conf, fob_agent)


def _close_output_files(fob_conf: FobConf):
    """
    Close the file object.
    """
    if not fob_conf:
        return

    for (_stype, fob) in fob_conf.items():
        if fob:
            fob.close()


def write_configs(conf: KeaConfigData):
    """
    Write out all config sections
    """
    (fob_conf, fob_agent) = _open_output_files(conf)

    #
    # Write the dhcp4 configs
    #
    dhcp4_write_top_section(conf, fob_conf)
    dhcp4_write_hooks_libs(conf, fob_conf)
    dhcp4_write_global_options(conf, fob_conf)
    dhcp4_write_subnets(conf,  fob_conf)
    dhcp4_write_reserved(conf, fob_conf)
    dhcp4_write_loggers(conf, fob_conf)

    #
    # Write the control agent configs
    #
    write_ctrl_agent(conf, fob_agent)

    _close_output_files(fob_conf)
    _close_output_files(fob_agent)
