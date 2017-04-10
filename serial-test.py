#!/usr/bin/env python

from simple_send_receive import SimpleSendReceiveCmd

import argparse
import logging
import sys

commands = {}
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(help='commands')

def register(cmd):
    cmd.register(subparser, commands)

def main():
    register(SimpleSendReceiveCmd())

    args = parser.parse_args();
    try:
    	args.func(args)
    except Exception as ex:
        logging.error('Command failed. {}'.format(type(ex).__name__, ex))
        raise
        sys.exit(-1)

if __name__ == "__main__":
    main()