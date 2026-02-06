# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
kea : 1 network
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-few-public-methods
# pylint: disable=too-few-public-methods
from typing import Any


class OptionData:
    """ dhcp options """
    def __init__(self):
        self.broadcast_address: str = ''
        self.routers: list[str] = []      # 'ip' or 'ip1,ip2,..'
        self.ntp_servers: list[str] = []

        self.domain_name: str = ''
        self.domain_search: list[str] = []
        self.domain_name_servers: list[str] = []

        self.valid_lifetime: int = -1
        self.min_valid_lifetime: int = -1
        self.max_valid_lifetime: int = -1

    def from_dict(self, a_dict: dict[str, Any]):
        """ data from dict """
        if not a_dict:
            return

        ints: list[str] = ['valid_lifetime', 'min_valid_lifetime', 'max_valid_lifetime']

        for (k, v) in a_dict.items():
            kk = k.replace('-', '_')
            if kk == 'routers' and isinstance(v, str):
                setattr(self, kk, [v])
            elif kk in ints:
                setattr(self, kk, int(v))
            else:
                setattr(self, kk, v)

    def merge_option_data(self, opts: OptionData):
        """
        Inherit in relevant global options 'opts'
        This is only used by network to inherit from global.
        Generally safer / better for each network to fully specify the option date
        User needs to exercise caution here as some global values may not be applicable
        **Never merged:
            - broadcast_address
            - domain_name
            - lifetimes - handled in KeaData() class itself
        """
        if not self.routers and opts.routers:
            self.routers = opts.routers

        if not self.ntp_servers and opts.ntp_servers:
            self.routers = opts.routers

        if self.valid_lifetime < 0:
            self.valid_lifetime = opts.valid_lifetime

        if self.min_valid_lifetime < 0:
            self.min_valid_lifetime = opts.min_valid_lifetime

        if self.max_valid_lifetime < 0:
            self.max_valid_lifetime = opts.max_valid_lifetime


class Reserved:
    """ reserved ip/name """
    def __init__(self, host: str, domain: str):
        self.host: str = host
        self.fqdn: str = ''
        self.hw_address: str = ''
        self.ip_address: str = ''
        self.ip: str = ''

        self.fqdn = f'{host}.{domain}'

    def from_dict(self, a_dict: dict[str, Any]):
        """
        get ip address from hostname
        Need resolver for PTR lookup.
        """
        if not a_dict:
            return

        for (k, v) in a_dict.items():
            kk = k.replace('-', '_')
            if kk not in ('host', 'fqdn'):
                setattr(self, kk, v)


class KeaNet:
    """
    All data needed for dhcp for one network
    - ip ranges, dns, reserved ips etc
    """
    def __init__(self, subnet: str):
        """
        Network is uniqely identified by it's subnet.
        """
        # self.name: str = name
        self.subnet: str = subnet
        self.subdomain: str = ''
        self.subnet_id: int = -1
        # self.id: str = ''
        self.pools: list[str] = []      # each pool is range "ip0 - ip1"

        self.valid_lifetime: int = -1
        self.min_valid_lifetime: int = -1
        self.max_valid_lifetime: int = -1

        self.option_data: OptionData = OptionData()

        self.reserved: dict[str, Reserved] = {}     # key is hostname

    def merge_option_data(self, opts: OptionData):
        """
        Inherit in relevant global options 'opts'
        Generally better for each network to fully specify
        Caution needed here as some global values may not be applicable
        """
        self.option_data.merge_option_data(opts)

    def from_dict(self, a_dict: dict[str, Any]):
        """ data from dict """
        if not a_dict:
            return

        ints: list[str] = ['valid_lifetime', 'min_valid_lifetime', 'max_valid_lifetime']

        domain: str = ''
        domain = a_dict.get('subdomain', '')
        subnet: str = ''
        subnet = a_dict.get('subnet', '')

        if not domain:
            print(f'Warning: net has no subdomain ({subnet})')

        for (k, v) in a_dict.items():
            kk = k.replace('-', '_')
            if kk == 'option_data':
                self.option_data.from_dict(v)

            elif kk == 'reserved':
                for (name, subv) in v.items():
                    reserved = Reserved(name, domain)
                    reserved.from_dict(subv)
                    self.reserved[name] = reserved

            elif kk in (ints):
                setattr(self, kk, int(v))
            else:
                setattr(self, kk, v)
