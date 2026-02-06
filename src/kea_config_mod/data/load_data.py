# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Load Config File
- use yaml if found otherwise toml
- craete sample yaml
"""
from typing import Any
import copy

from kea_config_mod.utils import read_toml_file
from kea_config_mod.utils import read_yaml_file
from kea_config_mod.utils import write_yaml_file


def load_data(conf_file: str) -> dict[str, Any]:
    """
    Load data - yaml if found else toml
    - yaml: kea-dhcp4-setup.yaml
    - toml: kea-dhcp4-setup.conf
    """
    conf_new: dict[str, Any] = {}
    #
    # Try 1 - check if valid yaml
    #
    conf_new = read_yaml_file(conf_file)

    #
    # Try 2a - check if valid toml
    #
    if not conf_new:
        print(f'Warning config not YAML (or not found): {conf_file}')
        conf = read_toml_file(conf_file)

        #
        # Try 2b - check chg xxx.yaml -> xxx.conf
        #
        if not conf and conf_file.endswith('.yaml'):
            toml_file = conf_file.replace('.yaml', '.conf')
            conf = read_toml_file(toml_file)

        if not conf:
            print(f'Error with config file: {conf_file}')
            print(f'  or {toml_file}')
            return conf_new

        #
        # Got toml, update data and save yaml version
        #
        if conf_file.endswith('.yaml'):
            yaml_file = conf_file

        elif conf_file.endswith('.conf'):
            yaml_file = conf_file.replace('.conf', '.yaml')

        elif conf_file.endswith('.toml'):
            yaml_file = conf_file.replace('.toml', '.yaml')

        else:
            yaml_file = conf_file + '.yaml'

        print('  Updating and converting to YAML')
        conf_new = update_conf(conf)

        if conf_new:
            # Save the yaml config file
            # yaml_file_sample = f'{yaml_file}.sample'
            print(f'  Saving YAML config to {yaml_file}')

            if write_yaml_file(conf_new, yaml_file):
                print('  Please check and/or add comments.')
            else:
                print(f'  Error saving {yaml_file}')

    return conf_new


def update_conf(conf: dict[str, Any]) -> dict[str, Any]:
    """
    Update old format
    """
    conf_new: dict[str, Any] = {}
    if not conf:
        return conf_new

    conf = _dash_to_underscore(conf)
    conf_new = copy.deepcopy(conf)

    conf_new['servers'] = {}
    servers = conf_new['servers']

    #
    # net -> nets {network-name: netdata}
    #
    net = conf.get('net')
    del conf_new['net']
    nets: dict[str, Any] = {}
    conf_new['nets'] = nets
    del conf_new['server']

    #
    # subdomain:
    # - global
    # - net['dns_net'] overrides
    #
    subdomain: str = ''
    glob_opts = conf.get('global_options')
    if glob_opts and glob_opts.get('domain_name'):
        subdomain = glob_opts.get('domain_name')

    # dns_net changed to subdomain
    if net:
        if net.get('dns_net'):
            net['subdomain'] = net.get('dns_net')
            del net['dns_net']
        else:
            # use global
            net['subdomain'] = subdomain

        subnet = net.get('subnet')
        if subnet:
            conf_new['nets'] = {subnet:  net}
        else:
            print('Error: Each net requires subnet be defined')
            conf_new = {}
            return conf_new
    #
    # interface -> interfaces
    # interfaces is list of [iface, network-name]
    # We use the 1 subnet as key : nets[subnet] = ...
    # Old config have 1 net (and one subdomain)
    #
    server = conf.get('server')
    server_types_active: list[str] = []
    del conf_new['server_types']

    if server:
        server_types_active = conf.get('server_types', [])
        stypes = list(server.keys())
        for stype in stypes:
            this_server = server.get(stype)
            this_server['stype'] = stype
            this_server['subdomain'] = subdomain
            interface = this_server.get('interface')
            this_server['active'] = True
            if stype not in server_types_active:
                this_server['active'] = False
            if interface:
                this_server['interfaces'] = [[interface, subnet]]
                del this_server['interface']
            servers[stype] = this_server

    return conf_new


def _dash_to_underscore(dic: dict[str, Any],
                        skip_key: bool = False
                        ) -> dict[str, Any]:
    """
    Change any key names with "-" to use "_"
    """
    clean: dict[str, Any] = {}
    for (k, v) in dic.items():
        kk = k
        if not skip_key:
            kk = k.replace('-', '_')
        if isinstance(v, dict):
            if k == 'reserved':
                vv = _dash_to_underscore(v, skip_key=True)
            else:
                vv = _dash_to_underscore(v)
        else:
            vv = v
        clean[kk] = vv
    return clean
