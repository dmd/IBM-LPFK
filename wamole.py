#!/usr/bin/env python

from lpfk import lpfk
from random import sample

def wamole(moles):
    lp = lpfk()

    # starting pattern
    for k in sample(range(32), moles):
        lp.keys[k] = 1
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

        if lp.keys[cmd] == 0:
            # do nothing if we whacked a non-existent mole
            continue

        # choose a new light that isn't on
        choices = sample(range(32), moles + 2)
        for k in choices:
            if lp.keys[k] == 0:
                lp.keys[k] = 1
                break

        # and whack the current mole
        lp.keys[cmd] = 0

        lp.update_lights()


if __name__ == '__main__':
    wamole(4)
