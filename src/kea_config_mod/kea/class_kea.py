# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 kea config tool
 Tools to generate kea-dhcp4 server configs
 Driven by toml config file
 gc    2022-03-03
"""
# pylint: disable=

from .write_configs import write_configs
from .kea_data import KeaConfigData


def _config_servers(kea_conf):
    """
    Split out the server info from config
    """
    okay = True
    for stype in kea_conf.server_types:
        this_server = getattr(kea_conf, stype)
        if not this_server:
            continue

        ipin = vars(this_server).get('ip-address')
        hostname = this_server.hostname
        ip = kea_conf.dns.query(hostname)
        if not ip:
            print(f'Failed to find IP for host : {hostname}')
            okay = False

        if ipin and ipin != ip:
            print(f' {stype} {this_server} : {hostname} ip mismatch with dns')
            txt = f'{ip} + ignoring and using config ip: {ipin}'
            print(f' ip from dns is : {txt}')
            ip = ipin
        this_server.ip = ip

    return okay


def _config_networks(kea_conf):
    """
    Network info from config
    """
    okay = True
    if not kea_conf.net:
        print('No [net] section')
        return not okay

    reserved = kea_conf.net.get('reserved')
    if reserved:
        dns_net = kea_conf.net.get('dns_net')
        if not dns_net:
            txt = 'host reservations require "dns_net" in [net] section'
            print(f'Error: {txt}')
            return not okay

        for host in reserved:
            fqdn = f'{host}.{dns_net}'
            ip = kea_conf.dns.query(fqdn)
            if not ip:
                print(f'Failed to find IP for host : {fqdn}')
                okay = False

            ipin = reserved[host].get('ip-address')
            if ipin and ipin != ip:
                txt = f'({ipin}) not same as dns ({ip})'
                print(f'Warning {host} ip address: {txt}')
                print(f'Using config value : {ipin}')
                ip = ipin
            # reserved[host]['ip-address'] = ip
            reserved[host]['ip'] = ip
            reserved[host]['fqdn'] = f'{fqdn}.'

    return okay


class KeaConfig(KeaConfigData):
    """
    Tools to generate kea-dhcp4 server configs.
    Generates primary, standby and backup configs.
    """
    def dns_query(self, query: str, rr_type: str = 'A', one_rr: bool = True):
        """
        dns query - used to map hostnames to ips
        """
        self.dns.query(query, rr_type=rr_type, one_rr=one_rr)

    def config_setup(self):
        """
        Prep the config information so have info needed to write
        all the kea config files
        """
        okay = _config_servers(self)
        okay &= _config_networks(self)
        return okay

    def save_configs(self):
        """
        Write out the kea config files for dhcp4
        """
        write_configs(self)
