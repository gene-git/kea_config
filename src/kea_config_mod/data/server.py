# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Each Kea Server
"""
# pylint: disable=too-many-instance-attributes
from typing import (Any, IO)


class KeaServer:
    """
    There are 3 types primary, secondary and backup
    """
    def __init__(self, stype: str):
        self.stype: str = stype
        self.active: bool = True
        self.hostname: str = ''
        self.port: str = '8761'         # todo: port change to int
        self.ip: str = ''
        # self.interface: str = ""
        # list of (interface, subdomain)
        self.interfaces: list[tuple[str, str]] = []
        self.auth_user: str = ''
        self.auth_password: str = ''

        self.fob_dhcp4: IO | None = None
        self.fob_agent: IO | None = None

    def get_iface(self, subnet: str) -> str:
        """
        If server has interface on this subnet return the interface name
        Returns empty string if not
        """
        for (iface, this_subnet) in self.interfaces:
            if this_subnet == subnet:
                return iface
        return ''

    def close_files(self):
        """ close any open file objects """
        if self.fob_dhcp4:
            self.fob_dhcp4.close()

        if self.fob_agent:
            self.fob_agent.close()

    def from_dict(self, a_dict: dict[str, Any]):
        """
        Load self from dictionary
        """
        if not a_dict:
            return

        for (k, v) in a_dict.items():
            kk = k.replace('-', '_')
            if kk == 'interfaces':
                if not v:
                    print(f'Error server interfaces: {v}')
                    continue

                for iface_dom in v:
                    if len(iface_dom) != 2:
                        print('Error interaces: each item must be (iface, subnet)')
                        print(f'   invalid: {iface_dom}')
                    else:
                        self.interfaces.append((iface_dom[0], iface_dom[1]))

            else:
                setattr(self, kk, v)
