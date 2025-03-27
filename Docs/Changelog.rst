=========
Changelog
=========

**Tags**     : 1.0 (2022-03-04) -> 4.15.0 (2025-03-27)
             : 132 commits.

* 2025-03-27  : **4.15.0**

                Update version file
                buglet with routers array too many double quotes"
                option-data routers can be single IP or list of IPs
 2025-03-23     update Docs/Changelog.rst

* 2025-03-23  : **4.14.0**

                Update version file
                Better error handling of host reservations/dns_net when missing info
 2024-12-31     update Docs/Changelog.rst

* 2024-12-31  : **4.13.0**

                Update version file
                Git tags are now signed.
                Update SPDX tags
                Add git signing key to Arch Package
                Bump python version
 2024-12-19     update Docs/Changelog.rst

* 2024-12-19  : **4.12.0**

                Update version file
                update license ids in source
                update Docs/Changelog.rst

* 2024-12-19  : **4.11.0**

                Update version file
                update PKGBUILD deps
                replace toml module with native tomllib which requires python >= 3.11
 2024-09-12     update Docs/Changelog.rst

* 2024-09-12  : **4.10.0**

                Update version file
                dns.resolver now uses dns.resolver.LRUCache()
 2024-05-23     update Docs/Changelog.rst

* 2024-05-23  : **4.9.0**

                Update version file
                update readme
                change order of lifetime output : min_life, life, max_life
                Bug fix imputing missing lifetimes.
                  If any of lifetime, min_lifetime or max_lifetime are missing impute them
                  using:
                    min_lifetime = lifetime / 2
                    max_lifetime = lifetime *2
                Add kea options:
                    "calculate-tee-times" : true
                    "offer-lifetime": 60
                  Remove renew-timer, rebind-timer which are no longer needed now.
                reservations - for "hostname" use FQDN
                Add global_options: min-valid-lifetime, valid-lifetime, max-valid-lifetime
                which can be overriden
                at the subnet level.
                update Docs/Changelog.rst

* 2024-05-23  : **4.8.4**

                Update version file
                Readme - add comment on compat with vers 2.4 and later
 2024-05-22     update Docs/Changelog.rst

* 2024-05-22  : **4.8.3**

                Update version file
                Add comment to readme about manually removing the deprecated option
                update Docs/Changelog.rst

* 2024-05-22  : **4.8.2**

                Update version file
                update Docs/Changelog.rst
                Update version file
                typo in readme
                update Docs/Changelog.rst

* 2024-05-22  : **4.8.1**

                Update version file
                update Docs/Changelog.rst

* 2024-05-22  : **4.8.0**

                Update version file
                Remove deprecated option "reservation-mode"
 2024-04-26     update Docs/Changelog.rst

* 2024-04-26  : **4.7.0**

                update project version
                bah kea_config is class not dict
                update sample config
                Add ctrl_agent_port option to config.
                If not set, the ctrl agent port is set to 1 + dhcp port
 2023-12-19     update Docs/Changelog.rst

* 2023-12-19  : **4.6.1**

                update project version
                Update depends array in PKGBUILD
 2023-11-26     update Docs/Changelog.rst

* 2023-11-26  : **4.6.0**

                update project version
                Switch python backend build to hatch
 2023-09-27     update Docs/Changelog.rst

* 2023-09-27  : **4.5.1**

                update project version
                fix links in README
                update Docs/Changelog.rst

* 2023-09-27  : **4.5.0**

                update project version
                Reorganize docs and move to rst
 2023-05-18     update CHANGELOG.md

* 2023-05-18  : **4.4.3**

                Update build info in README
                update CHANGELOG.md
                update project version
 2023-05-17     update CHANGELOG.md

* 2023-05-17  : **4.4.2**

                update project version
                Simplify Arch PKGBUILD and more closely follow arch guidelines
 2023-01-06     update CHANGELOG.md

* 2023-01-06  : **4.4.1**

                update project version
                Add SPDX licensing lines
 2022-12-14     update CHANGELOG.md

* 2022-12-14  : **4.4.0**

                update project version
                Update readme build to use poetry
                Use poetry to build wheel in PKGBUILD
                Installer now uses pip install
 2022-11-20     improve bash variable check in installer - no functional change
 2022-11-06     update CHANGELOG.md

* 2022-11-06  : **4.3.2**

                update project version
                remove unused comments
 2022-11-05     update CHANGELOG.md

* 2022-11-05  : **4.3.1**

                update project version
                small readme tweak
                tidy up config sameple a bit
                tidy up sample config
                tweak readme
                aur package now uploaded
                update CHANGELOG.md

* 2022-11-05  : **4.3.0**

                update project version
                typo in installer config -> congigs
                installer cleanup
                update CHANGELOG.md

* 2022-11-05  : **4.2.0**

                update project version
                Only create /usr/bin/kea-config (no more gen-kea-config)
                update CHANGELOG.md

* 2022-11-05  : **4.1.0**

                update project version
                tidy readme, MIT license, copy dns from gc_dns to keep this standalone
                tidy readme, MIT license, copy dns from gc_dns to keep this standalone
 2022-11-04     tweak installer
                tidy do-install
                do-install change changelog to CHANGELOG
                typo
                add README
                update CHANGELOG.md

* 2022-11-04  : **4.0**

                update project version
                Switch to standard python PEP-518  packaging

* 2022-09-22  : **3.1**

                Remove local class_dns file
                update changelog
                Remove local dns class and use GcDns class from gc_utils module
 2022-09-19     update do-install to handle filename change Changelog.md
                update changelog

* 2022-09-19  : **3.0**

                Skip HA when only primary
                add phone
                fix more silly
                normalize incoming dst
                remove duplicate // in link
                Missing makedir in do-install
                typo
                add link in /usr/bin/gc-kea-config for convenience
 2022-06-09     fix do-install config dir
                typo in changelog

* 2022-06-09  : **2.2**

                Changelog
                Add license
                add configs dir
                Install script for package build

* 2022-06-09  : **2.1**

                lint picking

* 2022-06-08  : **2.0**

                Rewrite with classes
 2022-03-05     fix typo in agent. Turn off pdb

* 2022-03-04  : **1.0**

                Tidy more - move config extract to classes file
                renamed sameple config
                Add conreol agent
                output now in configurable directory
                split single python file into smaller components;
                ;
                tidy
                Better control over file names etc
                error handling for dns lookups
 2022-03-03     Initial commit - generate kea-dhcp4 server configs


