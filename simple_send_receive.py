#!/usr/bin/env python

from send_receive import SendReceiveCmd
from send_receive import SendReceive

class SimpleSendReceiveCmd(SendReceiveCmd):

    def __init__(self):
        super(SimpleSendReceiveCmd, self).__init__('simple-send-receive',
            'Simple Send/Receive test')

    def add_arguments(self, parser):
        super(SimpleSendReceiveCmd, self).add_arguments(parser)

    def __call__(self, args):
        dict = vars(args)
        dict.pop('func', None)
        SimpleSendReceive(*dict.values(), **dict)

class SimpleSendReceive(SendReceive):

    def __init__(self, *args, **kwargs):
        super(SimpleSendReceive, self).__init__(*args, **kwargs)