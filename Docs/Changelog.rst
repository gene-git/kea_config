Changelog
=========

**[4.13.0] ----- 2024-12-31** ::

	    Git tags are now signed.
	    Update SPDX tags
	    Add git signing key to Arch Package
	    Bump python version
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.12.0] ----- 2024-12-19** ::

	    add new file toml.py
	    replace toml module with native tomllib which requires python >= 3.11
	    update license ids in source
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.10.0] ----- 2024-09-12** ::

	    dns.resolver now uses dns.resolver.LRUCache()
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.9.0] ----- 2024-05-23** ::

	    Add kea options:
	        "calculate-tee-times" : true
	        "offer-lifetime": 60
	      to output. Remove renew-timer, rebind-timer which are no longer needed now.
	    reservations: use FQDN for hostname.
	    Add kea_config global_options to config file:
	        min-valid-lifetime, valid-lifetime, max-valid-lifetime
	      Each can be overriden at the subnet level
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.8.4] ----- 2024-05-23** ::

	    Readme - add comment on compat with vers 2.4 and later
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.8.3] ----- 2024-05-22** ::

	    Add comment to readme about manually removing the deprecated option


**[4.8.2] ----- 2024-05-22** ::

	    typo in readme


**[4.8.1] ----- 2024-05-22** ::

	    Remove deprecated option "reservation-mode" output. kea versions after 2.4 will not start if kea-dhcp4 has the option
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.7.0] ----- 2024-04-26** ::

	    Add ctrl_agent_port option to config.
	        If not set, the ctrl agent port is set to 1 + dhcp port
	    update Docs/Changelog.rst Docs/kea_config.pdf


**[4.6.1] ----- 2023-12-19** ::

	    Update depends array in PKGBUILD
	    update Docs/Changelog.rst


**[4.6.0] ----- 2023-11-26** ::

	    Switch python backend build to hatch (was poetry)
	    update Docs/Changelog.rst


**[4.5.1] ----- 2023-09-27** ::

	    fix links in README
	    update Docs/Changelog.rst


**[4.5.0] ----- 2023-09-27** ::

	    Reorganize docs and move to rst
	    Now simple to build html and pdf docs using sphinx
	    update CHANGELOG.md


**[4.4.3] ----- 2023-05-18** ::

	    install: switch from pip to python installer package. This adds optimized bytecode
	    update CHANGELOG.md


**[4.4.2] ----- 2023-05-17** ::

	    Simplify Arch PKGBUILD and more closely follow arch guidelines
	    update CHANGELOG.md


**[4.4.1] ----- 2023-01-06** ::

	    Add SPDX licensing lines
	    update CHANGELOG.md


**[4.4.0] ----- 2022-12-14** ::

	    Use poetry to build wheel in PKGBUILD
	    Installer now uses pip install
	    Update readme build to use poetry
	    update CHANGELOG.md


**[4.3.2] ----- 2022-11-06** ::

	    remove un-needed comments
	    update CHANGELOG.md


**[4.3.1] ----- 2022-11-05** ::

	    small tweak to readme and sample config
	    tweak readme
	    aur package now available
	    update CHANGELOG


**[4.3.0] ----- 2022-11-05** ::

	    kea_config - Manage kea dhcp4 configs from single source config


