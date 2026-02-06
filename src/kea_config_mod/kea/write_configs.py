# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Write kea dhcp4 configs
"""
import os

from kea_config_mod.data import KeaData
from kea_config_mod.utils import open_file
from kea_config_mod.utils import os_move

from .agent import write_ctrl_agent
from .dhcp4 import dhcp4_write


def _open_output_files(data: KeaData) -> bool:
    """
    Open the kea config files for writing
    Make 1 backup into Prev subdirectory.
    """
    conf_base = data.conf_base
    agent_base = data.agent_base
    conf_dir_bakup = data.conf_dir_bakup

    for (stype, server) in data.servers.items():
        if not server.active:
            continue
        #
        # kea-dhcp4
        # - backup old and open new
        #
        fname = f'{conf_base}-{stype}.conf'

        if os.path.isfile(fname) and not os_move(fname, conf_dir_bakup):
            print(f'Error making backup of {fname} in {conf_dir_bakup}')
            return False

        server.fob_dhcp4 = open_file(fname, 'w')
        if not server.fob_dhcp4:
            print(f'Error opening file {fname}')
            return False
        #
        # kea-ctrl-agent
        # - backup old and open new
        #
        fname = f'{agent_base}-{stype}.conf'

        if os.path.isfile(fname) and not os_move(fname, conf_dir_bakup):
            print(f'Error making backup of {fname} in {conf_dir_bakup}')
            return False

        server.fob_agent = open_file(fname, 'w')
        if not server.fob_agent:
            print(f'Error opening file {fname}')
            return False

    return True


def _close_output_files(data: KeaData):
    """
    Close the file objects.
    """
    for (_stype, server) in data.servers.items():
        server.close_files()


def write_configs(data: KeaData) -> bool:
    """
    Write out all config sections
    """
    if not _open_output_files(data):
        return False

    #
    # Write the dhcp4 and control agent configs
    #
    dhcp4_write(data)
    write_ctrl_agent(data)

    _close_output_files(data)
    return True
