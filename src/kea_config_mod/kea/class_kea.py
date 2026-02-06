# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 kea config tool
 Tools to generate kea-dhcp4 server configs
 Driven by toml config file
 gc    2022-03-03
"""
# pylint: disable=

from kea_config_mod.data import KeaData
from kea_config_mod.data import KeaNet
from kea_config_mod.dns import Dns

from .write_configs import write_configs


def _config_servers(data: KeaData):
    """
    Split out the server info from config
    """
    okay = True
    ips: list[str] = []

    dummy_ip: str = '10.1.2.3:8761", \t# *** Error: Fix DNS IP for server hostname'

    for (_stype, server) in data.servers.items():
        if not server:
            continue

        hostname = server.hostname
        ips = data.dns.query(hostname)
        if not ips:
            print(f'DNS error: no IP for host : {hostname}')
            # okay = False
            server.ip = dummy_ip
        else:
            server.ip = ips[0]
            if len(ips) > 1:
                print(f'Warning: {hostname} has multiple ips ({ips})')
                print('  Using the first one')

    return okay


def _config_network(kea_net: KeaNet, dns: Dns):
    """
    Network info from config
    """
    if not kea_net:
        print('Error: missing a net section')
        return False

    if not kea_net.subnet:
        print('Error: net section missing subnet')
        return False

    #
    # Inherit any relevant/appropriate global options if not set in net
    #
    if not kea_net.reserved:
        return True

    #
    # Host reservations
    #
    if not kea_net.subdomain:
        txt = 'host reservations require "subdomain (aka dns_net)" in *net* section'
        print(f'Error: {txt}')
        return False

    okay: bool = True
    dummy_ip = '10.1.2.3", \t\t\t# *** Error: Fix DNS to provide correct IP address'

    for (host, reserved) in kea_net.reserved.items():
        ips = dns.query(reserved.fqdn)

        if not ips:
            print(f'DNS error: no IP for host : {reserved.fqdn}')
            ips = [dummy_ip]

        elif len(ips) > 1:
            print(f'Warning multiple ips for {reserved.fqdn} ({ips})')
            print('  using first')
        reserved.ip = ips[0]

        if reserved.ip_address:
            if not reserved.ip:
                reserved.ip = reserved.ip_address
                print(f'Using provided IP {reserved.ip}')
            elif reserved.ip_address != reserved.ip:
                txt = f'({reserved.ip_address}) not same as dns ({reserved.ip})'
                print(f'Warning {host} ip address: {txt}')
                print(f'Using value from DNS : {reserved.ip}')

        if not reserved.ip:
            # dummy should prevent this code
            print(f'Missing ip for host reservation {host}')
            reserved.ip = dummy_ip
            okay = False

    return okay


class KeaConfig(KeaData):
    """
    Tools to generate kea-dhcp4 server configs.
    Generates primary, standby and backup configs.
    """
    # def dns_query(self, query: str, rr_type: str = 'A', one_rr: bool = True):
    #     """
    #     dns query - used to map hostnames to ips
    #     """
    #     self.dns.query(query, rr_type=rr_type, one_rr=one_rr)

    def config_setup(self):
        """
        Prep the config information so have info needed to write
        all the kea config files
        """
        okay = _config_servers(self)
        for (_subnet, net) in self.nets.items():
            okay &= _config_network(net, self.dns)
            net.merge_option_data(self.global_options)
        return okay

    def save_configs(self):
        """
        Write out the kea config files for dhcp4
        """
        write_configs(self)
