# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint: disable=duplicate-code
from kea_config_mod.data import KeaData

from .dhcp4_peers import dhcp4_write_peers


def dhcp4_write_hooks_libs(data: KeaData):
    """
    Write out the hooks library section
    """
    lib: str = ''

    for (stype, server) in data.servers.items():
        if not server.active:
            continue

        fob = server.fob_dhcp4
        if not fob:
            continue

        name = f'kea-{stype}'

        fob.write('\n')
        fob.write('\t//\n')
        fob.write('\t// Hooks\n')
        fob.write('\t//')

        lib = '/usr/lib/kea/hooks/libdhcp_lease_cmds.so'
        fob.write('\n\t"hooks-libraries": [')
        fob.write('\n\t\t{')
        fob.write(f'\n\t\t\t"library": "{lib}",')
        fob.write('\n\t\t\t"parameters": { }')
        fob.write('\n\t\t}')

        if data.has_standby:
            lib = '/usr/lib/kea/hooks/libdhcp_ha.so'
            fob.write(',')
            fob.write('\n\t\t{')
            fob.write(f'\n\t\t\t"library": "{lib}",')
            fob.write('\n\t\t\t"parameters": {')
            fob.write('\n\t\t\t"high-availability": [')
            fob.write('\n\t\t\t{')
            fob.write(f'\n\t\t\t\t"this-server-name": "{name}",')
            fob.write('\n\t\t\t\t"mode": "hot-standby",')
            fob.write('\n\t\t\t\t"heartbeat-delay": 10000,')
            fob.write('\n\t\t\t\t"max-response-delay": 10000,')
            fob.write('\n\t\t\t\t"max-ack-delay": 5000,')
            fob.write('\n\t\t\t\t"max-unacked-clients": 5,')
            fob.write('\n\t\t\t\t"sync-timeout": 60000,')

            dhcp4_write_peers(data, fob)

            fob.write('\n\t\t\t}')
            fob.write('\n\t\t\t]')       # high avail
            fob.write('\n\t\t}')

            fob.write('\n\t}')
        fob.write('\n\t],')
