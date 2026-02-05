DEFAULT_CONF_DICT = {
        "image":"ubuntu:latest",
        "network":"bridge",
        "privileged":False,
        "auto_remove": True,
        "cap_add":[],
        "cap_del":[],
        "volumes":[],

        "ports":[],
        
        "command":"sleep infinite"
        }
