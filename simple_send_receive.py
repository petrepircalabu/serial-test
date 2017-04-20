#!/usr/bin/env python

from serial_base import Serial
from send_receive import SendReceiveCmd

from serial.threaded import LineReader
from serial.threaded import ReaderThread
import time
import threading

class SimpleSendReceiveCmd(SendReceiveCmd):

    def __init__(self,
            name = 'simple-send-receive',
            help = 'Simple Send/Receive test'):
        super(SimpleSendReceiveCmd, self).__init__(name, help)
        self.protocol_factory = SimpleSendReceive

    def add_arguments(self, parser):
        parser.add_argument('--delay-exec', type=int, default=0,
            help='delay execution with <param> seconds')
        super(SimpleSendReceiveCmd, self).add_arguments(parser)

    def prepare(self, test, dict):
        test.timeout = dict['timeout']

    def __call__(self, args):
        dict = vars(args)
        dict.pop('func', None)

        ser = Serial(port=dict['devices'][0], baudrate=dict['baudrate'],
            parity=dict['parity'], bytesize=dict['bytesize'],
            stopbits=dict['stop_bits'], rtscts=dict['rtscts'],
            xonxoff=dict['xonxoff'])

        time.sleep(dict['delay_exec'])

        with ReaderThread(ser, self.protocol_factory) as test:
            self.prepare(test, dict)

            command_map = {
                SendReceiveCmd.CmdType.SENDER   : test.sender,
                SendReceiveCmd.CmdType.RECEIVER : test.receiver,
                SendReceiveCmd.CmdType.LOOPBACK : test.loopback,
            }

            command_map[dict['type']]()

class SimpleSendReceive(LineReader):
    def __init__(self):
        self.test_pattern="All your base are belong to us"
        self.pattern_received = threading.Event()
        self.timeout = 60
        super(SimpleSendReceive, self).__init__()

    def handle_line(self, data):
        if data == self.test_pattern:
            self.pattern_received.set()

    def sender(self):
        self.write_line(self.test_pattern)

    def receiver(self):
        self.pattern_received.wait(self.timeout)
        if not self.pattern_received.is_set():
            raise ValueError('Timeout while receiving test pattern')

    def loopback(self):
        self.transport.serial.loopback = True
        self.sender()
        self.receiver()
        self.transport.serial.loopback = False
