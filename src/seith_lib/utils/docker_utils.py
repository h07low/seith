from pathlib import Path 
import docker

import shlex
import tarfile
import io

from config import DEST_SCRIPTS


client = docker.from_env()


def get_container(name):
    try:
        container = client.containers.get(name)
    except docker.errors.NotFound:
        # print("container not found")
        container = None 

    return container

def exec_on_container(container, command, output=False):
    bash_command = "bash -c {}".format(shlex.quote(command))  # TODO custom shell other than bash

    exec_instance = client.api.exec_create(
        container.id,
        bash_command,
        workdir=DEST_SCRIPTS,
        privileged=True,
        tty=False,
        user='root' 
    )

    exec_output = client.api.exec_start(
        exec_instance['Id'],
        tty=False,
        stream=output,
    )
    
    for o in exec_output:
        print(o.decode(), end='')

    exec_inspect = client.api.exec_inspect(exec_instance['Id'])
    exit_code = exec_inspect['ExitCode']
    return exit_code


def copy_folder_to_container(container, src_path, dest_path):
    """
    Copy a folder into a Docker container
    
    Args:
        container: Docker container object
        src_path: Local folder path (str or Path)
        dest_path: Destination path in container (str)
    """
    src_path = Path(src_path)
    
    # Create tar archive in memory
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        # Add folder to tar
        tar.add(src_path, arcname=src_path.name)
    
    # Reset stream position
    tar_stream.seek(0)
    
    container.exec_run(f"mkdir -p {dest_path}")

    # Put archive in container
    container.put_archive(dest_path, tar_stream)

def pull_image(image):
    #TODO handle image not found
    try:
        client.images.get(image)
        print(f"✓ Image '{image}' already present")
    except docker.errors.ImageNotFound:
        print(f"Pulling image '{image}'...")
        client.images.pull(image)
        print(f"✓ Image pulled successfully")

