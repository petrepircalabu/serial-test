#!/usr/bin/env python

import serial

class SerialBaseCmd(object):
    def __init__(self, name, help):
        self.name = name
        self.help = help

    def add_arguments(self, parser):
        parser.add_argument('-b', '--baudrate', type=int, default=115200,
            help='specify the baudrate')
        parser.add_argument('devices', nargs=1)

    def register(self, parser, list):
        list[self.name] = self
        parser = parser.add_parser(self.name, help=self.help)
        parser.set_defaults(func=self)
        self.add_arguments(parser)

class SerialBase(object):
    def __init__(self, *args, **kwargs):
        self.ser = []
        print kwargs
        for device in kwargs['devices']:
            self.ser.append(serial.Serial(port=device, baudrate=kwargs['baudrate']))

        print self.ser[0]

    def __call__(self):
        pass
