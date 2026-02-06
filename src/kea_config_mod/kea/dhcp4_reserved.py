# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint disable=too-many-statements, too-many-locals
# pylint disable=duplicate-code

from kea_config_mod.data import KeaServer
from kea_config_mod.data import KeaNet


def dhcp4_write_reserved(server: KeaServer, net: KeaNet):
    """
    Write out the reserved hosts - mac and ip
    """

    if not net.reserved:
        return

    fob = server.fob_dhcp4

    if fob is None:
        return

    fob.write('\n')
    # fob.write('\t\t//\n')
    fob.write('\t\t// IP Host Reservations\n')
    # fob.write('\t\t//\n')

    fob.write('\n')

    fob.write('\t\t"reservations": [\n')

    first = True
    for (_name, reserved) in net.reserved.items():
        host = reserved.host
        ip = reserved.ip
        mac = reserved.hw_address
        fqdn = reserved.fqdn

        if not first:
            fob.write(',\n')
        else:
            first = False

        fob.write('\t\t{\n')
        if fqdn:
            fob.write(f'\t\t\t"hostname": "{fqdn}",\n')
        else:
            fob.write(f'\t\t\t"hostname": "{host}",\n')
        fob.write(f'\t\t\t"hw-address": "{mac}",\n')
        fob.write(f'\t\t\t"ip-address": "{ip}"\n')
        fob.write('\t\t}')

    fob.write('\n')
    fob.write('\t\t]\n')
