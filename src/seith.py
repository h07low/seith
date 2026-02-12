#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import logging

from seith_lib.commands import add_all_parsers 
from seith_lib.completers import completers 

logger = logging.getLogger(__name__)

#TODO
def log():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')

def parse_args():
    '''
    seith create/add 
    seith remove
    seith start?
    seith stop?
    seith exec 

    # deps
    seith sync_deps  #TODO cache installed
    seith upgrade
    seith add_dep
    seith del_dep?

    # handle
    seith info
    seith stop
    seith start

    # TODObackup
    seith backup?
    seith restore
    '''
    parser = argparse.ArgumentParser(prog = 'seith', description='i cant explain TODO', epilog='GoodBye TODO')

    subparser = parser.add_subparsers(help='actions', required=True)

    add_all_parsers(subparser)
    
    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    
    args.func(args)

if __name__=="__main__":
    main()
