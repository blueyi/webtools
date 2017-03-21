#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 ubuntu <ubuntu@dev>
#
# Distributed under terms of the MIT license.

"""
batch block or allow ip from ufw
"""

import sys
import os
import subprocess
import glob


# is run by root
def runAsRoot():
    if os.geteuid() != 0:
        print('Please run the script by "root"!')
        sys.exit(1)

runAsRoot()

if len(sys.argv) < 3:
    print('You must specify "deny" or allow and a list of ip in file')
    sys.exit('bye')

choice = sys.argv[1]
ufw = 'ufw'
files = sys.argv[2:]


def ufw_batch_ip(cmd, files):
    count = 0
    for arg in files:
        for file in glob.iglob(arg):
            for line in open(file, 'r'):
                tcmd = ' '.join(cmd) + ' ' + line.strip('\n')
                print(tcmd)
                subprocess.call(tcmd, shell=True)
                count += 1
    return count

cmd = [ufw, choice, 'from']

if __name__ == '__main__':
    cnt = ufw_batch_ip(cmd, files)
    print(str(cnt) + ' ip ' + choice)
