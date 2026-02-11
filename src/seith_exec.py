#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import logging
import sys
from pathlib import Path

from seith_lib.commands import commands as seith_commands
from seith_lib.completers import completers 

logger = logging.getLogger(__name__)

#TODO
def log():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')

def parse_args():
    container_name = Path(sys.argv[0]).stem
    # exec parser #TODO interactive mode
    # TODO common function
    exec = argparse.ArgumentParser(prog = container_name, description='i cant explain TODO', epilog='GoodBye TODO')
    exec.add_argument('--env', help='extra environment variable to pass to the command', default='{}')
    exec.add_argument('--shell', help='specify shell to use (default=bash)', default='bash')
    exec.add_argument('--cwd', help='specify directory to use (default=/seith_temp)', default=None)
    exec.add_argument('--user', help='specify user to use (default=root)', default='root')
    exec.add_argument('command', nargs='*', help='command to execute').completer = completers.docker_command
    exec.set_defaults(func=seith_commands["exec"])
    exec.set_defaults(container=container_name)
    
    #TODO eval "$(register-python-argcomplete blockchain)"
    #TODO ln -s ~/.local/bin/seith_exec ~/.local/bin/blockchain

    argcomplete.autocomplete(exec)

    args = exec.parse_args()

    return args

def main():
    args = parse_args()
    
    args.func(args)

if __name__=="__main__":
    main()
