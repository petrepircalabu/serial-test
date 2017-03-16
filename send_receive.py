#!/usr/bin/env python

from serial_base import SerialBaseCmd
from serial_base import SerialBase

class SendReceiveCmd(SerialBaseCmd):

    def __init__(self, name, help):
        super(SendReceiveCmd, self).__init__(name, help)

    def add_arguments(self, parser):
        super(SendReceiveCmd, self).add_arguments(parser)        
