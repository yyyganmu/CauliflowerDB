#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author: YANG Yuyao
# time: 2024/1/2
# check the line separator
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


from sshtunnel import open_tunnel
import paramiko


def get_ssh():
    server = open_tunnel(
        ('taascr.myddns.me', 7251),
        ssh_username='yyy',
        ssh_password='2020apr23',
        remote_bind_address=('127.0.0.1', 3306)
    )
    server.start()
    return str(server.local_bind_port)


def remote_command(command):
    server = paramiko.SSHClient()
    server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    server.connect(hostname='taascr.myddns.me', port=7251, username='yyy', password='2020apr23')
    stdin, stdout, stderr = server.exec_command(command=command, get_pty=True)
    results = stdout.read().decode('utf-8')
    return results