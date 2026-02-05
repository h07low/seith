from seith_lib.utils import config_utils, docker_utils, metadata_utils
from config import SCRIPTS_DIR, DEST_SCRIPTS #TODO maybe change

#TODO print
def sync_deps(args):
    name = args.container

    # read configs
    conf_dir = config_utils.get_conf_dir(name)
    configs  = config_utils.parse_all_deps(conf_dir) 

    # get container
    container = docker_utils.get_container(name)
    # check running?

    # copy scripts directory in docker 
    docker_utils.copy_folder_to_container(container, conf_dir+SCRIPTS_DIR, DEST_SCRIPTS)

    # read metadata   
    a_metadata = metadata_utils.parse_metadata(name)

    # install missings
    for conf in configs:
        is_deps_dict = isinstance(conf["deps"], dict)
        dep_name = conf["name"]
        if dep_name in a_metadata["installed_deps"]:
            if is_deps_dict:
                to_install = set(conf["deps"].keys()) - set(a_metadata["installed_deps"][dep_name])
            else:
                to_install = set(conf["deps"]) - set(a_metadata["installed_deps"][dep_name])
        else:
            a_metadata["installed_deps"][dep_name]=[]
            if is_deps_dict:
                to_install = conf["deps"].keys()
            else:
                to_install = conf["deps"]


        if conf["unique_install"] and not is_deps_dict:
            dep_list = conf["separator"].join(to_install)
            command = conf["install"].format(dep_list)
            docker_utils.exec_on_container(container, command, True)
        else:
            for dep in to_install:
                if is_deps_dict:
                    attr = conf["deps"][dep]
                else:
                    attr = dep

                command = conf["install"].format(attr)
                docker_utils.exec_on_container(container, command, True)  #  change pos

        a_metadata["installed_deps"][dep_name]+=to_install
    
    # save metadata  
    metadata_utils.write_metadata(name, a_metadata)

def run(args):
    sync_deps(args)
