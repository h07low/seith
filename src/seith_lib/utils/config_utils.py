import json
from pathlib import Path

from seith_lib.utils import metadata_utils
from seith_lib.utils import paths as seith_paths 

from seith_lib.command.default_conf_values import DEFAULT_CONF_DICT
from config import DEPS_DIR, CONF_FILE_NAME

def parse_all_deps(conf_dir):
    configs = []
    for conf_file in Path(conf_dir+DEPS_DIR).glob("*.json"):
        with open(conf_file) as f:
            j = json.load(f)
            if isinstance(j, list):
                configs+=j
            else:
                configs.append(j)
    
    # order by priority 
    configs.sort(key=lambda x: x.get("priority", 100))
    return configs

def parse_config(conf_dir):
    #TODO err manag
    with open(conf_dir+CONF_FILE_NAME) as f:
        conf = json.load(f)
    
    conf = DEFAULT_CONF_DICT | conf

    return conf

def get_conf_dir(name):
    meta = metadata_utils.parse_metadata(name)
    if meta["conf_dir"]:
        return meta["conf_dir"]
    else:
        return seith_paths.config_home + '/' + name  
