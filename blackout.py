#!/usr/bin/env python

from lpfk import lpfk
from random import sample

def wamole(moles):
    lp = lpfk()

    rowcolgroups = [[0,1,2,3], # rows
                    [4,5,6,7,8,9],
                    [10,11,12,13,14,15],
                    [16,17,18,19,20,21],
                    [22,23,24,25,26,27],
                    [28,29,30,31],
                    [4,10,16,22], # cols
                    [0,5,11,17,23,28],
                    [1,6,12,18,24,29],
                    [2,7,13,19,25,30],
                    [3,8,14,20,26,31],
                    [9,15,21,27]]

    lp.update_lights()
    
    while True:
        cmd = lp.get()
        if not len(cmd):
            continue
        if cmd == lp.RETRANSMIT:
            print ('got error, resending')
            update_lights()
            continue
        cmd = ord(cmd)
        if lp.quitcheck(cmd):
            break

        # reverse the row and column of the hit key
        for group in rowcolgroups:
            if cmd in group:
                for light in group:
                    lp.keys[light] ^= 1

        # oops, we flipped the key itself twice, undo
        lp.keys[cmd] ^=1
        lp.update_lights()


if __name__ == '__main__':
    wamole(4)
