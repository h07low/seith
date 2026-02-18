import json
import shlex
import termios, tty, sys, select, os   # needed for tty 
from pathlib import Path

from seith_lib.utils import docker_utils, metadata_utils, utils


def auto_encode(commands):
    final_command=[]
    for c in commands:
        if c.isalnum():  # no special chars
            final_command.append(c)

        elif c[0]=="'" or c[0]=='"':  # already embedded in quotes
            # its ok
            final_command.append(c)

        elif c[0].isalnum():
            final_command.append("'"+c+"'")
        
        else:
            final_command.append(c)

    return final_command
        

def run(args):
    '''
    args:
        container
        env
        shell
        cwd
        command
    '''
    if args.encode == 'auto':
        cmds = auto_encode(args.command)
    elif args.encode == 'all':
        cmds = [shlex.quote(i) for i in args.command]
    else:
        cmds = args.command

    command = "{0} -lc {1}".format(args.shell, shlex.quote(" ".join(cmds)))

    
    container = docker_utils.get_container(args.container)
    if container.status != 'running':
        print(container.status)
        print('container not running')
        exit() #TODO manage

    # calculate CWD
    cwd = args.cwd
    if not cwd:
        cwd = utils.translate_cwd(args.container)
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

