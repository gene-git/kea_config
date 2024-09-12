# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
 class_dns.py
 DNS address lookup - caches resolver for faster multiple lookups
 Part of gc_utils library
"""
import dns.resolver

class GcDns:
    """
    dns class using dns.resolver - provides caching
    """
    def __init__ (self, dns_server=None, dns_port=53, search_domains=None):
        """
        Cache resolvers so we initialize once
        """
        self.resolver = None
        self.dns_server = dns_server
        self.search_domains = search_domains

        self.resolver = dns.resolver.Resolver(configure=True)
        self.resolver.port = dns_port
        if dns_server:
            self.resolver.nameservers = [dns_server]
        if self.search_domains:
            self.resolver.search = [dns.name.from_text(dom) for dom in self.search_domains]
            self.resolver.use_search_by_default = True
        self.resolver.cache = dns.resolver.LRUCache()

    def query (self, host_or_ip, qtype='A'):
        """
        Used cached dns servers to perform dns query
            qtype : 'A", 'PTR'
        """
        # pylint: disable=C0103
        okay = False
        ipaddr = None

        if not self.resolver:
            return ipaddr

        try:
            if qtype == 'PTR' :
                res = self.resolver.resolve_address(host_or_ip)
            else:               # 'A'
                res = self.resolver.resolve(host_or_ip, qtype)
            okay = True

        except dns.exception.DNSException :
            okay = False

        if okay:
            ips = []
            for rdata in res:
                rec = rdata.to_text()
                if rec != '0.0.0.0' :
                    ips.append(rdata.to_text())

            if ips and len(ips) > 0:
                ipaddr = ips[0]
        return ipaddr

    def __getattr__(self, name):
        """ non-set items simply return None so easy to check existence"""
        return None
