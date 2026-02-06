# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 dhcp4 part of kea config generator
 Write out the configs
"""
# pylint: disable=too-many-statements, too-many-locals
# pylint disable=too-many-statements
from kea_config_mod.data import KeaData
from kea_config_mod.data import KeaNet
from kea_config_mod.data import KeaServer

from .dhcp4_reserved import dhcp4_write_reserved
from .tools import list_to_strings


def _write_one_net(server: KeaServer, net: KeaNet):
    """
    Write out one subnet
    """
    #
    # handle multiple pool ranges in a subnet
    # pools: [{"pool": "range 1"}, {"pool": "range 2"}]
    #
    # multiple nets - each net needs 1 interface it applies to
    # subnet_id is unique to each subnet - caller increments for each subnet
    #
    # subdomain = net.subdomain
    subnet = net.subnet
    subnet_id = net.subnet_id
    fob = server.fob_dhcp4

    if fob is None:
        return

    iface = server.get_iface(subnet)
    if not iface:
        # this server does not handle this subnet
        return

    #
    # Check if this server supports this subnet
    #

    lifetime = net.valid_lifetime
    min_lifetime = net.min_valid_lifetime
    max_lifetime = net.max_valid_lifetime

    option_data = net.option_data
    bcast = option_data.broadcast_address
    ntp = option_data.ntp_servers
    ntp_servers = list_to_strings(ntp)
    routers = ''
    routers = list_to_strings(option_data.routers)

    #
    # format pool ranges into kea format
    #
    pool_info = ''
    for item in net.pools:
        if pool_info:
            pool_info = pool_info + f', {{"pool": "{item}"}}'
        else:
            pool_info = f'{{"pool": "{item}"}}'

    fob.write('\t{\n')
    fob.write(f'\t\t// network {subnet_id}\n')
    fob.write(f'\t\t"id": {subnet_id},\n')
    fob.write(f'\t\t"subnet": "{subnet}",\n')
    fob.write(f'\t\t"pools": [{pool_info}],\n')

    if min_lifetime > 0:
        fob.write(f'\t\t"min-valid-lifetime": {min_lifetime},\n')
    if lifetime > 0:
        fob.write(f'\t\t"valid-lifetime": {lifetime},\n')
    if max_lifetime > 0:
        fob.write(f'\t\t"max-valid-lifetime": {max_lifetime},\n')

    fob.write('\t\t"authoritative": true,\n')
    fob.write(f'\t\t"interface": "{iface}",\n')

    if option_data:
        fob.write('\t\t"option-data":[\n')

        fob.write('\t\t{\n')
        fob.write('\t\t\t"space": "dhcp4",\n')
        fob.write('\t\t\t"name": "broadcast-address",\n')
        fob.write(f'\t\t\t"data" : "{bcast}"\n')
        fob.write('\t\t},\n')

        fob.write('\t\t{\n')
        fob.write('\t\t\t"space": "dhcp4",\n')

        fob.write('\t\t\t"name": "routers",\n')
        fob.write(f'\t\t\t"data" : {routers}\n')
        fob.write('\t\t},\n')

        fob.write('\t\t{\n')
        fob.write('\t\t\t"space": "dhcp4",\n')
        fob.write('\t\t\t"name": "ntp-servers",\n')
        fob.write(f'\t\t\t"data" : {ntp_servers}\n')
        fob.write('\t\t}\n')

        fob.write('\t\t],\n')

    #
    # Write any ip host reservations
    #
    dhcp4_write_reserved(server, net)

    # fob.write('\t}\n')
    fob.write('\t}')


def dhcp4_write_subnets(data: KeaData):
    """
    Write out the subnet (we handle 1 subnet currently.
    """
    # pylint: disable=
    #
    # handle multiple pool ranges in a subnet
    # pools: [{"pool": "range 1"}, {"pool": "range 2"}]
    #
    # multiple nets - each net needs 1 interface it applies to
    #
    for (_stype, server) in data.servers.items():
        fob = server.fob_dhcp4
        if fob is None:
            continue

        fob.write('\n')
        fob.write('\t//\n')
        fob.write('\t// IPv4 subnets\n')
        fob.write('\t//\n')
        fob.write('\t"subnet4": [\n')

        net_count: int = 0
        for (subnet, net) in data.nets.items():
            #
            # Does this server support this net
            # If so,  which network interface
            #
            # subnet :== net.subnet
            iface = server.get_iface(subnet)
            if not iface:
                # this network not applicable for this server
                continue

            # each net elem in array ends with a comma
            if net_count > 0:
                fob.write(',\n')

            net_count += 1
            net.subnet_id = net_count

            _write_one_net(server, net)

        fob.write('\n\t],\n')
