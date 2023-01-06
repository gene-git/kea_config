# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
 Write out kea dhcp4 configs
"""
from .tools import open_file
from .dhcp4 import dhcp4_write_top_section
from .dhcp4 import dhcp4_write_hooks_libs
from .dhcp4 import dhcp4_write_global_options
from .dhcp4 import dhcp4_write_subnets
from .dhcp4 import dhcp4_write_reserved
from .dhcp4 import dhcp4_write_loggers
from .agent import write_ctrl_agent

def _open_output_files (kea_conf) :
    """
    Open the kea config files for writing
    """
    conf_base = kea_conf.conf_base
    agent_base = kea_conf.agent_base

    fobj_conf = {}
    fobj_agent = {}
    for stype in kea_conf.server_types:
        #server = getattr(kea_conf, stype)
        fobj_conf[stype] = None
        fobj_agent[stype] = None

        fname = f'{conf_base}-{stype}.conf'
        fobj_conf[stype] = open_file (fname, 'w')

        fname = f'{agent_base}-{stype}.conf'
        fobj_agent[stype] = open_file (fname, 'w')

    return [fobj_conf, fobj_agent]

def _close_output_files(fobj_dict):
    for (_stype,fobj) in fobj_dict.items():
        if fobj:
            fobj.close()

def write_configs (kea_conf):
    """
    Write out all config sections
    """
    [fobj_conf, fobj_agent] = _open_output_files (kea_conf)

    #
    # Write the dhcp4 configs
    #
    dhcp4_write_top_section (kea_conf, fobj_conf)
    dhcp4_write_hooks_libs (kea_conf, fobj_conf)
    dhcp4_write_global_options (kea_conf, fobj_conf)
    dhcp4_write_subnets (kea_conf,  fobj_conf)
    dhcp4_write_reserved (kea_conf, fobj_conf)
    dhcp4_write_loggers (kea_conf, fobj_conf)

    #
    # Write the control agent configs
    #
    write_ctrl_agent (kea_conf, fobj_agent)

    _close_output_files(fobj_conf)
    _close_output_files(fobj_agent)
