"""
 Support for dhcp4 part of kea config generator
 Write out the kea configs
   Output divided into sections
"""
# pylint: disable=C0103
from .tools import list_to_strings

def dhcp4_write_global_options (kea_config, fps):
    """ write the global options part """
    options = kea_config.global_options
    if not options:
        return

    domain_name_servers = options['domain-name-servers']
    domain_name = options['domain-name']
    domain_search = options['domain-search']
    ntp_servers = options['ntp-servers']

    dns_servers = list_to_strings(domain_name_servers)
    dns_search = list_to_strings(domain_search)
    ntp_servers = list_to_strings(ntp_servers)

    #
    # map list to comma separated strings
    #
    for stype in kea_config.server_types:
        fobj = fps[stype]
        if fobj:
            fobj.write('\n')
            fobj.write('\t"option-data" : [\n')
            if domain_name_servers:
                fobj.write('\t{\n')
                fobj.write('\t\t"name" : "domain-name-servers",\n')
                fobj.write('\t\t"data" : ' + dns_servers + '\n')
                fobj.write('\t}')

            if domain_name:
                fobj.write(',\n')
                fobj.write('\t{\n')
                fobj.write('\t\t"name" : "domain-name",\n')
                fobj.write('\t\t"data" : "' + domain_name + '"\n')
                fobj.write('\t}')

            if domain_search:
                fobj.write(',\n')
                fobj.write('\t{\n')
                fobj.write('\t\t"name" : "domain-search",\n')
                fobj.write('\t\t"data" : ' + dns_search + '\n')
                fobj.write('\t}')

            if ntp_servers:
                fobj.write(',\n')
                fobj.write('\t{\n')
                fobj.write('\t\t"name" : "ntp-servers",\n')
                fobj.write(f'\t\t"data" : {ntp_servers}\n')
                fobj.write('\t}\n')
            fobj.write('\n')
            fobj.write('\t],\n')

def dhcp4_write_top_section (kea_config, fps):
    """
    Write out the top of configs
    """

    title = kea_config.title
    if not title:
        title = ''

    now = kea_config.now

    for stype in kea_config.server_types :
        fobj = fps[stype]
        if fobj:
            server = getattr(kea_config, stype)
            iface = server.interface
            hostname = server.hostname

            fobj.write('//\n')
            fobj.write(f'// Kea Config : {hostname}\n')
            fobj.write(f'//    Title : {title}\n')
            fobj.write(f'// Server type : {stype}\n')
            fobj.write(f'// Generated at : {now }\n')
            fobj.write('//\n')

            fobj.write('\n')
            fobj.write('{\n')
            fobj.write('"Dhcp4": {\n')
            fobj.write('\t"authoritative": true,\n')
            fobj.write('\t"interfaces-config":\n')
            fobj.write('\t{\n')
            fobj.write(f'\t\t"interfaces": ["{iface}"],\n')
            fobj.write('\t\t"dhcp-socket-type": "raw" \n')
            fobj.write('\t},\n')

            fobj.write('\n')
            fobj.write('\t"control-socket": {\n')
            fobj.write('\t\t"socket-type": "unix",\n')
            fobj.write('\t\t"socket-name": "/var/tmp/kea4-ctrl-socket"\n')
            fobj.write('\t},\n')

            fobj.write('\t"lease-database": {\n')
            fobj.write('\t\t"type": "memfile",\n')
            fobj.write('\t\t"persist": true,\n')
            fobj.write('\t\t"name": "/var/lib/kea/kea-leases4.csv",\n')
            fobj.write('\t\t"lfc-interval": 3600\n')
            fobj.write('\t},\n')

            fobj.write('\t"expired-leases-processing": {\n')
            fobj.write('\t\t"reclaim-timer-wait-time": 10,\n')
            fobj.write('\t\t"flush-reclaimed-timer-wait-time": 25,\n')
            fobj.write('\t\t"hold-reclaimed-time": 3600,\n')
            fobj.write('\t\t"max-reclaim-leases": 100,\n')
            fobj.write('\t\t"max-reclaim-time": 250,\n')
            fobj.write('\t\t"unwarned-reclaim-cycles": 5\n')
            fobj.write('\t},\n')

            fobj.write('\t"renew-timer": 900,\n')
            fobj.write('\t"rebind-timer": 1800,\n')
            fobj.write('\t"valid-lifetime": 14400,\n')

