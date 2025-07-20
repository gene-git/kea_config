# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Support for dhcp4 part of kea config generator
 Write out the kea configs
   Output divided into sections
"""
# pylint: disable=too-many-statements, too-many-locals
# pylint: disable=duplicate-code

from .tools import list_to_strings
from .kea_data import KeaConfigData
from .kea_types import FobConf


def dhcp4_write_global_options(conf: KeaConfigData,
                               fobs: FobConf):
    """
    write the global options part
    """
    opts_global = conf.global_options
    if not opts_global:
        return

    domain_name_servers = opts_global['domain-name-servers']
    domain_name = opts_global['domain-name']
    domain_search = opts_global['domain-search']
    ntp_servers = opts_global['ntp-servers']

    #
    # map lists to comma separated strings
    #
    dns_servers = list_to_strings(domain_name_servers)
    dns_search = list_to_strings(domain_search)
    ntp_servers = list_to_strings(ntp_servers)

    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            fob.write('\n')
            fob.write('\t"option-data" : [\n')
            if domain_name_servers:
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

            if domain_search:
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


def dhcp4_write_top_section(conf, fobs):
    """
    Write out the top of configs
    """
    title = conf.title
    if not title:
        title = ''

    now = conf.now

    lifetime = conf.global_options.get('valid-lifetime')
    min_lifetime = conf.global_options.get('min-valid-lifetime')
    max_lifetime = conf.global_options.get('max-valid-lifetime')
    socket_dir = conf.socket_dir

    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            server = getattr(conf, stype)
            iface = server.interface
            hostname = server.hostname

            fob.write('//\n')
            fob.write(f'// Kea Config : {hostname}\n')
            fob.write(f'//    Title : {title}\n')
            fob.write(f'// Server type : {stype}\n')
            fob.write(f'// Generated at : {now}\n')
            fob.write('//\n')

            fob.write('\n')
            fob.write('{\n')
            fob.write('"Dhcp4": {\n')
            fob.write('\t"authoritative": true,\n')
            fob.write('\t"interfaces-config":\n')
            fob.write('\t{\n')
            fob.write(f'\t\t"interfaces": ["{iface}"],\n')
            fob.write('\t\t"dhcp-socket-type": "raw" \n')
            fob.write('\t},\n')

            fob.write('\n')
            fob.write('\t"control-socket": {\n')
            fob.write('\t\t"socket-type": "unix",\n')
            fob.write(f'\t\t"socket-name": "{socket_dir}/kea4-ctrl-socket"\n')
            fob.write('\t},\n')

            fob.write('\t"lease-database": {\n')
            fob.write('\t\t"type": "memfile",\n')
            fob.write('\t\t"persist": true,\n')
            fob.write('\t\t"name": "/var/lib/kea/kea-leases4.csv",\n')
            fob.write('\t\t"lfc-interval": 3600\n')
            fob.write('\t},\n')

            fob.write('\t"expired-leases-processing": {\n')
            fob.write('\t\t"reclaim-timer-wait-time": 10,\n')
            fob.write('\t\t"flush-reclaimed-timer-wait-time": 25,\n')
            fob.write('\t\t"hold-reclaimed-time": 3600,\n')
            fob.write('\t\t"max-reclaim-leases": 100,\n')
            fob.write('\t\t"max-reclaim-time": 250,\n')
            fob.write('\t\t"unwarned-reclaim-cycles": 5\n')
            fob.write('\t},\n')

            fob.write('\t"calculate-tee-times": true,\n')
            fob.write('\t"offer-lifetime": 60,\n')

            if min_lifetime:
                fob.write(f'\t"min-valid-lifetime": {min_lifetime},\n')
            if lifetime:
                fob.write(f'\t"valid-lifetime": {lifetime},\n')
            if lifetime:
                fob.write(f'\t"max-valid-lifetime": {max_lifetime},\n')


def dhcp4_write_peers(conf, fob):
    """
    Write out the server section (the peers)
    """

    if not fob:
        return

    num_peers = len(conf.server_types)

    fob.write('\n\t\t\t\t"peers": [')
    count = 1
    for stype in conf.server_types:
        server = getattr(conf, stype)

        if stype == 'backup':
            failover = 'false'
        else:
            failover = 'true'

        name = f'kea-{stype}'
        ip = server.ip
        port = server.port
        url = f'http://{ip}:{port}'
        role = stype

        auth_user = server.auth_user
        auth_pass = server.auth_password

        fob.write('\n\t\t\t\t{')
        fob.write(f'\n\t\t\t\t\t"name": "{name}",')
        fob.write(f'\n\t\t\t\t\t"url": "{url}",')
        fob.write(f'\n\t\t\t\t\t"basic-auth-user": "{auth_user}",')
        fob.write(f'\n\t\t\t\t\t"basic-auth-password": "{auth_pass}",')
        fob.write(f'\n\t\t\t\t\t"role": "{role}",')
        fob.write(f'\n\t\t\t\t\t"auto-failover": {failover}\n')
        fob.write('\n\t\t\t\t}')

        if count < num_peers:
            fob.write(',')
        count = count + 1

    fob.write('\n\t\t\t\t]')


def dhcp4_write_hooks_libs(conf, fobs):
    """
    Write out the hooks library section
    """

    lib: str
    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            name = f'kea-{stype}'
            # role = stype

            fob.write('\n')
            fob.write('\t//\n')
            fob.write('\t// Hooks\n')
            fob.write('\t//')

            lib = '/usr/lib/kea/hooks/libdhcp_lease_cmds.so'
            fob.write('\n\t"hooks-libraries": [')
            fob.write('\n\t\t{')
            fob.write(f'\n\t\t\t"library": "{lib}",')
            fob.write('\n\t\t\t"parameters": { }')
            fob.write('\n\t\t}')

            if conf.has_standby:
                lib = '/usr/lib/kea/hooks/libdhcp_ha.so'
                fob.write(',')
                fob.write('\n\t\t{')
                fob.write(f'\n\t\t\t"library": "{lib}",')
                fob.write('\n\t\t\t"parameters": {')
                fob.write('\n\t\t\t"high-availability": [')
                fob.write('\n\t\t\t{')
                fob.write(f'\n\t\t\t\t"this-server-name": "{name}",')
                fob.write('\n\t\t\t\t"mode": "hot-standby",')
                fob.write('\n\t\t\t\t"heartbeat-delay": 10000,')
                fob.write('\n\t\t\t\t"max-response-delay": 10000,')
                fob.write('\n\t\t\t\t"max-ack-delay": 5000,')
                fob.write('\n\t\t\t\t"max-unacked-clients": 5,')
                fob.write('\n\t\t\t\t"sync-timeout": 60000,')

                dhcp4_write_peers(conf, fob)

                fob.write('\n\t\t\t}')
                fob.write('\n\t\t\t]')       # high avail
                fob.write('\n\t\t}')

                fob.write('\n\t}')
            fob.write('\n\t],')


def dhcp4_write_subnets(conf, fobs):
    """
    Write out the subnet (we handle 1 subnet currently.
    """
    # pylint: disable=
    #
    # handle multiple pool ranges in a subnet
    # pools: [{"pool": "range 1"}, {"pool": "range 2"}]
    #
    net = conf.net

    pools = net['pools']
    subnet = net['subnet']

    lifetime = net.get('valid-lifetime')
    min_lifetime = net.get('min-valid-lifetime')
    max_lifetime = net.get('max-valid-lifetime')

    option_data = net.get('option-data')
    if option_data:
        bcast = option_data.get('broadcast-address')
        ntp = option_data.get('ntp-servers')
        ntp_servers = list_to_strings(ntp)
        routers = option_data.get('routers')
        routers = list_to_strings(routers)

    #
    # format pool ranges into kea format
    #
    pool_info = None
    for item in pools:
        if pool_info:
            pool_info = pool_info + f', {{"pool": "{item}"}}'
        else:
            pool_info = f'{{"pool": "{item}"}}'

    subnet_id = '1'
    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            server = getattr(conf, stype)
            iface = server.interface

            fob.write('\n')
            fob.write('\t//\n')
            fob.write('\t// IPv4 subnet\n')
            fob.write('\t//\n')

            fob.write('\t"subnet4": [\n')
            fob.write('\t{\n')
            fob.write(f'\t\t"id": {subnet_id},\n')
            fob.write(f'\t\t"subnet": "{subnet}",\n')
            fob.write(f'\t\t"pools": [{pool_info}],\n')

            if min_lifetime:
                fob.write(f'\t\t"min-valid-lifetime": {min_lifetime},\n')
            if lifetime:
                fob.write(f'\t\t"valid-lifetime": {lifetime},\n')
            if max_lifetime:
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


def dhcp4_write_reserved(conf, fobs):
    """
    Write out the reserved hosts - mac and ip
    """

    reserved = conf.net.get('reserved')
    if not reserved:
        return

    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            fob.write('\n')
            fob.write('\t\t//\n')
            fob.write('\t\t// IP Reservations\n')
            fob.write('\t\t//\n')

            fob.write('\n')
            # 2024-05-22 reservation-mode has been deprecated
            # fob.write('\t\t"reservation-mode": "out-of-pool",\n')
            fob.write('\t\t"reservations": [\n')

            first = True
            for host in reserved:
                ip = reserved[host]['ip']
                mac = reserved[host]['hw-address']
                fqdn = reserved[host].get('fqdn')
                if not first:
                    fob.write(',\n')
                else:
                    first = False
                fob.write('\t\t{\n')
                if fqdn:
                    fob.write(f'\t\t\t"hostname": "{fqdn}",\n')
                else:
                    fob.write(f'\t\t\t"hostname": "{host}",\n')
                fob.write(f'\t\t\t"hw-address": "{mac}",\n')
                fob.write(f'\t\t\t"ip-address": "{ip}"\n')
                fob.write('\t\t}')
            fob.write('\n')
            fob.write('\t\t]\n')
            fob.write('\t}\n')
            fob.write('\t],\n')


def dhcp4_write_loggers(conf, fobs):
    """
    Write out the logging section
    """
    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            fob.write('\n')
            fob.write('\t"loggers": [\n')
            fob.write('\t{\n')
            fob.write('\t\t"name": "kea-dhcp4",\n')
            fob.write('\t\t"output_options": [\n')
            fob.write('\t\t{\n')
            fob.write('\t\t\t"output": "/var/log/kea/kea-dhcp4.log",\n')
            fob.write('\t\t\t"flush": false,\n')
            fob.write('\t\t\t"maxsize": 1048576,\n')
            fob.write('\t\t\t"maxver": 8\n')
            fob.write('\t\t}\n')
            fob.write('\t\t],\n')
            fob.write('\t\t"severity": "WARN",\n')
            fob.write('\t\t"debuglevel": 0\n')

            fob.write('\t}\n')
            fob.write(']\n')
            fob.write('}\n')
            fob.write('}\n')
