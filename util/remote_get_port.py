#!/usr/bin/env python3
"""
seed a database with available ports
"""
import socket
from sys import argv
# import psutil


def check_port(port, local=False):
    """
    check if a perticulart port is in use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def get_available_port(port_ignore):
    """
    get ports that are available
    """
    port_ignore = port_ignore + [22,80, 443,21,25,53,110,143,993,995,3306,5432,6379,8000,8080,8888, 5000]
    ports = []
    # port_range = range(1024, 6066)
    port_range = range(1024, 2000)
    for port in port_range:
        if port in port_ignore:
            continue
        if not check_port(port):
            ports.append(port)
    return ports

if __name__ == "__main__":
    arg = eval(argv[1])
    if len(argv) == 3:
        if argv[2] == '--check-port':
            print(check_port(arg))
        elif argv[2] == '--assert-port':
            assert check_port(arg)
        else:
            print('incorrect arg')
    elif len(argv) == 2:
        print(get_available_port(arg))
    else:
        print('incorrect arg')
