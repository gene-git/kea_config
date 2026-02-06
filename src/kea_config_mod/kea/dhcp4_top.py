# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint: disable=too-many-statements
# pylint: disable=duplicate-code

from kea_config_mod.data import KeaData

from .tools import list_to_strings


def dhcp4_write_top_section(data: KeaData):
    """
    Write out the top of configs
    """
    title = ''
    if data.title:
        title = data.title

    now = data.now

    glob_opts = data.global_options
    lifetime = glob_opts.valid_lifetime
    min_lifetime = glob_opts.min_valid_lifetime
    max_lifetime = glob_opts.max_valid_lifetime

    socket_dir = data.socket_dir

    for (stype, server) in data.servers.items():
        if not server.active:
            continue

        fob = server.fob_dhcp4
        if not fob:
            continue

        ifaces_list = [item[0] for item in server.interfaces]
        ifaces = list_to_strings(ifaces_list)

        hostname = server.hostname

        fob.write('//\n')
        fob.write(f'// Kea Config : {hostname}\n')
        fob.write(f'//    Title : {title}\n')
        fob.write(f'// Server type : {stype}\n')
        fob.write(f'// Generated at : {now}\n')
        fob.write('//\n')

        fob.write('\n')
        fob.write('{\n')
        fob.write('"Dhcp4": {\n')
        fob.write('\t"authoritative": true,\n')
        fob.write('\t"interfaces-config":\n')
        fob.write('\t{\n')
        fob.write(f'\t\t"interfaces": [{ifaces}],\n')
        fob.write('\t\t"dhcp-socket-type": "raw" \n')
        fob.write('\t},\n')

        fob.write('\n')
        fob.write('\t"control-socket": {\n')
        fob.write('\t\t"socket-type": "unix",\n')
        fob.write(f'\t\t"socket-name": "{socket_dir}/kea4-ctrl-socket"\n')
        fob.write('\t},\n')

        fob.write('\t"lease-database": {\n')
        fob.write('\t\t"type": "memfile",\n')
        fob.write('\t\t"persist": true,\n')
        fob.write('\t\t"name": "/var/lib/kea/kea-leases4.csv",\n')
        fob.write('\t\t"lfc-interval": 3600\n')
        fob.write('\t},\n')

        fob.write('\t"expired-leases-processing": {\n')
        fob.write('\t\t"reclaim-timer-wait-time": 10,\n')
        fob.write('\t\t"flush-reclaimed-timer-wait-time": 25,\n')
        fob.write('\t\t"hold-reclaimed-time": 3600,\n')
        fob.write('\t\t"max-reclaim-leases": 100,\n')
        fob.write('\t\t"max-reclaim-time": 250,\n')
        fob.write('\t\t"unwarned-reclaim-cycles": 5\n')
        fob.write('\t},\n')

        fob.write('\t"calculate-tee-times": true,\n')
        fob.write('\t"offer-lifetime": 60,\n')

        if min_lifetime:
            fob.write(f'\t"min-valid-lifetime": {min_lifetime},\n')
        if lifetime:
            fob.write(f'\t"valid-lifetime": {lifetime},\n')
        if lifetime:
            fob.write(f'\t"max-valid-lifetime": {max_lifetime},\n')
