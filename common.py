#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

import re
import glob
import requests


# match regex pattern for begin of line from file name list
# return dict, key is matched and value is match times
def match_begin_of_line(pattern, files):
    key_dict = {}
    for arg in files:
        for file in glob.iglob(arg):
            for line in open(file, 'r'):
                match = re.match(pattern, line)
                if match:
                    key = match.group(0)
                    if key not in key_dict:
                        key_dict[key] = 1
                    else:
                        key_dict[key] += 1
    return key_dict


# return ip list and times in files and order by times
def extract_ip(files):
    pattern = '(\d+\.){3}(\d+)'
    ip_dic = match_begin_of_line(pattern, files)
    return sorted(ip_dic.iteritems(), key=lambda d: d[1], reverse=True)


def ip_to_local(ip):
    r = requests.get('http://www.ip138.com/ips138.asp?ip=' + ip)
    context = r.content
    match = re.search('class="ul1".+\<\/li\>', context)
    tloc = match.group(0).decode('gbk')
    loc = tloc[tloc.find('<li>')+9: tloc.find('</li>')]
    return loc
