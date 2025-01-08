#!/usr/bin/env python3
"""
seed a database with available ports
"""
import socket
from os import getenv
from fabric import Connection
# import psutil


def check_port(port, local=False):
    """
    check if a perticulart port is in use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((getenv("HOST_IP", "127.0.0.1"), port)) == 0

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

def get_available_remote_port(port_ignore):
    """
    get ports that are available
    """
    command = f"python3 check_port.py {port_ignore}"
    host = getenv("HOST_IP")
    user = getenv("HOST_USER")
    certificate = getenv("SSH_CERT_LOCATION")
    res = Connection(host=host, user=user,
                     connect_kwargs={"key_filename": certificate})
    res.put('test.py', f'/home/{user}/check_port.py')
    ret = res.run(command)
    ret = eval(ret.stdout)
    return ret


def filter_used_port(ports):
    """
    filter used port from list of port
    """
    used_port = []
    port_ignore = [22,80, 443,21,25,53,110,143,993,995,3306,5432,6379,8000,8080,8888, 5000]
    for port in ports:
        if port in port_ignore:
            used_port.append(port)
        if check_port(port):
            ports.append(port)
    return ports


def main():
    """
    """
    from models.ports import Ports
    #if "full check": #temp
    ports = get_available_remote_port([])
    #else

    try:
        # seed data bese
        print("%%", ports,type(ports))
        Ports.load_available_ports(ports)
    except Exception as e:
        print(e)
        print("error:............................")
        pass
    print("####### DONE.........................")
    return
if __name__ == "__main__":
    main()
