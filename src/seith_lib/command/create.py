import docker
import json
from pathlib import Path
import shlex

import tarfile
import io


from seith_lib.utils import docker_utils, metadata_utils, config_utils 

client = docker.from_env()

def create(args):
    c = docker_utils.get_container(args.container)
    if c:
        print('container already exists, remove it or change name\n')
        exit()  # TODO MANAGE BETTER
    
    # get conf
    if args.conf_dir:
        conf_dir = args.conf_dir
        conf = config_utils.parse_config(conf_dir)
    else:
        conf_dir = config_utils.get_conf_dir(args.container)
        conf = config_utils.parse_config(conf_dir)
    
    image_name = conf["image"]
    docker_utils.pull_image(image_name)

    # create container
    container = client.containers.create(
            image = conf["image"],
            command = conf["command"],
            cap_add = conf["cap_add"],
            cap_drop = conf["cap_del"],
            network_mode = conf["network"],
            ports = conf["ports"],
            privileged = conf["privileged"],
            volumes = conf["volumes"],
            name =  args.container,
            detach = True
            )
    
    #TODO install deps

    # write metadata
    ## parse volumes
    volumes = {}
    for src_dir, value in conf["volumes"].items():
        volumes[src_dir] = value["bind"] 

    metadata_utils.add_entry(args.container, conf_dir, {}, volumes)

def run(args):
    create(args)
    print('it is suggested to run the following command (if you have installed the tool using pipx)')
    print(f"cp /home/sigpwn/.local/bin/seith_exec /home/sigpwn/.local/bin/{args.container} && sed -i '1a # PYTHON_ARGCOMPLETE_OK' /home/sigpwn/.local/bin/{args.container}")
    print()


def add_dep(name, conf_dir):
    pass

def backup(name, conf_dir):
    pass #TODO EXTRA

# create("test1", "./config_example")

# start("test1")
# sync_deps("test1", "./config_example")
# upgrade_deps("test1", "./config_example")
