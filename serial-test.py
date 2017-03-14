#!/usr/bin/env python

from sendbreak import SendBreakCmd
from waitbreak import WaitBreakCmd

import argparse

commands = {}
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help='commands')

def register(cmd):
    cmd.register(subparser, commands)

def main():
    register(SendBreakCmd())
    register(WaitBreakCmd())

    args = parser.parse_args();
    args.func(args)

if __name__ == "__main__":
    main()