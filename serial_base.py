#!/usr/bin/env python

class SerialBaseCmd(object):
    def __init__(self, name, help):
        self.name = name
        self.help = help

    def add_arguments(self, parser):
        parser.add_argument('device', nargs=1)

    def register(self, parser, list):
        list[self.name] = self
        parser = parser.add_parser(self.name, help=self.help)
        parser.set_defaults(func=self)
        self.add_arguments(parser)

class SerialBase(object):
	def __init__(self, device):
		self.device = device