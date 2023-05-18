
# OVERVIEW of kea-config

## What is kea?

kea is a modern dhcp server from ISC (<https://www.isc.org/kea>) which supercedes its older
dhcp software. 

kea offers a nice feature set including the ability to have a hot standby server to pick up 
in case the primary is unavailable.
Its power also lurks behind a complicated configuration suite that, at least for me, is not 
terribly human friendly. 

Most notably each server requires it's own separate config and keeping them all 
synchronized can be a bit of a chore and which naturally is prone to human error.

## What is kea-config

kea-config provides a tool which takes a single configuration file as its input and 
it then generates the native kea configuration files needed from that single source of truth. 
By using a single configuration we can be assured that
the configs for the primary, standby and backup servers are consistent with one other.

It also provides the convenience of doing the DNS lookups for any host reservations, meaning 
the reservation is specified using hostname only not IP as expected by kea.

At the moment kea-config supports kea-dhcp4 and its companion control agent.

## Contents

    1. Installation 
    2. Using kea-config
    3. Summary of config variables
    4. Discussion and Next Steps

### 1. Installation  

Available on
 - [Github source ](https://github.com/gene-git/kea-config)
 - [Archlinux AUR](https://aur.archlinux.org/packages/kea_config)  
   The same PKGBUILD also in source tree under *pkg* directory.

kea-config is written in python and that is its sole dependency, so python must be installed.

You can run it out of the cloned repo (src/kea_config/kea-config.py) or install manually

        rm -f dist/*
        /usr/bin/python -m build --wheel --no-isolation
        ./scripts/do-install /

which will install */usr/bin/kea-config* and sample config in */usr/share/kea_config*

or on Arch just build and install the package from pkg/PKGBUILD or AUR.

# 2. Using kea-config 

Once installed, to use it, copy the sample config file in the *configs* dir, modify 
for your own setup and simply run it:

    kea-config -c <your.conf>

This will generate pairs of files, one kea config and one control agent config for each
of primary, standby and backup - or whatever subset you used in the conf file. 
    
e.g. it will create kea configs in the <conf_dir> which is defined config being used.

        kea-ctrl-agent-primary.conf
        kea-dhcp4-primary.conf

and similarly for standby and/or backup if requested. Each pair of files is to be used
on the corresponding server. e.g The 2 primary files are used on the kea-dhcp4 primary server.

One simple way to manage these is to copy the entire <conf_dir> to each kea server /etc/kea
then use sym links for kea config - linking to appropriate primary, standby or backup.

e.g. /etc/kea on primary would have :

        kea-dhcp4.conf -> <conf_dir>/kea-dhcp4-primary.conf
        kea-ctrl-agent.conf -> <conf_dir>/kea-ctrl-agent-primary.conf


# 3.  Summary of config variable:

Comments are anything starting with '#' and are ignored.
The conf file in standard TOML format and as usual sections are denoted in square brackets.
e.g.

        some_variable = 'xxx'
        [section_1]
            a_variable = 'hi'
            a_list = ['1', 'two', 'three']

See the sample config for details, but we'll summarize the main pieces here:

 - *title*
   For human use only - not used by kea-config.

 - *conf_dir*
   Directory where generated kea configs reside. What I do is rsync this directory to
   /etc/kea/ on each kea server. Each server then has a soft link to its own specific config.
   For example on my primary server I have
     - ln -s <conf_dir>/kea-ctrl-agent-primary.conf kea-ctrl-agent.conf
     -  ln -s <conf_dir>//kea-dhcp4-primary.conf kea-dhcp4.conf
   And similarly for standby and backup. 

 - *server_types*
   The list of servers used - should contain at least 'primary'. 
   e.g. server_types = ['primary',  'standby', 'backup']

 - [*global_options*]
   This section has some common dhcp information shared with dhcp clients:

        * domain-name-servers - list of DNS server IPs 
        * domain-name - what is sounds like
        * domain-search - list of (sub)domains to search (if any)
        * ntp-servers - list of local ntp server IPs (if any)

 - *[server.primary]* 
    Provides the information needed for the primary server
    interface, hostname, port, auth_user and auth_password

 - *[server.standby]* *[server.backup]*
   Same format as primary server section. Optional and only used if turned on in *server_types* list.

 - *[net]*
   This section describes the standard dhcp information including host IP reservations. 

     + dns_net  - internal domain, used to lookup IP for host reservations.
     + pools - list of IP ranges to use
     + subnet - what it sounds like
     + max-valid-lifetime - as usual in seconds 
     + *[net.option-data]*
       sub section with:
       + *broadcast-address*
       + *routers* - default gateway / route
       + *ntp-servers* (list)

        # host XXX 
        * *[net.reserved.XXX]*
          hardware-address = "mac address" 

Will reserve the IP for XXX based on dns lookup of XXX.
Have as many of these as needed.


# 4. Discussion and Next Steps

This version is for kea-dhcp4 (IPv4).

Not all kea options are supported by kea-config. For example the high availibilty component of kea
allows for either hot-standby or load balancing. At moment we only support hot standby. 
Hot standby has one server at a time actively serving clients, whereas in load balancing case
both servers are servicing clients at same time.

To create a version for kea-dhcp6, for example where a firewall is responsible for passing 
prefix delegation to the internal hosts, one needs an IPV6 internet connection; I am unable 
to work on this at the moment.

While kea-config is distro agnostic, I do provide an Archlinux package available on the AUR.

## License

Created by Gene C. and licensed under the terms of the MIT license.

 - SPDX-License-Identifier: MIT
 - Copyright (c) 2022-2023 Gene C

