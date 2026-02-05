from seith_lib.utils import config_utils, metadata_utils, docker_utils

from config import SCRIPTS_DIR, DEST_SCRIPTS

def upgrade_deps(name):
    # read config
    conf_dir = config_utils.get_conf_dir(name)
    configs  = config_utils.parse_all_deps(conf_dir) 

    # read metadata
    a_metadata = metadata_utils.parse_metadata(name)

    # get container
    container = docker_utils.get_container(name)

    # copy scripts directory in docker 
    docker_utils.copy_folder_to_container(container, conf_dir+SCRIPTS_DIR, DEST_SCRIPTS)

    for conf in configs:
        is_deps_dict = isinstance(conf["deps"], dict)
        dep_name = conf["name"]
        if dep_name in a_metadata["installed_deps"]:
            to_upgrade = a_metadata["installed_deps"][dep_name] 
        else:
            to_upgrade = []

        if conf["unique_upgrade"] and not is_deps_dict:
            dep_list = conf["separator"].join(to_upgrade)
            command = conf["upgrade"].format(dep_list)
            e,o = docker_utils.exec_on_container(container, command)
        else:
            for dep in to_upgrade:
                if is_deps_dict:
                    attr = conf["deps"][dep]
                else:
                    attr = dep

                command = conf["install"].format(attr)
                docker_utils.exec_on_container(container, command)  #  change pos


def run(args):
    upgrade_deps(args.container)
