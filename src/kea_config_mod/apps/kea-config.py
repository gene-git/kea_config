#!/usr/bin/python
# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
kea config generator tool

Uses config file (toml format) to produce consistent configs for each of:
 primary, standby and backup servers as well as control agent.

The config to be consumed :
  use -c <config>     - defaults to kea-dhcp4-setup.conf

Outputs:
  Are put in the 'conf_dir' directory specified in the config file.
  For each of primary, standby and backup there will be dhcp4 config
  and control agent config.

  Copy each generated config to its respective server.
  You should run 'test' mode to confirm

Usage:
  ./gen-kea-conf.py -c <config>

  Then copy the appropriate configs for dhcp4 and
  ctrol-agent /etc/kea on corresonding server

 e.g. on primary:
   cd /etc/kea
   (save current kea-dhc4.conf and ctrl-agent.conf)

   test - on actual server as interfaces are checkedj.
       kea-dhcp4 -t kea-dhcp4-primary.conf
       kea-ctrl-agent -t kea-ctrl-agent-primary.conf

 All being well:
   ln -s kea-dhcp4-primary.conf kea-dhcp4.conf
   ln -s kea-ctrl-agent-primary.conf kea-ctrl-agent.conf

   systemctl restart kea-ctril-agent
   systemctl restart kea-dhcp4
"""
# pylint: disable=invalid-name
from kea_config_mod.kea import KeaConfig


def main():
    """
    kea config generator tool
    """
    kea_conf = KeaConfig()
    if not kea_conf:
        return

    okay = kea_conf.config_setup()
    if not okay:
        return

    kea_conf.save_configs()


if __name__ == '__main__':
    main()
