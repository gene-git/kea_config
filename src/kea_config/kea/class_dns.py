# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 class_dns.py
 DNS address lookup - caches resolver for faster multiple lookups
 Part of gc_utils library
"""
from typing import (Any)
import dns.resolver


class Dns:
    """
    dns class using dns.resolver - provides caching
    """
    def __init__(self,
                 dns_server: str | list[str] = '',
                 dns_port: int = 53,
                 search_domains: str | list[str] = ''):
        """
        Cache resolvers and initialize once
        """
        self.resolver: dns.resolver.Resolver
        self.dns_server: list[str] = []
        self.search_domains: list[str] = []

        self.resolver = dns.resolver.Resolver(configure=True)
        self.resolver.port = dns_port

        #
        # Use any provided server(s)
        #
        if dns_server:
            if isinstance(dns_server, list):
                self.dns_server = dns_server
                self.resolver.nameservers = dns_server
            else:
                self.dns_server = [dns_server]
                self.resolver.nameservers = [dns_server]

        #
        # Search domains
        #
        if search_domains:
            if isinstance(search_domains, list):
                self.search_domains = search_domains
            else:
                self.search_domains = [search_domains]

            self.resolver.search = [
                    dns.name.from_text(dom) for dom in self.search_domains
                    ]
            self.resolver.use_search_by_default = True

        #
        # Cache
        # - Cache() or LRUCache()
        #
        self.resolver.cache = dns.resolver.Cache()

    def query(self,
              query: str,
              rr_type: str = 'A',
              one_rr: bool = True
              ) -> str | list[str]:
        """
        Used cached dns servers to perform dns query
            rr_type : 'A", 'PTR'
        By default if query returns multiple resource rescords
        we return the first.  If one_rr is False,
        then list of all records are returned.
        """
        rrs: list[str] = []
        rr: str = ''

        resolver = self.resolver
        if not resolver or not query:
            return rr if one_rr else rrs

        try:
            if rr_type == 'PTR':
                res = self.resolver.resolve_address(query)
            else:
                res = self.resolver.resolve(query, rr_type)

        except dns.exception.DNSException:
            return rr if one_rr else rrs

        for rdata in res:
            rec_str = rdata.to_text()
            if rec_str != '0.0.0.0':
                rrs.append(rec_str)

        if one_rr:
            if rrs and len(rrs) > 0:
                rr = rrs[0]
            return rr
        return rrs

    def __getattr__(self, name: str) -> Any:
        """ non-set items simply return None so easy to check existence"""
        return None