def dhcp4_write_peers (kea_config, fobj):
    """
    Write out the server section (the peers)
    """

    if not fobj:
        return

    num_peers = len(kea_config.server_types)

    fobj.write('\n\t\t\t\t"peers": [')
    count = 1
    for stype in kea_config.server_types :
        server = getattr(kea_config, stype)

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

        fobj.write('\n\t\t\t\t{')
        fobj.write(f'\n\t\t\t\t\t"name": "{name}",')
        fobj.write(f'\n\t\t\t\t\t"url": "{url}",')
        fobj.write(f'\n\t\t\t\t\t"basic-auth-user": "{auth_user}",')
        fobj.write(f'\n\t\t\t\t\t"basic-auth-password": "{auth_pass}",')
        fobj.write(f'\n\t\t\t\t\t"role": "{role}",')
        fobj.write(f'\n\t\t\t\t\t"auto-failover": {failover}\n')
        fobj.write('\n\t\t\t\t}')

        if count < num_peers:
            fobj.write(',')
        count = count + 1

    fobj.write('\n\t\t\t\t]')

def dhcp4_write_hooks_libs (kea_config, fps):
    """
    Write out the hooks library section
    """

    for stype in kea_config.server_types :
        fobj = fps[stype]
        if fobj:
            name = f'kea-{stype}'
            #role = stype

            fobj.write('\n')
            fobj.write('\t//\n')
            fobj.write('\t// Hooks\n')
            fobj.write('\t//')

            fobj.write('\n\t"hooks-libraries": [')
            fobj.write('\n\t\t{')
            fobj.write('\n\t\t\t"library": "/usr/lib/kea/hooks/libdhcp_lease_cmds.so",')
            fobj.write('\n\t\t\t"parameters": { }')
            fobj.write('\n\t\t}')

            if kea_config.has_standby:
                fobj.write(',')
                fobj.write('\n\t\t{')
                fobj.write('\n\t\t\t"library": "/usr/lib/kea/hooks/libdhcp_ha.so",')
                fobj.write('\n\t\t\t"parameters": {')
                fobj.write('\n\t\t\t"high-availability": [')
                fobj.write('\n\t\t\t{')
                fobj.write(f'\n\t\t\t\t"this-server-name": "{name}",')
                fobj.write('\n\t\t\t\t"mode": "hot-standby",')
                fobj.write('\n\t\t\t\t"heartbeat-delay": 10000,')
                fobj.write('\n\t\t\t\t"max-response-delay": 10000,')
                fobj.write('\n\t\t\t\t"max-ack-delay": 5000,')
                fobj.write('\n\t\t\t\t"max-unacked-clients": 5,')
                fobj.write('\n\t\t\t\t"sync-timeout": 60000,')

                dhcp4_write_peers(kea_config, fobj)

                fobj.write('\n\t\t\t}')
                fobj.write('\n\t\t\t]')       # high avail
                fobj.write('\n\t\t}')

                fobj.write('\n\t}')
            fobj.write('\n\t],')

