#!/usr/bin/env python

import os
import sys
import serial
from time import sleep
import struct


class lpfk:
    PORT = os.getenv('LIGHTS_PORT', '/dev/serial/by-id/usb-Silicon_Labs_IBM-LPFK_75BB67F3-A9AA8F7A-if00-port0')

    RESET = b'\x01'
    READCONF = b'\x06'
    CONFOK = b'\x03'
    ENABLE = b'\x08'
    SET = b'\x94'
    RETRANSMIT = b'\x80'
    OK = b'\x81'

    def __init__(self):
        self.keys = [0] * 32
        self.sp = serial.Serial(port=self.PORT,
                           baudrate=9600,
                           bytesize=serial.EIGHTBITS,
                           parity=serial.PARITY_ODD,
                           stopbits=serial.STOPBITS_ONE,
                           xonxoff=False,
                           rtscts=False,
                           dsrdtr=False)

        # reset
        self.sp.timeout = 1
        self.get()
        self.sp.timeout = 10
        self.sp.write(self.RESET)
        sleep(0.8)

        # check ID
        self.sp.write(self.READCONF)

        if self.get() == self.CONFOK:
            print ("LPFK detected")
        else:
            print ("uh oh, LPFK not detected")
            self.sp.close()
            sys.exit(1)

        # enable
        self.sp.write(b'\x08')
        sleep(0.1)


    def update_lights(self, retries=0):
        self.sp.write(self.SET)
        self.sp.write(struct.pack('BBBB',
                             int(''.join(str(k) for k in self.keys[0:8]),2),
                             int(''.join(str(k) for k in self.keys[8:16]),2),
                             int(''.join(str(k) for k in self.keys[16:24]),2),
                             int(''.join(str(k) for k in self.keys[24:32]),2)))
        resp = self.get()
        if resp == b'\x80':
            print('error, retry')
            if retries > 2:
                print('{} retries and still failing so aborting'.format(retries))
                sys.exit(1)
            else:
                self.update_lights(retries+1)
        elif resp == b'\x81':
            pass # print('good set')
        else:
            print('huh??')

    def get(self):
        return self.sp.read(1)

    def close(self):
        self.sp.close()

    
