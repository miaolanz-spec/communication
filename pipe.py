# coding: utf-8

from __future__ import print_function

import math
import os
import sys


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0 / (2 * k + 1) / (2 * k + 1)
    return s


def pi(n):
    childs = {}
    unit = n / 10
    for i in range(10):  # 10 child processes 
        mink = unit * i
        maxk = mink + unit
        r, w = os.pipe()
        pid = os.fork()
        if pid > 0:
            childs[pid] = r  
            os.close(w)  # close w of parent process.  
        else:
            os.close(r)  # close r 
            s = slice(mink, maxk)  # sub-process start 
            os.write(w, str(s))
            os.close(w)  # close w 
            sys.exit(0)  # end  
    sums = []

    for pid, r in childs.items():
        sums.append(float(os.read(r, 1024)))
        os.close(r)  # close r 
        os.waitpid(pid, 0)  # wait 
    return math.sqrt(sum(sums) * 8)


print(pi(10000000))
