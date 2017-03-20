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
from common import match_begin_of_line

files = sys.argv[1:]
# files = ['access.log']


# return ip list and times in files
def extract_ip(files):
    pattern = '(\d+\.){3}(\d+)'
    ip_dic = match_begin_of_line(pattern, files)
    return sorted(ip_dic.iteritems(), key=lambda d: d[1], reverse=True)


for ip in extract_ip(files):
    if ip[1] > 10:
        print(ip[0] + ': ' + str(ip[1]))
