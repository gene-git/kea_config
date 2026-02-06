# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint disable=too-many-statements, too-many-locals
# pylint disable=duplicate-code
from typing import IO

from kea_config_mod.data import KeaData


def dhcp4_write_peers(data: KeaData, fob: IO):
    """
    Write out the server section (the peers)
    """
    num_peers = len(data.servers)

    fob.write('\n\t\t\t\t"peers": [')
    count = 1
    for (stype, server) in data.servers.items():
        if not server.active:
            continue

        if stype == 'backup':
            failover = 'false'
        else:
            failover = 'true'

        name = f'kea-{stype}'

        ip = server.ip
        port = server.port
        url = f'http://{ip}:{port}'
        role = stype

        auth_user = server.auth_user
        auth_pass = server.auth_password

        fob.write('\n\t\t\t\t{')
        fob.write(f'\n\t\t\t\t\t"name": "{name}",')
        fob.write(f'\n\t\t\t\t\t"url": "{url}",')
        fob.write(f'\n\t\t\t\t\t"basic-auth-user": "{auth_user}",')
        fob.write(f'\n\t\t\t\t\t"basic-auth-password": "{auth_pass}",')
        fob.write(f'\n\t\t\t\t\t"role": "{role}",')
        fob.write(f'\n\t\t\t\t\t"auto-failover": {failover}\n')
        fob.write('\n\t\t\t\t}')

        if count < num_peers:
            fob.write(',')
        count = count + 1

    fob.write('\n\t\t\t\t]')
