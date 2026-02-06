# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
kea config base class
"""
# pylint: disable=too-many-instance-attributes, too-few-public-methods

from typing import (Any)
import os
import datetime

from kea_config_mod.dns import Dns
from kea_config_mod.utils import make_dir_path

from .load_data import load_data
from .server import KeaServer
from .network import KeaNet
from .network import OptionData
from .options import options


def _attribs_from_conf(conf: dict[str, Any], data: KeaData):
    """
    Extract class attribs from dictionary.
    """
    if not conf:
        return

    for (k, v) in conf.items():
        kk = k.replace('-', '_')
        if kk == 'nets':
            for (subnet, a_dict) in v.items():
                kea_net = KeaNet(subnet)
                kea_net.from_dict(a_dict)
                data.nets[subnet] = kea_net

        elif kk == 'servers':
            for (stype, a_dict) in v.items():
                kea_serv = KeaServer(stype)
                kea_serv.from_dict(a_dict)
                data.servers[stype] = kea_serv

        elif kk == 'global_options':
            data.global_options.from_dict(v)
        else:
            setattr(data, kk, v)


class KeaData:
    """
    Tools to generate kea-dhcp4 server configs
    Generates primary and standby and backup configs
    """
    def __init__(self):
        self.dns: Dns = Dns()
        self.now: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config_file: str = 'kea-dhcp4-setup.yaml'
        self.socket_dir: str = '/var/run/kea'
        # self.net: dict[str, Any] = {}

        self.global_options: OptionData = OptionData()

        self.servers: dict[str, KeaServer] = {}     # key is stype (primary, secondary ...)
        self.nets: dict[str, KeaNet] = {}           # key is subnet

        self.has_standby: bool = False
        self.has_backup: bool = False

        self.conf_dir: str = ''
        self.conf_prefix: str = ''
        self.conf_base: str = ''
        self.agent_prefix: str = ''
        self.agent_base: str = ''
        self.conf_dir_bakup: str = ''

        # Command line options
        cl_opts: dict[str, Any] = options(self.config_file)
        confile = cl_opts['config']

        config = load_data(confile)
        if not config:
            print(f'Missing config file : {confile}')
            self.okay = False
            return

        _attribs_from_conf(config, self)
        if not self.servers:
            print('At least primary server must be defined')
            self.okay = False
            return

        if not _check_server_types(self):
            return

        #
        # valid_lifetimes
        #
        _valid_lifetimes(self)

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
# Private
#
def _check_server_types(data: KeaData) -> bool:
    """
    check config has valid server_types list
    Backward compat: Handle older configs with no server_types,
    but each section marked with active
    """
    if not data.servers:
        print('Missing servers (must have at least primary)')
        return False

    server_types = list(data.servers.keys())
    if 'primary' not in server_types:
        print('Missing primary server')
        return False

    if not data.servers['primary'].active:
        print('primary server is marked inactive')
        return False

    if 'standby' in data.servers:
        data.has_standby = True

    if 'backup' in data.servers:
        data.has_backup = True

    return True


def _outputs_init(data: KeaData) -> bool:
    """
    Make config file name base
    """
    conf_dir = data.conf_dir
    if not conf_dir:
        print('Missing conf_dir in config - required')
        return False

    if conf_dir:
        conf_dir = os.path.realpath(conf_dir)

    if not make_dir_path(conf_dir):
        print('Error creating conf_dir {conf_dir}')

    conf_dir_bakup = os.path.join(conf_dir, 'Prev')
    if not make_dir_path(conf_dir_bakup):
        print('Error creating conf_dir {conf_dir_bakup}')
    data.conf_dir_bakup = conf_dir_bakup

    data.conf_prefix = 'kea-dhcp4'
    data.conf_base = os.path.join(conf_dir, data.conf_prefix)

    data.agent_prefix = 'kea-ctrl-agent'
    data.agent_base = os.path.join(conf_dir, data.agent_prefix)

    return True


def _lifetimes(life_in: int, min_life_in: int, max_life_in: int) -> tuple[int, int, int]:
    """
    Check and infer lifetime
    returns :
        (lifetime, min_lifetime, max_lifetime) as integers if any are set
        (-1, -1, -1) if none are set
    """
    life: int = -1
    min_life: int = -1
    max_life: int = -1

    if life_in < 0 and min_life_in < 0 and max_life_in < 0:
        return (life, min_life, max_life)

    life = max(life_in, -1)
    min_life = max(min_life_in, -1)
    max_life = max(max_life_in, -1)

    if life < 0:
        if max_life > 0:
            life = int(max_life / 2)
        else:
            life = int(min_life * 2)

    if min_life < 0:
        min_life = int(life / 2)

    if max_life < 0:
        max_life = int(life * 2)

    return (life, min_life, max_life)


def _valid_lifetimes(data: KeaData):
    """
    Check and infer lifetime
    """
    #
    # Global
    #
    life: int = -1
    min_life: int = -1
    max_life: int = -1

    glob_opts = data.global_options

    #
    # Get sensible global values
    # - use any provided
    #
    life = glob_opts.valid_lifetime
    min_life = glob_opts.min_valid_lifetime
    max_life = glob_opts.max_valid_lifetime

    (life, min_life, max_life) = _lifetimes(life, min_life, max_life)
    if life < 0:
        (life, min_life, max_life) = _lifetimes(14400, min_life, max_life)

    glob_opts.valid_lifetime = life
    glob_opts.min_valid_lifetime = min_life
    glob_opts.max_valid_lifetime = max_life

    #
    # net
    #
    for (_subnet, net) in data.nets.items():

        life = net.valid_lifetime
        min_life = net.min_valid_lifetime
        max_life = net.max_valid_lifetime

        (life, min_life, max_life) = _lifetimes(life, min_life, max_life)

        if life < 0:
            net.valid_lifetime = glob_opts.valid_lifetime
            net.min_valid_lifetime = glob_opts.min_valid_lifetime
            net.max_valid_lifetime = glob_opts.min_valid_lifetime
