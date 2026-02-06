.. SPDX-License-Identifier: GPL-2.0-or-later

##########
kea-config
##########

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
* `The Appendix`_


Please Note:

An Archlinux package can be built using the PKGBUILD from the packaging directory or from the AUR.
All git tags are signed with arch@sapience.com key which is available via WKD
or download from `sapience website <https://www.sapience.com/tech>`_. 
Add the key to your package builder gpg keyring.
The key is included in the Arch package and the source= line with *?signed* at the end can be used
to verify the git tag.  You can also manually verify the signature


Latest Changes
==============

**Version 6.0.0**

* Major Changes

  Our testing has not uncovered any issues, but it is always sensible to 
  backup the *kea-dhcp4* and *kea-ctrl-agent* config files (these are 
  the output of the *kea-config* tool) before running the new version.

  *kea-config* does keeps 1 backup copy of previous runs outputs as well.

* New dependency *python-ruamel-yaml*
* Add support for multiple network interfaces with separate subnets.
   
  The server section *interface* is replaced by *interfaces* that is now a list
  of pairs, (interface, subnet).  Note that even if the primary server supports 
  more than 1 interface/subnet, multiples are optional for standby and backup.

* Configuration file has been changed from TOML to YAML format.

  Existing config files will be auto converted to the new format. Comments will be lost
  unfortunately, so you may want to edit the file.

  Example configs have been updated using the new format (the previous one are there too).
  One example illustrates a server offering IPs for 2 different subnets, with each 
  subnet associated with it's own network interface.

* Code simplification and rewrite. Remove dynamic created classes and replace with 
  clearly defined classes. More robust (if less cool). Re-organize the code to 
  keep it more maintainable.

* Config variables removed.

  - *server_types*

    Each server is enabled using in the server section using *active: true* or disabled with *active: false*

* Backup of current kea configuration files.

  - Keeps a backup copy of each output kea file under "Prev" subdirectory.

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


  .. _The Appendix:

########
Appendix
########

Installation  
============

Available on

* `Github`_
* `Archlinux AUR`_

On Arch you can build using the PKGBUILD provided in packaging directory or from the AUR package.

You can manually install using pyton package tools *uv* and *uv-build*.

 .. code-block:: bash
    :caption: Manual Install

        rm -f dist/*
        /usr/bin/uv build --wheel --no-build-isolation
        root_dest="/"
        ./scripts/do-install $root_dest

When running as non-root then set root_dest to a user writable directory
This will install the executable */usr/bin/kea-config* along with a
sample config in */usr/share/kea_config*

Dependencies
============

* Run time

 * python       
 * dnspython       
 * ruamel-yaml       

* Building Package:

  * git
  * uv
  * uv-build
  * rsync

* Optional for building docs:

  * sphinx
  * texlive-latexextra  (archlinux packaguing of texlive tools)

Discussion and Next Steps
=========================

This version is for kea-dhcp4 (IPv4).

Most but not every available kea option is supported by kea-config. 
For example the high availibilty component of kea
allows for either hot-standby or load balancing. At present we support hot standby only. 
Hot standby has one server at a time actively serving clients, whereas in load balancing case
both servers are servicing clients at same time.


To create a version for kea-dhcp6, for example where a firewall is responsible for passing 
prefix delegation to the internal hosts, one needs an IPV6 internet connection; I am unable 
to work on this at the moment. It may also have significantly less utility than IPv4 dhcp.

kea-config is distro agnostic but I do maintain an Archlinux package on the AUR.

Older Changes
=============

Please see the Changelog's in Docs directory for full history.

* Code Reorg
* Switch packaging from hatch to uv
* Testing to confirm all working on python 3.14.2
* License GPL-2.0-or-later
* Code re-org/cleanup.
* Code now complies with PEP-8, PEP-257 and PEP-484 style and type annotations

* Socket dir now defaults to */var/run/kea*. 
  
  We prefer */run/kea* per Linux FHS, but since kea version 2.7.9 requires 
  the path to to be */var/run/kea/*. 
  See `kea docs <https://kea.readthedocs.io/en/stable/arm/dhcp4-srv.html#dhcp4-unix-ctrl-channel>`_. 
  There is a config option, *socket_dir*, to set this as well.

* Multiple gateway routers. option-data routers can now be a list of gateways.
* Add output option "calculate-tee-times" : true (replaces explicit renew-timer, rebind-timer)
* Add output option: "offer-lifetime": 60
* Add global input options: "min-valid-lifetime", "valid-lifetime", "max-valid-lifetime"

  These can be overriden at the subnet level

* If some lifetimes are set, missing ones are imputed using:

  min-valid-lifetime = valid-lifetime / 2
  max-valid-lifetime = valid-lifetime * 2

* reservations : use FQDN for hostname. Hostname must be requested by client for kea to send it.

* kea has deprecated the option *reservation-mode* for versions of kea newer than 2.4.
  We have now removed this option from *kea-config* generated output. 


Philosophy
==========

We follow the *live at head commit* philosophy as recommended by
Google's Abseil team [1]_.  This means we recommend using the
latest commit on git master branch. 


License
=======

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

* SPDX-License-Identifier: GPL-2.0-or-later
* Copyright (c) 2022-present Gene C

.. _Github: https://github.com/gene-git/kea_config
.. _Archlinux AUR: https://aur.archlinux.org/packages/kea_config

.. [1] https://abseil.io/about/philosophy#upgrade-support

