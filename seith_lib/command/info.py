from seith_lib.utils import metadata_utils, docker_utils

import json

#TODO colors
def run(args):
    if args.container:
        meta = metadata_utils.parse_metadata(args.container) 
        get_info(args.container, meta)
    else:
        get_all_info()

def get_all_info():
    meta = metadata_utils.get_all_metadata()
    for name, c_meta in meta.items():
        print(name)
        get_info(name, c_meta)


def get_info(name, meta):
    c = docker_utils.get_container(name)
    if c:
        print('container is: {}'.format(c.status))
    else:
        print('container does not exists')

    print('saved metadata')
    print(json.dumps(meta,indent=4) )


