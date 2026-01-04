# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
kea config base class
"""
# pylint: disable=too-many-instance-attributes, too-few-public-methods

from typing import (Any)
import os
import datetime
import argparse

from .class_dns import Dns
from .toml import read_toml_file


# -----------------------------------------------------
# Public
#
class KeaConfigData:
    """
    Tools to generate kea-dhcp4 server configs
    Generates primary and standby and backup configs
    """
    def __init__(self):
        self.dns: Dns = Dns()
        self.now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config_file: str = 'kea-dhcp4-setup.conf'
        self.socket_dir: str = '/var/run/kea'
        self.net: dict[str, Any] = {}

        self.server_types: list[str] = []
        self.has_standby: bool = False

        self.conf_prefix: str = ''
        self.conf_base: str = ''
        self.agent_prefix: str = ''
        self.agent_base: str = ''

        #
        # Command line options
        #
        arp = argparse.ArgumentParser(description='kea_config')

        arp.add_argument(
                '-c', '--config',
                default=self.config_file,
                help=f'Config file ({self.config_file})'
                )

        parsed = arp.parse_args()
        # save cmd line opts - more general than we presently need
        cl_opts: dict[str, Any] = {}
        if parsed:
            for (ckey, cval) in vars(parsed).items():
                cl_opts[ckey] = cval

        # load config file
        confile = cl_opts['config']
        config = read_toml_file(confile)
        if not config:
            print(f'Missing config file : {confile}')
            self.okay = False
            return

        #
        # Create attributes from config
        for (ckey, cval) in config.items():
            setattr(self, ckey, cval)

        if not _check_server_types(self):
            return

        #
        # valid_lifetimes
        #
        _valid_lifetimes(self)

        #
        # Dynamic Classes
        #

        #
        # class for each server type (KeaPrimary, KeaStandby, KeaBackup)
        # e.g. self.primary is instance of KeaPrimary
        #      class derived from KeaServers class
        # Similarly for self.standy and self.backup
        #
        server = self.server
        for name in self.server_types:
            sname = 'Kea' + name.capitalize()
            xtra_attributes: dict[str, Any] = {}
            globals()[sname] = type(sname, (KeaServer,), xtra_attributes)

            this_class = globals()[sname]

            # config dictionary
            attributes = server[name]

            # create class instance
            this_instance = this_class(self, name, attributes)

            # save to self.name
            setattr(self, name, this_instance)

        # output file set up
        if not _outputs_init(self):
            self.okay = False
            return

    def __getattr__(self, name: str) -> Any:
        """ non-set items return None.
        Makes it simple to check aatribute existence
        """
        return None


# -----------------------------------------------------
# Dynamic classes
#
class KeaServer:
    """
    Base Class for all server types
    """
    def __init__(self,
                 kea_conf: KeaConfigData,
                 name: str,
                 attribs: dict[str, Any]):
        self.name = name
        self.kea_conf = kea_conf
        for (key, val) in attribs.items():
            setattr(self, key, val)

    def __getattr__(self, name: str) -> Any:
        return None


# -----------------------------------------------------
# Private
#
def _check_server_types(kea_conf: KeaConfigData) -> bool:
    """
    check config has valid server_types list
    Backward compat: Handle older configs with no server_types,
    but each section marked with active
    """
    if not kea_conf.server_types:
        print('Warning - old style config, please add "server_types" list')
        kea_conf.server_types = ['primary', 'standby',  'backup']
        server_types: list[str] = []

        for stype in kea_conf.server_types:
            this_server = getattr(kea_conf, stype)
            if this_server and this_server['active']:
                server_types.append(stype)

        kea_conf.server_types = server_types

    if 'primary' not in kea_conf.server_types:
        print('Missing primary server')
        return False

    if len(kea_conf.server_types) > 1:
        kea_conf.has_standby = True
    else:
        kea_conf.has_standby = False

    return True


# def _reserved_hosts(kea_conf: KeaConfigData) -> list[str]:
#    """
#    Get list of reserved host names
#    """
#    reserved: list[str] = []
#
#    net = kea_conf.net
#    if net and net.get('reserved'):
#        for res_host in net.reserved.items():
#            reserved.append(res_host)
#    return reserved


def _outputs_init(kea_conf: KeaConfigData) -> bool:
    """
    Make config file name base
    """
    conf_dir = kea_conf.conf_dir
    if not conf_dir:
        print('Missing conf_dir in config - required')
        return False

    # old:
    # if conf_dir and
    #    not (conf_dir.startswith('/') or conf_dir.startswith('./')) :
    #     conf_dir = os.path.join('./', conf_dir)
    if conf_dir:
        conf_dir = os.path.realpath(conf_dir)

    os.makedirs(conf_dir, exist_ok=True)

    kea_conf.conf_prefix = 'kea-dhcp4'
    kea_conf.conf_base = os.path.join(conf_dir, kea_conf.conf_prefix)
    kea_conf.agent_prefix = 'kea-ctrl-agent'
    kea_conf.agent_base = os.path.join(conf_dir, kea_conf.agent_prefix)

    return True


def _lifetimes(life_in: str | None,
               min_life_in: str | None,
               max_life_in: str | None) -> tuple[int, int, int]:
    """
    Check and infer lifetime
    returns :
        (lifetime, min_lifetime, max_lifetime) as integers if any are set
        (-1, -1, -1) if none are set
    """
    if not (life_in or min_life_in or max_life_in):
        return (-1, -1, -1)

    life: int = int(life_in) if life_in else 0
    min_life: int = int(min_life_in) if min_life_in else 0
    max_life: int = int(max_life_in) if max_life_in else 0

    if not life:
        if max_life:
            life = int(max_life / 2)
        else:
            life = int(min_life * 2)

    if not min_life:
        min_life = int(life / 2)

    if not max_life:
        max_life = int(life * 2)

    return (life, min_life, max_life)


def _valid_lifetimes(conf: KeaConfigData):
    """
    Check and infer lifetime
    """
    #
    # Global
    #
    has_global: bool = False
    has_net: bool = False

    life_str: str | None
    min_life_str: str | None
    max_life_str: str | None

    life: int
    min_life: int
    max_life: int

    conf_global = conf.global_options
    if conf_global:
        life_str = conf_global.get('valid-lifetime')
        min_life_str = conf_global.get('min-valid-lifetime')
        max_life_str = conf_global.get('max-valid-lifetime')

        (life, min_life, max_life) = (
                _lifetimes(life_str, min_life_str, max_life_str)
                )

        if life > 0:
            has_global = True
            conf.global_options['valid-lifetime'] = life
            conf.global_options['min-valid-lifetime'] = min_life
            conf.global_options['max-valid-lifetime'] = max_life

    #
    # net
    #
    net = conf.net

    life_str = net.get('valid-lifetime')
    min_life_str = net.get('min-valid-lifetime')
    max_life_str = net.get('max-valid-lifetime')

    (life, min_life, max_life) = (
            _lifetimes(life_str, min_life_str, max_life_str)
            )

    if life > 0:
        has_net = True
        net['valid-lifetime'] = life
        net['min-valid-lifetime'] = min_life
        net['max-valid-lifetime'] = max_life

    #
    # Set default if not specified
    #
    if not (has_global or has_net):
        conf.global_options['valid-lifetime'] = 14400
        conf.global_options['min-valid-lifetime'] = 28800
        conf.global_options['max-valid-lifetime'] = 57600
