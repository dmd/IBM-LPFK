#!/usr/bin/env python

from lpfk import lpfk

def toggler():
    lp = lpfk()
    
    while True:
        cmd = lp.get()
        if not len(cmd):
            continue
        if cmd == lp.RETRANSMIT:
            print ('got error, resending')
            lp.update_lights()
            continue
        cmd = ord(cmd)

        lp.keys[cmd] ^= 1
        print('button {} set to {}'.format(cmd, lp.keys[cmd]))
        lp.update_lights()


if __name__ == '__main__':
    toggler()
