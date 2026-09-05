.. SPDX-License-Identifier: GPL-2.0-or-later

.. _The Appendix:

========
Appendix
========

Installation  
============

Available on
* `Github <https://github.com/gene-git/kea_config>`_
* `Archlinux AUR <https://aur.archlinux.org/packages/kea_config>`_

On Arch you can build using the PKGBUILD provided in packaging directory or from the AUR package.

 .. code-block:: bash
    :caption: Manual Install

        ./scripts/do-build
        ./scripts/do-build <destination-directory>

Dependencies
============

* Run time

  * python       
  * dnspython       
  * ruamel-yaml       

* Building Package:

  * git
  * meson
  * meson-python
  * rsync

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


License
=======

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

* SPDX-License-Identifier: GPL-2.0-or-later
* SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>

