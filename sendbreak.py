#!/usr/bin/env python

from serial_base import SerialBase
from serial_base import SerialBaseCmd

class SendBreakCmd(SerialBaseCmd):

    def __init__(self):
        SerialBaseCmd.__init__(self, 'sendbreak', 'send BREAK to the specified port')

    def add_arguments(self, parser):
        parser.add_argument('-d', '--duration', type=int, default=0,
            help='break duration')

    def __call__(self, args):
        SendBreak(duration=args.duration, device=args.device)()

class SendBreak(SerialBase):

    def __init__(self, duration, device):
        SerialBase.__init__(self, device)
        self.duration = duration

    def __call__(self):
        print "Execute SendBreak duration = {} device = {}".format(
            self.duration, self.device)
