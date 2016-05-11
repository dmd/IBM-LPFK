#!/usr/bin/env python

import os
import sys
import serial
from time import sleep
import struct

PORT = os.getenv('LIGHTS_PORT', '/dev/serial/by-id/usb-Silicon_Labs_IBM-LPFK_75BB67F3-A9AA8F7A-if00-port0')


##### setup

sp = serial.Serial(port=PORT,
                   baudrate=9600,
                   bytesize=serial.EIGHTBITS,
                   parity=serial.PARITY_ODD,
                   stopbits=serial.STOPBITS_ONE,
                   xonxoff=False,
                   rtscts=False,
                   dsrdtr=False)

# reset
sp.timeout = 1
sp.read(1)
sp.timeout = 10
sp.write(b'\x01')
sleep(0.8)

# check ID
sp.write(b'\x06')
resp = sp.read(1)

if resp == b'\x03':
    print ("LPFK detected")
else:
    print ("uh oh, LPFK not detected")
    sys.exit(1)

# enable
sp.write(b'\x08')
sleep(0.1)

##### control

status = [0] * 32

def update_lights(status):
    sp.write(b'\x94')
    sp.write(struct.pack('BBBB',
                         int(''.join(str(k) for k in status[0:8]),2),
                         int(''.join(str(k) for k in status[8:16]),2),
                         int(''.join(str(k) for k in status[16:24]),2),
                         int(''.join(str(k) for k in status[24:32]),2)))
    resp = sp.read(1)
    if resp == b'\x80':
        print('error')
    elif resp == b'\x81':
        pass # print('good set')
    else:
        print('huh??')

while True:
    cmd = sp.read(1)
    if not len(cmd):
        next
    cmd = ord(cmd)
    if cmd == 0x80:
        print ('got error, resending')
        update_lights(status)
        next

    status[cmd] ^= 1
    print('button {} set to {}'.format(cmd, status[cmd]))
    update_lights(status)
    
sp.close()




