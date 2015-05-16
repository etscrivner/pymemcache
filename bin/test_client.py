# -*- coding: utf-8 -*-
import socket


def create_socket(host, port):
    """Create a new socket.

    :param host: A host
    :type host: str or unicode
    :param port: A port
    :type port: int
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def run(host, port):
    socket = create_socket(host, port)
    command = "get eric\r\n"
    socket.send(command.encode('utf-8'))


if __name__ == '__main__':
    run('localhost', 9999)
