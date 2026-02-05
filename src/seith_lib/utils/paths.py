import os
import platform

os_platform = platform.system()

if os_platform == 'Linux':
    config_home = os.environ["XDG_CONFIG_HOME"] + '/seith'
    data_home   = os.environ["XDG_DATA_HOME"] + '/seith'
    os.makedirs(data_home, exist_ok=True)
    pass
elif os_platform == 'Darwin': # MAC
    pass
elif os_platform == 'Windows':
    pass
else:
    print('UNSUPPORT OS')
    exit()


metadata = data_home + "/metadata.json"

