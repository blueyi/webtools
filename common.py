#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

import re
import os
import glob
import requests


# match regex pattern for begin of line from file name list
# return dict, key is matched and value is match times
def match_begin_of_line(pattern, files):
    rep = re.compile(pattern)
    key_dict = {}
    for arg in files:
        for file in glob.iglob(arg):
            for line in open(file, 'r'):
                match = re.match(rep, line)
                if match:
                    key = match.group(0)
                    if key not in key_dict:
                        key_dict[key] = 1
                    else:
                        key_dict[key] += 1
    return key_dict


# is tlist has anything string in tstr
def is_list_in_str(tlist, tstr):
    for item in tlist:
        if item in tstr:
            return True
    return False


# like fuzzy search
# search regex patten with key_list and fixed_words from files
# each line must contain fixed_words and one of the word from key_list
def two_key_match(pattern, keys, files):
    rep = re.compile(pattern)
    key_list = keys.split()
    res_line = []
    for arg in files:
        for file in glob.iglob(arg):
            for line in open(file, 'r'):
                if re.search(rep, line) and is_list_in_str(key_list, line):
                    res_line.append(line)
    return res_line


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

