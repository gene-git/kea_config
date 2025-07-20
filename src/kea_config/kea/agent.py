# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Writes out the control agent configs
"""
# pylint: disable=duplicate-code

from .kea_types import FobConf
from .kea_data import KeaConfigData


def write_ctrl_agent(conf: KeaConfigData, fobs: FobConf):
    """
    Write out the control agent kea configs
    """
    # pylint: disable=R0915
    now = conf.now
    port = conf.ctrl_agent_port
    socket_dir = conf.socket_dir

    for stype in conf.server_types:
        fob = fobs[stype]
        if fob:
            server = getattr(conf, stype)
            #
            # if no ctrl agent port in config, then port = 1 + dhcp server port
            #
            hostname = server.hostname
            ip = server.ip
            if not port:
                port = str(int(server.port) + 1)

            auth_user = server.auth_user
            auth_pass = server.auth_password

            fob.write(f'// Kea Control Agent : {hostname}\n')
            fob.write(f'//    Server tyoe : {stype}\n')
            fob.write(f'//    Generated : {now}\n')
            fob.write('\n')

            fob.write('{\n')
            fob.write('\t"Control-agent" : {\n')
            fob.write(f'\t\t"http-host" : "{ip}",\n')
            fob.write(f'\t\t"http-port" : {port},\n')

            fob.write('\t\t"authentication" : {\n')
            fob.write('\t\t\t"type" :"basic",\n')
            fob.write('\t\t\t"realm" :"kea-control-agent",\n')
            fob.write('\t\t\t"clients" : [\n')
            fob.write('\t\t\t{\n')
            fob.write(f'\t\t\t\t"user" : "{auth_user}",\n')
            fob.write(f'\t\t\t\t"password" : "{auth_pass}"\n')
            fob.write('\t\t\t}]\n')
            fob.write('\t\t},\n')

            fob.write('\t\t"control-sockets": {\n')
            fob.write('\t\t\t"dhcp4": {\n')
            fob.write('\t\t\t\t"socket-type": "unix",\n')

            txt = f'{socket_dir}/kea4-ctrl-socket'
            fob.write(f'\t\t\t\t"socket-name": "{txt}"\n')
            fob.write('\t\t\t},\n')

            fob.write('\t\t\t"dhcp6": {\n')
            fob.write('\t\t\t\t"socket-type": "unix",\n')
            txt = f'{socket_dir}/kea6-ctrl-socket'
            fob.write(f'\t\t\t\t"socket-name": "{txt}"\n')
            fob.write('\t\t\t},\n')

            fob.write('\t\t\t"d2": {\n')
            fob.write('\t\t\t\t"socket-type": "unix",\n')

            txt = f'{socket_dir}/kea-ddns-ctrl-socket'
            fob.write(f'\t\t\t\t"socket-name": "{txt}"\n')
            fob.write('\t\t\t}\n')

            fob.write('\t\t},\n')

            fob.write('\t\t"loggers": [\n')
            fob.write('\t\t{\n')
            fob.write('\t\t\t"name": "kea-ctrl-agent",\n')
            fob.write('\t\t\t"output_options": [\n')
            fob.write('\t\t\t{\n')
            fob.write('\t\t\t\t"output": "/var/log/kea/kea-ctrl-agent.log",\n')
            fob.write('\t\t\t\t"maxsize": 1048576,\n')
            fob.write('\t\t\t\t"maxver": 8\n')
            fob.write('\t\t\t}\n')
            fob.write('\t\t\t],\n')
            fob.write('\t\t"severity": "WARN",\n')
            fob.write('\t\t"debuglevel": 0\n')
            fob.write('\t\t}\n')
            fob.write('\t\t]\n')

            fob.write('\t}\n')
            fob.write('}\n')
