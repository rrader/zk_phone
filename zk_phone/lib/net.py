from netifaces import interfaces, ifaddresses, AF_INET


def get_ips():
    ips = []
    for iface in interfaces():
        if iface == 'lo':
            continue
        ip = ifaddresses(iface).get(AF_INET)
        if ip:
            ips.extend(i['addr'] for i in ip)
    return ips


if __name__ == "__main__":
    print(get_ips())
