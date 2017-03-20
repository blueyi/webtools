#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

import re
import glob


# match regex pattern for begin of line from file name list
# return dict, key is matched and value is match times
def match_begin_of_line(pattern, files):
    ip_dict = {}
    for arg in files:
        for file in glob.iglob(arg):
            for line in open(file, 'r'):
                match = re.match(pattern, line)
                if match:
                    ip = match.group(0)
                    if ip not in ip_dict:
                        ip_dict[ip] = 1
                    else:
                        ip_dict[ip] += 1
    return ip_dict
