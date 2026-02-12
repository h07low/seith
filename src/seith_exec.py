#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import logging
import sys
from pathlib import Path

from seith_lib.commands import exec_parser, commands 
from seith_lib.completers import completers 

logger = logging.getLogger(__name__)

#TODO
def log():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')

def parse_args():
    container_name = Path(sys.argv[0]).stem

    exec = argparse.ArgumentParser(prog = container_name, description='i cant explain TODO', epilog='GoodBye TODO')
    exec_parser(exec, 'exec', commands['exec']['help'], commands['exec'].get('func', 'exec')) 
    exec.set_defaults(container=container_name)

    argcomplete.autocomplete(exec)
    args = exec.parse_args()

    return args

def main():
    args = parse_args()
    
    args.func(args)

if __name__=="__main__":
    main()
