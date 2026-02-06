Changelog
=========

Tags
====

.. code-block:: text

	4.3.0 (2022-11-05) -> 6.1.0 (2026-02-06)
	61 commits.

Commits
=======


* 2026-02-06  : **6.1.0**

.. code-block:: text

              - Version 6.0.0
            
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
                  subnet associated with its own network interface.
            
                * Code simplification and rewrite. Remove dynamic created classes and replace with
                  clearly defined classes. More robust (if less cool). Re-organize the code to
                  keep it more maintainable.
            
                * Config variables removed.
                  - *server_types*
                    Each server is enabled using in the server section using *active: true* or disabled with *active: false*
            
                * Backup of current kea configuration files.
                  - Now keeps a backup copy of each output kea file under "Prev" subdirectory before generating
                    any ones.
 2026-01-06   ⋯

.. code-block:: text

              - update Docs/Changelog

* 2026-01-06  : **5.2.2**

.. code-block:: text

              - PKGBUILD small change
 2026-01-04   ⋯

.. code-block:: text

              - update Docs/Changelog

* 2026-01-04  : **5.2.1**

.. code-block:: text

              - Update arch PKGBUILD
              - update Docs/Changelog

* 2026-01-04  : **5.2.0**

.. code-block:: text

              - ** 5.2.0**
            
                * Code Reorg
                * Switch packaging from hatch to uv
                * Testing to confirm all working on python 3.14.2
                * License GPL-2.0-or-later
 2025-07-20   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/kea_config.pdf

* 2025-07-20  : **5.0.1**

.. code-block:: text

              - readme - more rst tweaks
              - more readme
              - Readme: tidy up some rst
              - update Docs/Changelog Docs/kea_config.pdf

* 2025-07-20  : **5.0.0**

.. code-block:: text

              - update Docs/Changelog Docs/kea_config.pdf
              - Code re-org/cleanup.
                Code now complies with PEP-8, PEP-257 and PEP-484 style and type annotations
 2025-05-29   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/kea_config.pdf

* 2025-05-29  : **4.16.0**

.. code-block:: text

              - Make default socket_dir "/var/run/kea". Linux FHS recommends "/run".
                  "/var/run" is typically a legacy compatibility symlink. Unclear why kea us requiring legacy paths
 2025-03-27   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2025-03-27  : **4.15.0**

.. code-block:: text

              - option-data routers can be single IP or list of IPs
 2025-03-23   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2025-03-23  : **4.14.0**

.. code-block:: text

              - Better error handling of host reservations/dns_net when missing info
 2024-12-31   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-12-31  : **4.13.0**

.. code-block:: text

              - Git tags are now signed.
                Update SPDX tags
                Add git signing key to Arch Package
                Bump python version
 2024-12-19   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-12-19  : **4.12.0**

.. code-block:: text

              - add new file toml.py
              - replace toml module with native tomllib which requires python >= 3.11
                update license ids in source
 2024-09-12   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-09-12  : **4.10.0**

.. code-block:: text

              - dns.resolver now uses dns.resolver.LRUCache()
 2024-05-23   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-05-23  : **4.9.0**

.. code-block:: text

              - Add kea options:
                    "calculate-tee-times" : true
                    "offer-lifetime": 60
                  to output. Remove renew-timer, rebind-timer which are no longer needed now.
                reservations: use FQDN for hostname.
                Add kea_config global_options to config file:
                    min-valid-lifetime, valid-lifetime, max-valid-lifetime
                  Each can be overriden at the subnet level
              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-05-23  : **4.8.4**

.. code-block:: text

              - Readme - add comment on compat with vers 2.4 and later
 2024-05-22   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-05-22  : **4.8.3**

.. code-block:: text

              - Add comment to readme about manually removing the deprecated option

* 2024-05-22  : **4.8.2**

.. code-block:: text

              - typo in readme

* 2024-05-22  : **4.8.1**

.. code-block:: text

              - Remove deprecated option "reservation-mode" output. kea versions after 2.4 will not start if kea-dhcp4 has the option
 2024-04-26   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2024-04-26  : **4.7.0**

.. code-block:: text

              - Add ctrl_agent_port option to config.
                    If not set, the ctrl agent port is set to 1 + dhcp port
 2023-12-19   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/kea_config.pdf

* 2023-12-19  : **4.6.1**

.. code-block:: text

              - Update depends array in PKGBUILD
 2023-11-26   ⋯

.. code-block:: text

              - update Docs/Changelog.rst

* 2023-11-26  : **4.6.0**

.. code-block:: text

              - Switch python backend build to hatch (was poetry)
 2023-09-27   ⋯

.. code-block:: text

              - update Docs/Changelog.rst

* 2023-09-27  : **4.5.1**

.. code-block:: text

              - fix links in README
              - update Docs/Changelog.rst

* 2023-09-27  : **4.5.0**

.. code-block:: text

              - Reorganize docs and move to rst
                Now simple to build html and pdf docs using sphinx
 2023-05-18   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-05-18  : **4.4.3**

.. code-block:: text

              - install: switch from pip to python installer package. This adds optimized bytecode
 2023-05-17   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-05-17  : **4.4.2**

.. code-block:: text

              - Simplify Arch PKGBUILD and more closely follow arch guidelines
 2023-01-06   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2023-01-06  : **4.4.1**

.. code-block:: text

              - Add SPDX licensing lines
 2022-12-14   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-12-14  : **4.4.0**

.. code-block:: text

              - Use poetry to build wheel in PKGBUILD
                Installer now uses pip install
                Update readme build to use poetry
 2022-11-06   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-06  : **4.3.2**

.. code-block:: text

              - remove un-needed comments
 2022-11-05   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-05  : **4.3.1**

.. code-block:: text

              - small tweak to readme and sample config
              - tweak readme
              - aur package now available
              - update CHANGELOG

* 2022-11-05  : **4.3.0**

.. code-block:: text

              - kea_config - Manage kea dhcp4 configs from single source config


