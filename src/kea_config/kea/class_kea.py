# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 kea config tool
 Tools to generate kea-dhcp4 server configs
 Driven by toml config file
 gc    2022-03-03
"""
import os
import datetime
import argparse

from .class_dns import GcDns
from .write_configs import write_configs
from .toml import read_toml_file

# pylint: disable=R0903,C0103
#-----------------------------------------------------
# Dynamic classes
#
class KeaServer:
    """ Base Class for all server types """
    def __init__(self, kea_conf, name, server):
        self.name = name
        self.kea_conf = kea_conf
        for (key, val) in server.items():
            setattr(self, key, val)

    def __getattr__(self, name):
        return None

def _check_server_types(kea_conf):
    """
    check config has valid server_types list
        Backward compat: Handle older configs with no server_types,
        but each section marked with active
    """
    okay = True
    if not kea_conf.server_types:
        print('Warning - old style config, please add "server_types" list')
        kea_conf.server_types = ['primary', 'standby',  'backup']
        server_types = []
        for stype in kea_conf.server_types:
            this_server = getattr(kea_conf, stype)
            if this_server and this_server['active'] :
                server_types.append(stype)
        kea_conf.server_types = server_types

    if 'primary' not in kea_conf.server_types:
        print ('Missing primary server')
        return not okay

    if len(kea_conf.server_types) > 1:
        kea_conf.has_standby = True
    else:
        kea_conf.has_standby = False

    return okay

def _reserved_hosts(kea_conf):
    """
    Get list of reserved host names
    """
    reserved = []
    net = kea_conf.net
    if net.get('reserved'):
        for res_host in net.reserved.items() :
            reserved.append(res_host)
    return reserved

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
            print (f'Failed to find IP for host : {hostname}')
            okay = False

        if ipin and ipin != ip:
            print (f' {stype} {this_server} : {hostname} ip mismatch with dns')
            print (f' ip from dns is : {ip} + ignoring and using config ip: {ipin}')
            ip = ipin
        this_server.ip = ip

    return okay

def _config_networks(kea_conf):
    """
    Network info from config
    """
    okay = True
    if not kea_conf.net:
        print ('No [net] section')
        return not okay

    reserved = kea_conf.net.get('reserved')
    if reserved:
        dns_net = kea_conf.net.get('dns_net')
        if not dns_net:
            print(f'Error: host reservations require "dns_net" in [net] section')
            return not okay

        for host in reserved:
            fqdn = f'{host}.{dns_net}'
            ip = kea_conf.dns.query(fqdn)
            if not ip:
                print (f'Failed to find IP for host : {fqdn}')
                okay = False

            ipin = reserved[host].get('ip-address')
            if ipin and ipin != ip:
                print (f'Warning {host} ip address ({ipin}) not same as dns ({ip})')
                print (f'Using config value : {ipin}')
                ip = ipin
            #reserved[host]['ip-address'] = ip
            reserved[host]['ip'] = ip
            reserved[host]['fqdn'] = f'{fqdn}.'

    return okay

def _outputs_init(kea_conf):
    """
    Make config file name base
    """
    okay = True
    conf_dir = kea_conf.conf_dir
    if not conf_dir:
        print ('Missing conf_dir in config - required')
        return not okay

    if conf_dir and not (conf_dir.startswith('/') or conf_dir.startswith('./')) :
        conf_dir = os.path.join('./', conf_dir)

    os.makedirs(conf_dir, exist_ok=True)

    kea_conf.conf_prefix = 'kea-dhcp4'
    kea_conf.conf_base = os.path.join(conf_dir, kea_conf.conf_prefix)
    kea_conf.agent_prefix = 'kea-ctrl-agent'
    kea_conf.agent_base = os.path.join(conf_dir, kea_conf.agent_prefix)

    return okay

class KeaConfig:
    """
    Tools to generate kea-dhcp4 server configs
    Generates primary and standby and backup configs
    """
    def __init__(self):
        self.dns = GcDns()
        self.now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config_file = 'kea-dhcp4-setup.conf'
        self.socket_dir = '/var/run/kea'

        arp = argparse.ArgumentParser(description='kea_config')

        arp.add_argument('-c',  '--config',
                default = self.config_file,
                help = f'Config file ({self.config_file})'
                )

        parsed = arp.parse_args()
        # save cmd line opts - more general than we presently need
        cl_opts = {}
        if parsed:
            for (ckey, cval) in  vars(parsed).items() :
                cl_opts[ckey] = cval

        # load toml config
        confile = cl_opts['config']
        config = read_toml_file(confile)
        if not config:
            print(f'Missing config file : {confile}')
            self.okay = False
            return

        #
        # Create our attribute variables
        for ckey, cval in config.items():
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

        #   class for each server type  (KeaPrimary, KeaStandby, KeaBackup)
        #   e.g. self.primary is instance of KeaPrimary class derived from KeaServers class
        #    and self.standy and self.backup
        #
        server = self.server
        for name in self.server_types:
            this_name = 'Kea' + name.capitalize()
            xtra_attributes = {}
            globals()[this_name] = type(this_name, (KeaServer,), xtra_attributes)

            this_class = globals()[this_name]
            this_attributes = server[name]                   # config dictionary
            this_instance = this_class(self, name, this_attributes) # create instance
            setattr(self, name, this_instance)                      # save to self.name

        # output file set up
        if not _outputs_init(self):
            self.okay = False
            return

    def __getattr__(self, name):
        """ non-set items simply return None so easy to check existence"""
        return None

    def dns_query(self, query, qtype='A'):
        """
        dns query - used to map hostnames to ips
        """
        self.dns.query(query, qtype=qtype)

    def config_setup(self):
        """
        Prep the config information so have info needed to wtite the kea config files
        """
        okay = _config_servers(self)
        okay &= _config_networks(self)
        return okay

    def save_configs(self):
        """
        Write out the kea config files for dhcp4
        """
        write_configs(self)

def _lifetimes(lifetime, min_lifetime, max_lifetime):
    """
    Check and infer lifetime
    returns :
        (lifetime, min_lifetime, max_lifetime) as integers if any are set
        (None, None, None) if none are set
    """
    if not (lifetime or min_lifetime or max_lifetime):
        return (None, None, None)

    if not lifetime:
        if max_lifetime:
            lifetime = int(int(max_lifetime) / 2)
        else:
            lifetime = int(int(min_lifetime) * 2)

    if not min_lifetime:
        min_lifetime = int(int(lifetime) / 2)

    if not max_lifetime:
        max_lifetime = int(int(lifetime) * 2)

    return (lifetime, min_lifetime, max_lifetime)

def _valid_lifetimes(conf):
    """
    Check and infer lifetime
    """
    #
    # Global
    #
    has_global = False
    has_net = False
    lifetime = conf.global_options.get('valid-lifetime')
    min_lifetime = conf.global_options.get('min-valid-lifetime')
    max_lifetime = conf.global_options.get('max-valid-lifetime')

    (lifetime, min_lifetime, max_lifetime) = _lifetimes(lifetime, min_lifetime, max_lifetime)
    if lifetime:
        has_global = True
        conf.global_options['valid-lifetime'] = lifetime
        conf.global_options['min-valid-lifetime'] = min_lifetime
        conf.global_options['max-valid-lifetime'] = max_lifetime

    #
    # net
    #
    net = conf.net
    lifetime = net.get('valid-lifetime')
    min_lifetime = net.get('min-valid-lifetime')
    max_lifetime = net.get('max-valid-lifetime')
    (lifetime, min_lifetime, max_lifetime) = _lifetimes(lifetime, min_lifetime, max_lifetime)
    if lifetime:
        has_net = True
        net['valid-lifetime'] = lifetime
        net['min-valid-lifetime'] = min_lifetime
        net['max-valid-lifetime'] = max_lifetime

    #
    # Set default if not specified
    #
    if not (has_global or has_net):
        conf.global_options['valid-lifetime'] = 14400
        conf.global_options['min-valid-lifetime'] = 28800
        conf.global_options['max-valid-lifetime'] = 57600
