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
    e1, dirs = docker_utils.exec_on_container(c, 'compgen -d '+prefix) 
    e2, files = docker_utils.exec_on_container(c, 'compgen -f '+prefix) 

    result = set()
    # Add directories with trailing slash
    for d in dirs.decode().split('\n'):
        if d:
            result.add(d + '/')
    # Add files without trailing slash
    for f in files.decode().split('\n'):
        if f and not any(f == d.rstrip('/') for d in result):
            result.add(f)

    return result  
