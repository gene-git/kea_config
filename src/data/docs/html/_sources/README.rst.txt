.. SPDX-License-Identifier: GPL-2.0-or-later

==========
kea-config
==========

Overview
========

**What is kea?**

kea is a modern dhcp server from `ISC <https://www.isc.org/kea>`_ which supercedes their older
dhcp software. 

kea offers a nice feature set including the ability to have a hot standby to pick up 
in case the primary is unavailable.

However, it's power lurks behind a complicated configuration suite that, at least for me, is not 
terribly human friendly. 

Perhaps most notable is that each of the servers requires it's own separate configuration and 
keeping them all synchronized can be a bit of a chore and naturally is prone to human error
unless a tool is used to ensure each server config is consistent.

**What is kea-config?**

kea-config provides the tool that has a single configuration input file from which 
it generates the native kea configuration files.

By using a single configuration we guarantee that the configs kea needs 
for the primary, standby and backup servers are always consistent with one other.

*kea-config* also has the convenience of doing DNS lookups for any host reservations, meaning 
the IP host reservations are specified by hostname and the IP, from DNS lookup,
is then output for *kea-dhcp4* to use..

*kea-config* supports **kea-dhcp4** and its companion control agent.

Contents

* `Overview`_
* `Latest Changes`_
* `Using kea-config`_
* `Configuration`_
* :ref:`The Appendix`


Please Note:

An Archlinux package can be built using the PKGBUILD from the packaging directory or from the AUR.
All git tags are signed with arch@sapience.com key which is available via WKD
or download from `sapience website <https://www.sapience.com/tech>`_. 
Add the key to your package builder gpg keyring.
The key is included in the Arch package and the source= line with *?signed* at the end can be used
to verify the git tag.  You can also manually verify the signature


Latest Changes
==============

**6.5.1**

* switch to meson/meson-python for build/package management
* add pytest checks and checkdepends on pytest

Using kea-config 
================

kea-config depends on python, dnspython and ruamel-yaml.

To use it after installation,  copy a sample config file from the *examples* dir and modify 
appropriately for your use case. When ready run it to generate the set of
input files for *kea* to use:

.. code-block:: bash

    kea-config -c <your-config.yaml>

It can also be run from the git source repo:

.. code-block:: bash

    PYTHONPATH=src src/kea_config_mod/apps/kea-config.py -c <your-config.yaml>

The yaml config also specifes the directory where the outputs are to be written.

For each (active) server section (primary, standby and backup), it creates one configuration 
file to for use by *kea-dhcp4* and one for *kea-ctrl-agent* (the control agent). 

The *primary* server must be provided in the input config file,  
while *standby* and *backup* servers are optional. 

For example, the resulting kea configs for the primary server will be written to 
the directory specified by *conf_dir*:

.. code-block:: text

        kea-ctrl-agent-primary.conf
        kea-dhcp4-primary.conf

Similarly for standby and/or backup servers if so requested. Each pair of files is to be used
on the corresponding server. e.g The 2 primary files are for use on the *kea-dhcp4* primary server.

One simple way to manage these is to copy the entire *conf_dir* to each server /etc/kea/
and use symlinks /etc/kea/ poinging to appropriate primary, standby or backup config.

e.g. /etc/kea on primary could have:

.. code-block:: text

        kea-dhcp4.conf -> <conf_dir>/kea-dhcp4-primary.conf
        kea-ctrl-agent.conf -> <conf_dir>/kea-ctrl-agent-primary.conf


Note that if the input config, *xxx.conf*, passed to 

.. code-block:: text

    kea-congig -c xxx.conf
    
is a pre-6.0 (*.conf*) file, 
then a *xxx.yaml* version will be written in the same directory. 

The yaml file should be used thereafter. You may want to 
check it and/or add comments. Uunfortunately any comments in the old config will 
be lost in the automatic conversion to yaml (my apologies).

Configuration
-------------

Config files are in YAML. Earlier versions used TOML. As mentioned above, version 6.0 
of *kea-config* will automatically convert these to the new yaml format.

