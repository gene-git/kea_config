# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint disable=too-many-statements, too-many-locals
# pylint disable=duplicate-code

from kea_config_mod.data import KeaData

from .tools import list_to_strings


def dhcp4_write_global_options(data: KeaData):
    """
    write the global options part
    """
    opts_global = data.global_options
    if not opts_global:
        return

    domain_name: str = opts_global.domain_name

    #
    # map lists to comma separated strings
    #
    dns_servers = list_to_strings(opts_global.domain_name_servers)
    dns_search = list_to_strings(opts_global.domain_search)
    ntp_servers = list_to_strings(opts_global.ntp_servers)

    for (stype, server) in data.servers.items():
        if not server.active:
            continue

        fob = server.fob_dhcp4
        if not fob:
            print(f'Error missing file object for server {stype}')
            continue

        #
        # can be:
        # "hw-address", "duid", "circuit-id", "client-id", "flex-id"
        #
        fob.write('\n')
        fob.write('\t"host-reservation-identifiers": [\n')
        fob.write('\t\t"hw-address"\n')
        fob.write('\t],')

        fob.write('\n')
        fob.write('\t"option-data" : [\n')
        if dns_servers:
            fob.write('\t{\n')
            fob.write('\t\t"name" : "domain-name-servers",\n')
            fob.write('\t\t"data" : ' + dns_servers + '\n')
            fob.write('\t}')

        if domain_name:
            fob.write(',\n')
            fob.write('\t{\n')
            fob.write('\t\t"name" : "domain-name",\n')
            fob.write('\t\t"data" : "' + domain_name + '"\n')
            fob.write('\t}')

        if dns_search:
            fob.write(',\n')
            fob.write('\t{\n')
            fob.write('\t\t"name" : "domain-search",\n')
            fob.write('\t\t"data" : ' + dns_search + '\n')
            fob.write('\t}')

        if ntp_servers:
            fob.write(',\n')
            fob.write('\t{\n')
            fob.write('\t\t"name" : "ntp-servers",\n')
            fob.write(f'\t\t"data" : {ntp_servers}\n')
            fob.write('\t}\n')
        fob.write('\n')
        fob.write('\t],\n')
