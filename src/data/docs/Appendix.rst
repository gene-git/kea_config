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

License
=======

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

* SPDX-License-Identifier: GPL-2.0-or-later
* SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>

