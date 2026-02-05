from seith_lib.utils import docker_utils

def run(args):
    container = docker_utils.get_container(args.container)
    if not container:
        print('container not found')
    else: 
        container.start()
        print('container started')

