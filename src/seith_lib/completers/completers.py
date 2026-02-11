from seith_lib.utils import metadata_utils, docker_utils
import sys

def containers(prefix, parsed_args, **kwargs):
    containers = metadata_utils.get_all_metadata().keys()
    return (c for c in containers if c.startswith(prefix))

def docker_command(prefix, parsed_args, **kwargs):
    container = getattr(parsed_args, 'container', None)
    commands  = getattr(parsed_args, 'command', None)
    if not container:
        return set()

    c = docker_utils.get_container(container)
    
    if not prefix:
        prefix = "''"
    e, o = docker_utils.exec_on_container(c, 'compgen -f '+prefix) 
    o = o.decode()
    o = o.split('\n')

    return set(o)
