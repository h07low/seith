# seith_lib/commands.py
import importlib

def _lazy_load(command_name):
    """Lazy load and execute command"""
    def wrapper(args):
        module = importlib.import_module(f'seith_lib.command.{command_name}')
        return module.run(args)
    return wrapper

commands = {
    "exec": _lazy_load("exec"),
    "sync_deps": _lazy_load("sync_deps"),
    "create": _lazy_load("create"),
    "start": _lazy_load("start"),
    "stop": _lazy_load("stop"),
    "info": _lazy_load("info"),
    "upgrade": _lazy_load("upgrade"),
}

