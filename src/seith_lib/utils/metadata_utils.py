from pathlib import Path
import json

import seith_lib.utils.paths as seith_paths

'''
metadata structure example
{
    "container_name":{
        "conf_dir": "/asdf..",
        "installed_deps":{
            "APT":["vim", "nano"],
            "PIPX":["impacket"]
        },
        
        "volumes":{
            "/home/out_user":"/container_dir"
        }
    }
}
'''

def get_all_metadata():
    if Path(seith_paths.metadata).exists():
        with open(seith_paths.metadata) as f:
            metadata = json.load(f)
    else:
        metadata = dict() 
    return metadata


def parse_metadata(name):
    if Path(seith_paths.metadata).exists():
        with open(seith_paths.metadata) as f:
            metadata = json.load(f)
    else:
        metadata = dict() 
    
    if name in metadata:
        a_metadata = metadata[name]
    else:
        a_metadata = {"conf_dir":"", "installed_deps":{},"volumes":{}} 
    
    return a_metadata

def add_entry(name, conf_dir, installed_deps={}, volumes={}):
    entry = {"conf_dir": conf_dir,
             "installed_deps": installed_deps,
             "volumes": volumes}

    write_metadata(name, entry)

def write_metadata(name, new_meta):
    '''
    overwrite the metadata entry name with the given metadata
    '''
    if Path(seith_paths.metadata).exists():
        with open(seith_paths.metadata) as f:
            metadata = json.load(f)
    else:
        metadata = dict() 

    metadata[name] = new_meta
    with open(seith_paths.metadata, "w") as f:
        json.dump(metadata, f)


