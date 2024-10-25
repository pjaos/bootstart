# bootstart
A simple command to automate the execution of a script file on boot using systemd on Linux platforms.

# Building bootstart
To build the package the python pipx and poetry modules must be installed on a debian/ubuntu system.
This can be done as shown below.

```
sudo apt update
sudo apt install python3-venv
sudo apt install pipx
sudo pipx ensurepath
sudo pipx install poetry
pipx ensurepath
pipx install poetry
```

The python wheel package can be built by executing the build.sh script as shown below.

```
./build.sh 
Using virtualenv: /home/username/.cache/pypoetry/virtualenvs/bootstart-hEAeM5vN-py3.12
Building bootstart (1.0)
  - Building sdist
  - Adding: /scratch/git_repos/python3/bootstart/bootstart/__init__.py
  - Adding: /scratch/git_repos/python3/bootstart/bootstart/bootstart.py
  - Adding: pyproject.toml
  - Adding: README.md
  - Built bootstart-1.0.tar.gz
  - Building wheel
  - Adding: /scratch/git_repos/python3/bootstart/bootstart/__init__.py
  - Adding: /scratch/git_repos/python3/bootstart/bootstart/bootstart.py
  - Built bootstart-1.0-py3-none-any.whl
```

This will create the bootstart-1.0-py3-none-any.whl file in the dist folder.

# Installing bootstart
Note !!!

- bootstart must be installed as the root user.
- The version in the bootstart python wheel file may change.

The python wheel package can be installed as shown below. 

```
sudo pipx install dist/bootstart*.whl
  installed package bootstart 1.0, installed using Python 3.12.3
  These apps are now globally available
    - bootstart
⚠️  Note: '/root/.local/bin' is not on your PATH environment variable. These apps will not be globally accessible until your PATH is updated. Run `pipx ensurepath` to automatically add it, or manually
    modify your PATH in your shell's config file (i.e. ~/.bashrc).
done! ✨ 🌟 ✨
```

# Using bootstart
Once the bootstart command is installed as detailed above you can use it to ensure command/script files are executed each time a machine boot up.

For this example the /tmp/loop.sh script file is created

```
#!/bin/bash

num=1
while [ True ]; do
        echo "INFO: num = $num"
        num=$(($num+1))
        sleep 1
done
```

This will output an incrementing count.

## Enable boot time script execution.
To ensure this script file is started at boot time the following bootstart command can be used.

```
bootstart -f /tmp/loop.sh --enable_auto_start
INFO:  OS: Linux
INFO:  SERVICE FILE: /etc/systemd/system/loop.sh.service
INFO:  Created /etc/systemd/system/loop.sh.service
INFO:  Enabled loop.sh.service on restart
INFO:  Started loop.sh.service
root@L7490:/etc/systemd/system# 
```

Once started the syslog output shows

```
tail -f /var/log/syslog
2024-10-25T09:02:01.624103+01:00 192.168.0.10 552568 root-/root/.local/bin/bootstart: INFO:  OS: Linux
2024-10-25T09:02:01.625229+01:00 192.168.0.10 552568 root-/root/.local/bin/bootstart: INFO:  SERVICE FILE: /etc/systemd/system/loop.sh.service
2024-10-25T09:02:01.626333+01:00 192.168.0.10 552568 root-/root/.local/bin/bootstart: INFO:  Created /etc/systemd/system/loop.sh.service
2024-10-25T09:02:05.333743+01:00 192.168.0.10 552568 root-/root/.local/bin/bootstart: INFO:  Enabled loop.sh.service on restart
2024-10-25T09:02:08.541430+01:00 192.168.0.10 552568 root-/root/.local/bin/bootstart: INFO:  Started loop.sh.service
2024-10-25T09:02:08.718466+01:00 192.168.0.10 552971 root-/root/.local/bin/bootstart: DEBUG: CMD: command/script file: /tmp/loop.sh
2024-10-25T09:02:08.725952+01:00 L7490 bootstart[552972]: INFO: num = 1
2024-10-25T09:02:09.731946+01:00 L7490 bootstart[552972]: INFO: num = 2
2024-10-25T09:02:10.737717+01:00 L7490 bootstart[552972]: INFO: num = 3
2024-10-25T09:02:11.742400+01:00 L7490 bootstart[552972]: INFO: num = 4
2024-10-25T09:02:12.750531+01:00 L7490 bootstart[552972]: INFO: num = 5
```

