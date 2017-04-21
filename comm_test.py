#!/usr/bin/env python

from serial_base import Serial
from simple_send_receive import SimpleSendReceiveCmd

from serial.threaded import LineReader
from serial.threaded import ReaderThread
import time
import threading
import serial

class CommInhibitTest(LineReader):
    def __init__(self):
        self.cmd1 = "CMD1"
        self.cmd2 = "CMD2"
        self.cmd3 = "CMD3"
        self.resp_ok = "OKAY"
        self.resp_tout = "TOUT"
        self.pattern_received = threading.Event()
        self.timeout = 60
        super(CommInhibitTest, self).__init__()

    def inhibit(self):
        pass

    def handle_line(self, data):
        if data == self.expected:
            self.pattern_received.set()

    def sender(self):
        # send command 1
        self.write_line(self.cmd1)

        # wait response 1
        self.expected = self.resp_ok
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if not self.pattern_received.is_set():
            raise ValueError('Timeout')

        # send command 2
        self.write_line(self.cmd2)

        # wait response 2
        self.expected = self.resp_tout
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if self.pattern_received.is_set():
            raise ValueError('Data received')

        # send command 2
        self.write_line(self.cmd3)

        # wait response 2
        self.expected = self.resp_ok
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if not self.pattern_received.is_set():
            raise ValueError('Timeout')

    def receiver(self):
        # wait command 1
        self.expected = self.cmd1
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if not self.pattern_received.is_set():
            raise ValueError('Timeout')

        # inhibit communication
        self.inhibit(True)

        # send response 1
        self.write_line(self.resp_ok)

        # wait command 2 (timeout expected)
        self.expected = self.cmd2
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if self.pattern_received.is_set():
            self.write_line(self.resp_tout)
            raise ValueError('Data received')

        # restore communication
        self.inhibit(False)

        # wait command 3
        self.expected = self.cmd3
        self.pattern_received.clear()
        self.pattern_received.wait(self.timeout)
        if not self.pattern_received.is_set():
            raise ValueError('Timeout')

        # send response 3
        self.write_line(self.resp_ok)

    def loopback(self):
        raise ValueError("Loopback mode not allowed")


class CreadTestCmd(SimpleSendReceiveCmd):
    def __init__ (self,
            name = 'cread',
            help = 'Test if the driver allows input to be received'):
        super(CreadTestCmd, self).__init__(name, help)
        self.protocol_factory = CreadTest

    def prepare(self, test, dict):
        super(CreadTestCmd, self).prepare(test, dict)

class CreadTest(CommInhibitTest):
    def __init__(self):
        super(CreadTest, self).__init__()

    def inhibit(self, value):
        self.transport.serial.cread = not value
