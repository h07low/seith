#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse
import logging

from seith_lib.commands import commands as seith_commands
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
    
    ## handle containers
    # create parser
    create = subparser.add_parser('create', help='create container')
    create.add_argument('--conf-dir', help='specify conf dir (default=XDG_CONFIG_HOME/seith/containers/<name>/config.json)') 
    create.add_argument('container', help='container name')
    create.set_defaults(func=seith_commands['create'])

    # info
    info = subparser.add_parser('info', help='get container info')
    info.add_argument('container', nargs='?', help='container name', default='').completer = completers.containers
    info.set_defaults(func=seith_commands['info'])
    
    # start
    start = subparser.add_parser('start', help='start container')
    start.add_argument('container', help='container name', default='').completer = completers.containers
    start.set_defaults(func=seith_commands['start'])
    
    # stop
    stop = subparser.add_parser('stop', help='stop container')
    stop.add_argument('container', help='container name', default='').completer = completers.containers
    stop.set_defaults(func=seith_commands['stop'])

    ## deps
    # sync deps
    sync = subparser.add_parser('sync_deps', help='install added deps')
    sync.add_argument('container', help='container to sync').completer = completers.containers
    sync.set_defaults(func=seith_commands["sync_deps"])

    # upgrade
    upgrade = subparser.add_parser('upgrade', help='upgade installed deps')
    upgrade.add_argument('container', help='container to upgrade').completer = completers.containers
    upgrade.set_defaults(func=seith_commands["upgrade"])


    
    # exec parser #TODO interactive mode
    exec = subparser.add_parser('exec', help='exec commands on container')
    exec.add_argument('--env', help='extra environment variable to pass to the command', default='{}')
    exec.add_argument('--shell', help='specify shell to use (default=bash)', default='bash')
    exec.add_argument('--cwd', help='specify directory to use (default=/seith_temp)', default=None)
    exec.add_argument('--user', help='specify user to use (default=root)', default='root')
    exec.add_argument('container', help='container where to run the command').completer = completers.containers
    exec.add_argument('command', nargs='*', help='command to execute').completer = completers.docker_command
    exec.set_defaults(func=seith_commands["exec"])

    argcomplete.autocomplete(parser)

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    
    args.func(args)

if __name__=="__main__":
    main()