In yaml, comments begin with '#' and can be at for an entire line or part of a line.

Two example config files are provided in the *examples* directory and make a
good starting template.
The installer script puts these into */usr/share/kea_config/examples*.

One of the examples has a primary server serving DHCP over a single
network interface. It includes a high availibility standby server as well as 
a backup server.

The second example expands on the first one, and introduces a second subnet that is on a 
a separate netowrk interface. This offers IPs out of pools belonging to the second subnet. 

Each server configuration must have an *interfaces:* varieble that is a list of 
*(interface, subnet)* pairs. That server is then able to offer DHCP for each subnet
over it's companion interface.

While the primary server is distinctive in being required, any server may provide
2 (or more) subnets. In the example, the primary server has 2 subnets.

For testing purposes, it can be useful to run:

.. code:: bash

    kea-dhcp4 -t kea-dhcp4-xxx
    # or
    kea-dhcp4 -T kea-dhcp4-xxx

using the corresponding output *kea-dhcp4-xxx* file for the server the test is run on.
Since *kea-dhcp4* validates not only the syntax, but also subnets and network 
interfaces, this test must be run on the actual server.

Please see the examples for full details. Below is a summary of the main 
parts of the *kea-config* input file.

.. code:: text

   ---
   # config snippet
    title: Example 1 Config
    conf_dir: Example-1
    ctrl_agent_port: '8762'
    socket_dir: /var/run/kea
    global_options:
      domain_name_servers:
        - 10.1.0.10
        - 10.1.0.11
        - 10.1.0.12
      domain_name: sub1.example.com
      domain_search:
        - sub1.example.com
        - foo.com
      ntp_servers:
        - 10.1.0.10
        - 10.1.0.14
      min_valid_lifetime: 14400
      valid_lifetime: 28800
      max_valid_lifetime: 57600
    servers:
      primary:
        hostname: server1.sub1.example.com
        port: '8761'
        auth_user: kea-ctrl
        auth_password: xxxSecretHotSauce
        stype: primary
        subdomain: sub1.example.com
        active: true
        interfaces:
          -
            - eno1
            - 10.1.0.0/24
      standby:
        hostname: server2.sub1.example.com
        ...

      backup:
        hostname: server3.sub1.example.com
        ...

    nets:
      // first subnet
      10.1.0.0/24:
        pools:
          - 10.1.0.72 - 10.1.0.95
          - 10.1.0.193 - 10.1.0.250
        subnet: 10.1.0.0/24
        option_data:
          broadcast_address: 10.1.0.255
          routers: 10.1.0.1
          ntp_servers:
            - 10.1.0.10
            - 10.1.0.14
        reserved:
          ap0:
            hw_address: cc:aa:aa:aa:aa:01
          bob_laptop:
            hw_address: cc:aa:aa:aa:aa:02
          web_serv1:
            hw_address: cc:aa:aa:aa:aa:03
        subdomain: sub1.example.com
      // second subnet
      10.2.0.0/24:
        ...


It should be pretty self-exaplanatory.

* *title:* 

  For human use only - not used by kea-config.

* *conf_dir:*

  Directory where generated kea configs reside. What I do is rsync this directory to
  /etc/kea/ on each kea server. Each server then has a soft link to its own specific config.
  For example on my primary server I have

* *global_options:*

  This section provides common dhcp information to be shared with dhcp clients:
  It is generally better for each *net* section to have it's own.

* *servers:* 

  Provides the information needed for the each server. Primary is required
  while standby and backare are optional.
  Having a standby server is strongly recommended for high availibility.
 
* *nets*

  This section describes one or more networks to offer DHCP. Each section has
  the subnet, sub-domain, pool of IP addresses and so on for that network.

  Any server offering a network, must have that subnet on one of it's network interfaces
  and every interface it will serve DHCP on, must be listed in the server's interface section.

  Each subnet has it's own list of IP host resevations which are proivided by short form 
  *hostname* and it's MAC (hardware) address. Local DNS is used to lookup each host's 
  IP address from it's hostname. Please be sure that any host in the reservation list
  can have it's IP retrieved via DNS

