#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

"""

"""
import sys
from common import extract_ip, ip_to_local

reload(sys).setdefaultencoding("UTF-8")

count = int(sys.argv[1])
files = sys.argv[2:]
# files = ['access.log']


if __name__ == '__main__':
    for ip in extract_ip(files):
        if ip[1] > count:
            print(ip[0] + ': ' + str(ip[1]) + ' ' + ip_to_local(ip[0]))
