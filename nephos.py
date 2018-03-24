#!/usr/bin/env python3

from actions.upload import UploadHandler
# from actions.search import SearchHandler

ActionsHandler = [
    UploadHandler('upload'),
    # SearchHandler('search'),
]


import argparse

parser = argparse.ArgumentParser(prog='nephos.py')
parser.add_argument('--foo', action='store_true', help='foo help')


subparser = parser.add_subparsers(dest='subc')

for handler in ActionsHandler:
    handler._init_args(subparser)

args = parser.parse_args()

if args.subc is None:
    parser.print_help()
    exit(0)

h = list(filter(lambda x: x.subcommand == args.subc, ActionsHandler))[0]
h.run(args)
