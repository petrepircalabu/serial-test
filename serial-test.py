#!/usr/bin/env python

from simple_send_receive import SimpleSendReceiveCmd

import argparse

commands = {}
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help='commands')

def register(cmd):
    cmd.register(subparser, commands)

def main():
    register(SimpleSendReceiveCmd())

    args = parser.parse_args();
    args.func(args)

if __name__ == "__main__":
    main()