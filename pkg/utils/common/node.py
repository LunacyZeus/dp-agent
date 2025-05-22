# -*- coding: UTF-8 -*-
import os
import socket

path = "/proc/" + str(os.getpid()) + "/cgroup"


def get_node_id():
    node_id = socket.gethostname()  # 通过socket获取到主机名
    return node_id