def dhcp4_write_subnets (kea_config, fps):
    """
    Write out the subnet (we handle 1 subnet currently.
    """
    # pylint: disable=R0914,R0915
    #
    # handle multiple pool ranges in a subnet
    # pools: [{"pool": "range 1"}, {"pool": "range 2"}]
    #
    net = kea_config.net

    pools = net['pools']
    subnet = net['subnet']
    max_lifetime = net['max-valid-lifetime']

    option_data = net.get('option-data')
    if option_data:
        bcast = option_data.get('broadcast-address')
        routers = option_data.get('routers')
        ntp = option_data.get('ntp-servers')
        ntp_servers = list_to_strings(ntp)

    #
    # format pool ranges into kea format
    #
    pool_info = None
    for item in pools:
        if pool_info :
            pool_info = pool_info + f', {{"pool": "{item}"}}'
        else:
            pool_info = f'{{"pool": "{item}"}}'

    subnet_id = '1'
    for stype in kea_config.server_types :
        fobj = fps[stype]
        if fobj:
            server = getattr(kea_config, stype)
            iface = server.interface

            fobj.write('\n')
            fobj.write('\t//\n')
            fobj.write('\t// IPv4 subnet\n')
            fobj.write('\t//\n')

            fobj.write('\t"subnet4": [\n')
            fobj.write('\t{\n')
            fobj.write(f'\t\t"id": {subnet_id},\n')
            fobj.write(f'\t\t"subnet": "{subnet}",\n')
            fobj.write(f'\t\t"pools": [{pool_info}],\n')
            fobj.write(f'\t\t"max-valid-lifetime": {max_lifetime},\n')
            fobj.write('\t\t"authoritative": true,\n')
            fobj.write(f'\t\t"interface": "{iface}",\n')

            if option_data:
                fobj.write('\t\t"option-data":[\n')

                fobj.write('\t\t{\n')
                fobj.write('\t\t\t"space": "dhcp4",\n')
                fobj.write('\t\t\t"name": "broadcast-address",\n')
                fobj.write(f'\t\t\t"data" : "{bcast}"\n')
                fobj.write('\t\t},\n')

                fobj.write('\t\t{\n')
                fobj.write('\t\t\t"space": "dhcp4",\n')
                fobj.write('\t\t\t"name": "routers",\n')
                fobj.write(f'\t\t\t"data" : "{routers}"\n')
                fobj.write('\t\t},\n')

                fobj.write('\t\t{\n')
                fobj.write('\t\t\t"space": "dhcp4",\n')
                fobj.write('\t\t\t"name": "ntp-servers",\n')
                fobj.write(f'\t\t\t"data" : {ntp_servers}\n')
                fobj.write('\t\t}\n')

                fobj.write('\t\t],\n')

def dhcp4_write_reserved (kea_config, fps):
    """
    Write out the reserved hosts - mac and ip
    """

    reserved = kea_config.net.get('reserved')
    if not reserved:
        return

    for stype in kea_config.server_types :
        fobj = fps[stype]
        if fobj:
            fobj.write ('\n')
            fobj.write('\t\t//\n')
            fobj.write('\t\t// IP Reservations\n')
            fobj.write('\t\t//\n')

            fobj.write('\n')
            fobj.write('\t\t"reservation-mode": "out-of-pool",\n')
            fobj.write('\t\t"reservations": [\n')

            first = True
            for host in reserved:
                ip = reserved[host]['ip']
                mac = reserved[host]['hw-address']
                if not first:
                    fobj.write(',\n')
                else:
                    first = False
                fobj.write('\t\t{\n')
                fobj.write(f'\t\t\t"hostname": "{host}",\n')
                fobj.write(f'\t\t\t"hw-address": "{mac}",\n')
                fobj.write(f'\t\t\t"ip-address": "{ip}"\n')
                fobj.write('\t\t}')
            fobj.write('\n')
            fobj.write('\t\t]\n')
            fobj.write('\t}\n')
            fobj.write('\t],\n')


def dhcp4_write_loggers (kea_config, fps):
    """
    Write out the logging section
    """
    for stype in kea_config.server_types :
        fobj = fps[stype]
        if fobj:
            fobj.write('\n')
            fobj.write('\t"loggers": [\n')
            fobj.write('\t{\n')
            fobj.write('\t\t"name": "kea-dhcp4",\n')
            fobj.write('\t\t"output_options": [\n')
            fobj.write('\t\t{\n')
            fobj.write('\t\t\t"output": "/var/log/kea/kea-dhcp4.log",\n')
            fobj.write('\t\t\t"flush": false,\n')
            fobj.write('\t\t\t"maxsize": 1048576,\n')
            fobj.write('\t\t\t"maxver": 8\n')
            fobj.write('\t\t}\n')
            fobj.write('\t\t],\n')
            fobj.write('\t\t"severity": "WARN",\n')
            fobj.write('\t\t"debuglevel": 0\n')

            fobj.write('\t}\n')
            fobj.write(']\n')
            fobj.write('}\n')
            fobj.write('}\n')
