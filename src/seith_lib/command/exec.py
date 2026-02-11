import json
import shlex
import termios, tty, sys, select, os   # needed for tty 
from pathlib import Path

from seith_lib.utils import docker_utils
from seith_lib.utils import metadata_utils


def exec_on_container(container, command):
    bash_command = "bash -c {}".format(shlex.quote(command))  # TODO custom shell other than bash

    return container.exec_run(bash_command,
                       stdout=True,
                       stderr=True,
                       stdin=False,
                       tty=True,
                       workdir=DEST_SCRIPTS
                       )

def run(args):
    '''
    args:
        container
        env
        shell
        cwd
        command
    '''
    command = "{0} -lc {1}".format(args.shell, shlex.quote(" ".join(args.command)))

    
    container = docker_utils.get_container(args.container)
    if container.status != 'running':
        print(container.status)
        print('container not running')
        exit() #TODO manage

    # TODO calculate CWD
    cwd = args.cwd
    if not cwd:
        metadata = metadata_utils.parse_metadata(args.container)
        volumes = metadata["volumes"].keys()
        current_path = Path().absolute()
        for src_dir in volumes:
            if current_path.as_posix().startswith(src_dir):
                cwd = current_path.as_posix().replace(src_dir, metadata["volumes"][src_dir], 1)
                break
        if not cwd:
            cwd = '/seith_temp' # TODO add to config
    

    env = json.loads(args.env)

    r = container.exec_run(command,
                       stdout=True,
                       stderr=True,
                       stdin=True,
                       tty=True,
                       socket=True,
                       workdir=cwd,
                       user=args.user,
                       environment=env,
                       )

    sock = r.output._sock
    
    # VIBE CODED
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        while True:
            readable, _, _ = select.select([sock, sys.stdin], [], [], 0.1)

            if sock in readable:
                data = sock.recv(1024)
                if not data:
                    break
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()

            if sys.stdin in readable:
                data = os.read(fd, 1024)
                if not data:
                    break
                sock.sendall(data)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sock.close()

