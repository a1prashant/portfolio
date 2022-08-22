# Ansible

- Works only on Linux
- On Windows via WSL is tricky and useless

## Linux Steps

- Steps: https://docs.ansible.com/ansible/latest/installation_guide/installation_distros.html#installing-ansible-on-ubuntu
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

## Trying tutorial:
https://riptutorial.com/Download/ansible.pdf

```
mkdir work/sandbox-ansible
vim hosts
```
Add data:
```
192.168.100.110
192.168.100.111
192.168.100.112
```

- On command-line, run: `ansible all -m ping -k -i .`
- If error "Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host."
- vim /etc/ansible/ansible.cfg
- Add text
```
[defaults]
inventory = /etc/hostfile.txt
host_key_checking = False
```
- Run again `ansible all -m ping -k -i .`
- Should see output:
```
SSH password:
192.168.100.110 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.100.111 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
192.168.100.112 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```
