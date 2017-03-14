#!/usr/bin/env python

from serial_base import SerialBase
from serial_base import SerialBaseCmd

class WaitBreakCmd(SerialBaseCmd):

    def __init__(self):
        SerialBaseCmd.__init__(self, 'waitbreak',
            'waits for BREAK condition on the specified port')

    def add_arguments(self, parser):
        parser.add_argument('-d', '--duration', type=int, default=0,
            help='break duration')

    def __call__(self, args):
        WaitBreak(duration=args.duration, device=args.device)()

class WaitBreak(SerialBase):

    def __init__(self, duration, device):
        SerialBase.__init__(self, device)
        self.duration = duration

    def __call__(self):
        print "Execute WaitBreak duration = {} device = {}".format(
            self.duration, self.device)
