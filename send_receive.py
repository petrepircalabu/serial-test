#!/usr/bin/env python

from serial_base import SerialBaseCmd
from serial_base import SerialBase

class SendReceiveCmd(SerialBaseCmd):

    class CmdType:
        SENDER = 1
        RECEIVER = 2
        LOOPBACK = 3

    def __init__(self, name, help):
        super(SendReceiveCmd, self).__init__(name, help)

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-s', '--sender', dest='type', action='store_const',
            const = SendReceiveCmd.CmdType.SENDER)
        group.add_argument('-r', '--receiver', dest='type', action='store_const',
            const = SendReceiveCmd.CmdType.RECEIVER)
        group.add_argument('-l', '--loopback', dest='type', action='store_const',
            const = SendReceiveCmd.CmdType.LOOPBACK)
        super(SendReceiveCmd, self).add_arguments(parser)        

class SendReceive(SerialBase):

    def __init__(self, *args, **kwargs):
        super(SendReceive, self).__init__(*args, **kwargs)

    def __call__(self):
        print "SendReceive::execute"
