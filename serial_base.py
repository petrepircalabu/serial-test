#!/usr/bin/env python

import serial
import argparse

class ParityAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(ParityAction, self).__init__(option_strings, dest, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        for k, v in serial.PARITY_NAMES.items():
            if v == values:
                setattr(namespace, self.dest, k)
                break

class SerialBaseCmd(object):

    def __init__(self, name, help):
        self.name = name
        self.help = help

    def add_arguments(self, parser):
        parser.add_argument('-b', '--baudrate', type=int, default=115200,
            help='specify the baudrate')
        parser.add_argument('-p', '--parity', choices = serial.PARITY_NAMES.values(),
            default=serial.PARITY_NONE, action=ParityAction, help='specify the parity')
        parser.add_argument('--stop-bits', type=float,
            choices = [serial.STOPBITS_ONE,  serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO],
            default=serial.STOPBITS_ONE, help='specify the number of stop bits')
        parser.add_argument('--bytesize', type=int,
            choices = [serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS],
            default=serial.EIGHTBITS, help='specify the number of bits')
        parser.add_argument('-t', '--timeout', type=int, default=60,
            help='specify the commmand timeout')
        parser.add_argument('devices', nargs=1)

    def register(self, parser, list):
        list[self.name] = self
        parser = parser.add_parser(self.name, help=self.help)
        parser.set_defaults(func=self)
        self.add_arguments(parser)
