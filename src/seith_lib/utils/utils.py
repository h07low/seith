from pathlib import Path

from seith_lib.utils import metadata_utils


def translate_cwd(container):
    metadata = metadata_utils.parse_metadata(container)
    volumes = metadata["volumes"].keys()
    current_path = Path().absolute()
    with open("/tmp/debug_seith", "a" ) as f:
        f.write(current_path.as_posix())
    cwd = None
    for src_dir in volumes:
        if current_path.as_posix().startswith(src_dir):
            cwd = current_path.as_posix().replace(src_dir, metadata["volumes"][src_dir], 1)
            break
    with open("/tmp/debug_seith", "a" ) as f:
        f.write('\n'+str(cwd)+'\n')
    return cwd

