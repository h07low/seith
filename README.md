# seith 
layer between docker and cli to better handle your container

## Feature
- specify package to install and automatically install and upgrade them all
- automatically translates your CWD using volumes

## Install
using pipx
```
pipx install git+https://github.com/h07low/seith.git
```


## example usage
### create
create a new container ( if no conf_dir is specified seith tries to access XDG_CONFIG_HOME/seith/<container_name> )
```
seith.py create demo
```

example conf.json:
```
{
	"image": "debian:latest",
	"network": "host",
	"privileged": true,
	"cap_add": [],
	"cap_del": [],
	
	"volumes": {"/tmp/": {"bind":"/seith_temp", "mode":"rw"},
		"/home/sigpwn/hacking":{"bind":"/home_sigpwn", "mode": "rw"},

	"command": "sleep infinity",
}
``` 

### packages
install packages, you can specify packages to install in the `deps` dir of the configuration directory, follows an example:
```
{
	"name": "APT",
	"install": "apt update && apt install -y {0}",
	"unique_install": true,

	"separator": " ",
	"deps":["vim", "nano", "python3", "git", "wireshark", "pipx"],

	"upgrade": "apt update && apt upgrade",
	"unique_upgrade": true,

	"priority": "50"
	
}
```

the deps attribute can either be a list or an object as the follow:
```
{
	"name": "GIT",
	"install": "cd /opt/ && git clone {0[repo]}",
	"unique_install": false,

	"separator": " ",
	"deps":{
		"SecLists":
			{"repo": "https://github.com/danielmiessler/SecLists.git", "dir_name":"SecLists"}
	},

	"upgrade": "cd /opt/{0[dir_name]} && git pull",
	"unique_upgrade": true,

	"priority": "60"
	
}
```

moreover you can have a directory `script` inside `deps` which is copied into the docker as `/seith_deps_scripts` so that if necessary you can be more creative with the installation or upgrade command.

to install the packages you can simply run:
```
seith.py sync_deps demo
```

to upgrade installed packages:
```
seith.py upgrade demo
```

### exec commands
to run a command in the docker simply do the following. 
```
seith.py exec demo --cwd / -- ls -la
```

seith automatically tries to translate your current directory in docker using volumes, if it fails to do so it uses the dir `/seith_temp` which you can bind using a volume to access it directly or you can specify it using `--cwd`.

by default seith uses bash to run your command doing `bash -c 'your command'`, if you want you can specify another shell like `zsh` or `sh` using `--shell`.

