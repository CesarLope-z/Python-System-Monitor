"""Funciones relacionadas con la red."""

import socket

import psutil


def get_network_info():
    """Devuelve IP local, interfaces y tráfico de red acumulado."""
    hostname = socket.gethostname()

    try:
        local_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        local_ip = "No disponible"

    link_family = getattr(psutil, "AF_LINK", None)
    interfaces = []

    for interface_name, addresses in psutil.net_if_addrs().items():
        interface = {
            "name": interface_name,
            "ipv4": [],
            "ipv6": [],
            "mac": [],
        }

        for address in addresses:
            if address.family == socket.AF_INET:
                interface["ipv4"].append(address.address)
            elif address.family == socket.AF_INET6:
                interface["ipv6"].append(address.address)
            elif link_family is not None and address.family == link_family:
                interface["mac"].append(address.address)

        interfaces.append(interface)

    io = psutil.net_io_counters()

    return {
        "hostname": hostname,
        "local_ip": local_ip,
        "interfaces": interfaces,
        "bytes_sent": io.bytes_sent,
        "bytes_received": io.bytes_recv,
    }
