import ipaddress

def anonymize_ip(ip: str | None) -> str | None:
    if not ip:
        return None
    try:
        addr = ipaddress.ip_address(ip)
        if addr.version == 4:
            # обнулим последний октет: 192.168.1.123 -> 192.168.1.0
            parts = ip.split(".")
            return ".".join(parts[:3] + ["0"])
        else:
            # для IPv6 обрежем до /64
            network = ipaddress.IPv6Network((addr, 64), strict=False)
            return str(network.network_address)
    except ValueError:
        return None
