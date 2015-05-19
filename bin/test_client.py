# -*- coding: utf-8 -*-
import fcntl
import os
import socket

from pymemcache import server


def create_socket(host, port):
    """Create a new socket.

    :param host: A host
    :type host: str or unicode
    :param port: A port
    :type port: int
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))
    return sock


def run(host, port):
    channel = create_socket(host, port)
    command = "get eric\r\n"
    server.spit_connection(channel, command.encode('utf-8'))
    print("Sent")
    print(server.slurp_connection(channel))
    channel.close()


if __name__ == '__main__':
    run('localhost', 9999)
