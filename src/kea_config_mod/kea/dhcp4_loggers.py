# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint disable=too-many-statements, too-many-locals
# pylint disable=duplicate-code

from kea_config_mod.data import KeaData


def dhcp4_write_loggers(data: KeaData):
    """
    Write out the logging section
    """
    for (_stype, server) in data.servers.items():
        if not server.active:
            continue
        fob = server.fob_dhcp4
        if not fob:
            continue

        fob.write('\n')
        fob.write('\t"loggers": [\n')
        fob.write('\t{\n')
        fob.write('\t\t"name": "kea-dhcp4",\n')
        fob.write('\t\t"output_options": [\n')
        fob.write('\t\t{\n')
        fob.write('\t\t\t"output": "/var/log/kea/kea-dhcp4.log",\n')
        fob.write('\t\t\t"flush": false,\n')
        fob.write('\t\t\t"maxsize": 1048576,\n')
        fob.write('\t\t\t"maxver": 8\n')
        fob.write('\t\t}\n')
        fob.write('\t\t],\n')
        fob.write('\t\t"severity": "WARN",\n')
        fob.write('\t\t"debuglevel": 0\n')

        fob.write('\t}\n')
        fob.write('\t]\n')
        fob.write('}\n')
        fob.write('}\n')
