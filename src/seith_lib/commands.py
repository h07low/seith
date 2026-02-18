import argcomplete
import importlib
import argparse
from seith_lib.completers import completers 

def _lazy_load(command_name):
    """Lazy load and execute command"""
    def wrapper(args):
        module = importlib.import_module(f'seith_lib.command.{command_name}')
        return module.run(args)
    return wrapper




def exec_parser(parent_parser, name, help, func_name):
    if isinstance(parent_parser, argparse._SubParsersAction):
        parser = parent_parser.add_parser(name, help=help)
        parser.add_argument('container', help='container name', default='').completer = completers.containers
    else:
        parser = parent_parser

    parser.add_argument('--env', help='extra environment variable to pass to the command', default='{}')
    parser.add_argument('--encode', help='how to encode the command (auto, all, none) (default=auto)', default='auto')
    parser.add_argument('--shell', help='specify shell to use (default=bash)', default='bash')
    parser.add_argument('--cwd', help='specify directory to use (default=/seith_temp)', default=None)
    parser.add_argument('--user', help='specify user to use (default=root)', default='root')
    parser.add_argument('command', nargs='*', help='command to execute').completer = completers.docker_command
    parser.set_defaults(func=_lazy_load(func_name))
    return parser

def create_parser(parent_parser, name, help, func_name):
    if isinstance(parent_parser, argparse._SubParsersAction):
        parser = parent_parser.add_parser(name, help=help)
    else:
        parser = parent_parser

    parser.add_argument('container', help='container name', default='').completer = completers.containers
    parser.add_argument('--conf-dir', help='specify conf dir (default=XDG_CONFIG_HOME/seith/containers/<name>/config.json)') 
    parser.set_defaults(func=_lazy_load(func_name))
    return parser

def info_parser(parent_parser, name, help, func_name):
# subparser
    if isinstance(parent_parser, argparse._SubParsersAction):
        p = parent_parser.add_parser(name, help=help)

    # defined parser
    else:
        p = parent_parser

    p.add_argument('container', nargs="?", help='container name', default='').completer = completers.containers
    p.set_defaults(func=_lazy_load(func_name))
    return p


def container_parser(parent_parser, name, help, func_name):
    # subparser
    if isinstance(parent_parser, argparse._SubParsersAction):
        p = parent_parser.add_parser(name, help=help)

    # defined parser
    else:
        p = parent_parser

    p.add_argument('container', help='container name', default='').completer = completers.containers
    p.set_defaults(func=_lazy_load(func_name))
    return p


def add_all_parsers(subparser):
    for name, cmd in commands.items():
        cmd['parser'](subparser, name, cmd['help'], cmd.get('func', name)) 

commands = {
    'create':   {"parser":create_parser,    "help":"create container"},
    'info':     {"parser":info_parser,      "help":"get containers info"},
    'start':    {"parser":container_parser, "help":"start container"},
    'stop':     {"parser":container_parser, "help":"stop container"},
    'sync_deps':{"parser":container_parser, "help":"install added deps"},
    'upgrade':  {"parser":container_parser, "help":"upgade installed deps"},
    
    'exec':     {"parser":exec_parser,       "help":"exec commands on container"},
}
