#!/usr/bin/env python

class SerialBaseCmd:
    def __init__(self, name, help):
        self.name = name
        self.help = help

    def register(self, parser, list):
        list[self.name] = self
        parser = parser.add_parser(self.name, help=self.help)
        parser.set_defaults(func=self)
        self.add_arguments(parser)
        parser.add_argument('device', nargs=1)

class SerialBase:
	def __init__(self, device):
		self.device = device