#!/usr/bin/env python

from send_receive import SendReceiveCmd
from send_receive import SendReceive

import serial
from serial.threaded import LineReader
from serial.threaded import ReaderThread
import time
import threading

class SimpleSendReceiveCmd(SendReceiveCmd):

    def __init__(self):
        super(SimpleSendReceiveCmd, self).__init__('simple-send-receive',
            'Simple Send/Receive test')

    def add_arguments(self, parser):
        super(SimpleSendReceiveCmd, self).add_arguments(parser)

    def __call__(self, args):
        dict = vars(args)
        dict.pop('func', None)

        ser = serial.Serial(port=dict['devices'][0], baudrate=dict['baudrate'])

        with ReaderThread(ser, SimpleSendReceive) as test:
            if dict['type'] == SendReceiveCmd.CmdType.SENDER:
                test.send_pattern()
            elif dict['type'] == SendReceiveCmd.CmdType.RECEIVER:
                test.recv_pattern()
                if test.pattern_received.is_set() == 1:
                    print "Pattern Received"
                else:
                    print "Pattern NOT Received"                
            else:
                print "Loopback not supported"

class SimpleSendReceive(LineReader):

    def __init__(self):
        self.test_pattern="All your base are belong to us"
        self.pattern_received = threading.Event()
        super(SimpleSendReceive, self).__init__()

    def handle_line(self, data):
        if data == self.test_pattern:
            self.pattern_received.set()

    def send_pattern(self):
        self.write_line(self.test_pattern)

    def recv_pattern(self):
        self.pattern_received.wait(60)