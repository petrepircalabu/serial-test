#!/usr/bin/env python

import serial

class SerialBaseCmd(object):
    def __init__(self, name, help):
        self.name = name
        self.help = help

    def add_arguments(self, parser):
        parser.add_argument('devices', nargs=1)

    def register(self, parser, list):
        list[self.name] = self
        parser = parser.add_parser(self.name, help=self.help)
        parser.set_defaults(func=self)
        self.add_arguments(parser)

class SerialBase(object):
    def __init__(self, device):
        self._device = device
        self._ser = None

    def __call__(self):
        try:
            self.set_up()
            self.run()
        except:
            print "Unexpected error:", sys.exc_info()[0]
        finally:
            self.tear_down()

    def set_up(self):
        # Open the port
        self._ser = serial.Serial()

    def tear_down(self):
        pass

    def run(self):
        pass