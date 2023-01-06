# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
Writes out the control agent configs
"""
# pylint: disable=C0103


def write_ctrl_agent (kea_config, fps):
    """
    Write out the control agent kea configs
    """
    # pylint: disable=R0915
    now = kea_config.now

    for stype in kea_config.server_types:
        fobj = fps[stype]
        if fobj:
            server = getattr(kea_config, stype)

            #name = f'kea-{stype}'
            hostname = server.hostname
            ip = server.ip
            port = server.port
            #url = f'http://{ip}:{port}'
            auth_user = server.auth_user
            auth_pass = server.auth_password
            #role = stype

            fobj.write( f'// Kea Control Agent : {hostname}\n')
            fobj.write( f'//    Server tyoe : {stype}\n')
            fobj.write( f'//    Generated : {now}\n')
            fobj.write('\n')

            fobj.write('{\n')
            fobj.write('\t"Control-agent" : {\n')
            fobj.write(f'\t\t"http-host" : "{ip}",\n')
            fobj.write(f'\t\t"http-port" : {port},\n')

            fobj.write('\t\t"authentication" : {\n')
            fobj.write('\t\t\t"type" :"basic",\n')
            fobj.write('\t\t\t"realm" :"kea-control-agent",\n')
            fobj.write('\t\t\t"clients" : [\n')
            fobj.write('\t\t\t{\n')
            fobj.write(f'\t\t\t\t"user" : "{auth_user}",\n')
            fobj.write(f'\t\t\t\t"password" : "{auth_pass}"\n')
            fobj.write('\t\t\t}]\n')
            fobj.write('\t\t},\n')

            fobj.write('\t\t"control-sockets": {\n')
            fobj.write('\t\t\t"dhcp4": {\n')
            fobj.write('\t\t\t\t"socket-type": "unix",\n')
            fobj.write('\t\t\t\t"socket-name": "/var/tmp/kea4-ctrl-socket"\n')
            fobj.write('\t\t\t},\n')

            fobj.write('\t\t\t"dhcp6": {\n')
            fobj.write('\t\t\t\t"socket-type": "unix",\n')
            fobj.write('\t\t\t\t"socket-name": "/var/tmp/kea6-ctrl-socket"\n')
            fobj.write('\t\t\t},\n')

            fobj.write('\t\t\t"d2": {\n')
            fobj.write('\t\t\t\t"socket-type": "unix",\n')
            fobj.write('\t\t\t\t"socket-name": "/var/tmp/kea-ddns-ctrl-socket"\n')
            fobj.write('\t\t\t}\n')

            fobj.write('\t\t},\n')

            fobj.write('\t\t"loggers": [\n')
            fobj.write('\t\t{\n')
            fobj.write('\t\t\t"name": "kea-ctrl-agent",\n')
            fobj.write('\t\t\t"output_options": [\n')
            fobj.write('\t\t\t{\n')
            fobj.write('\t\t\t\t"output": "/var/log/kea/kea-ctrl-agent.log",\n')
            fobj.write('\t\t\t\t"maxsize": 1048576,\n')
            fobj.write('\t\t\t\t"maxver": 8\n')
            fobj.write('\t\t\t}\n')
            fobj.write('\t\t\t],\n')
            fobj.write('\t\t"severity": "WARN",\n')
            fobj.write('\t\t"debuglevel": 0\n')
            fobj.write('\t\t}\n')
            fobj.write('\t\t]\n')

            fobj.write('\t}\n')
            fobj.write('}\n')
