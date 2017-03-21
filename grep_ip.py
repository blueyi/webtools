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
import os
from common import two_key_match

if len(sys.argv) < 3:
    print('At least keys_file and input file as input')
    sys.exit('bye')

pattern = ''
if os.path.isfile(sys.argv[1]):
    pattern = open(sys.argv[1]).readline().strip('\n')
key_file = sys.argv[2]
files = sys.argv[3:]


def grep_ip(pattern, key_file, files):
    keys = ''
    for line in open(key_file, 'r'):
        keys = keys + ' ' + line.strip('\n')
    for line in two_key_match(pattern, keys, files):
        print(line)

if __name__ == '__main__':
    grep_ip(pattern, key_file, files)