## Checking a script file execution.
You can check on the status as shown below.

```
bootstart -f /tmp/loop.sh --check_auto_start
INFO:  OS: Linux
INFO:  ● loop.sh.service
INFO:       Loaded: loaded (/etc/systemd/system/loop.sh.service; enabled; preset: enabled)
INFO:       Active: active (running) since Fri 2024-10-25 09:02:08 BST; 3min 53s ago
INFO:     Main PID: 552971 (bootstart)
INFO:        Tasks: 3 (limit: 38285)
INFO:       Memory: 7.1M (peak: 7.7M)
INFO:          CPU: 1.488s
INFO:       CGroup: /system.slice/loop.sh.service
INFO:               ├─552971 /root/.local/share/pipx/venvs/bootstart/bin/python /root/.local/bin/bootstart -f /tmp/loop.sh
INFO:               ├─552972 /bin/bash /tmp/loop.sh
INFO:               └─554906 sleep 1
INFO:  
INFO:  Oct 25 09:05:53 L7490 bootstart[552972]: INFO: num = 224
INFO:  Oct 25 09:05:54 L7490 bootstart[552972]: INFO: num = 225
INFO:  Oct 25 09:05:55 L7490 bootstart[552972]: INFO: num = 226
INFO:  Oct 25 09:05:56 L7490 bootstart[552972]: INFO: num = 227
INFO:  Oct 25 09:05:57 L7490 bootstart[552972]: INFO: num = 228
INFO:  Oct 25 09:05:58 L7490 bootstart[552972]: INFO: num = 229
INFO:  Oct 25 09:05:59 L7490 bootstart[552972]: INFO: num = 230
INFO:  Oct 25 09:06:00 L7490 bootstart[552972]: INFO: num = 231
INFO:  Oct 25 09:06:01 L7490 bootstart[552972]: INFO: num = 232
INFO:  Oct 25 09:06:02 L7490 bootstart[552972]: INFO: num = 233
INFO:  
INFO:  
```

## Stopping a script files execution.
You may stop the execution of the script at boot time as shown below.

```
bootstart -f /tmp/loop.sh --disable_auto_start
INFO:  OS: Linux
INFO:  SERVICE FILE: /etc/systemd/system/loop.sh.service
INFO:  Disabled loop.sh.service on restart
INFO:  Stopped loop.sh.service
```

## Command line help
The command line help for the bootstart command is shown below.

```
bootstart -h
usage: bootstart [-h] [-d] [-f FILE] [-s SECONDS] [-n NAME]
                 [--enable_auto_start] [--disable_auto_start]
                 [--check_auto_start]

A simple way of running a command/script on a Linux system using systemd when the computer starts.
The output (stdout) from the executed script is sent to syslog.

options:
  -h, --help            show this help message and exit
  -d, --debug           Enable debugging.
  -f FILE, --file FILE  The command/script file to execute. No arguments can
                        be passed to this command/script.
  -s SECONDS, --seconds SECONDS
                        The restart delay for the command/script in seconds
                        (default=1.0). If the script file stops running for
                        any reason then an attempt to restart it will be made
                        after this delay.
  -n NAME, --name NAME  The name of the service to be created. If this is left
                        blank the name of the service name is the filename of
                        the command/script file.
  --enable_auto_start   Auto start when this computer starts.
  --disable_auto_start  Disable auto starting when this computer starts.
  --check_auto_start    Check the status of an auto started icons_gw instance.
```