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

- Run `ansible all -m ping -k -b -i .`
- If error "Missing sudo password"
- Run `ansible all -m ping -k -K -b -i .`
- Note: -k, --ask-pass: ask for connection password
- Note: -K, --as-become-pass: ask for previlege escalation password

- Verify following before using:
```
192.168.100.110 ansible_user=<username> ansible_ssh_pass=<password>
```

- To install jdk, jre
```
---
- name: install-java
  hosts: all
  vars:
    - basedir: '/usr/local'
    - sparkdir: '/usr/local/spark-3.3.0-bin-hadoop3'
    - tempdir: '/tmp'

  tasks:
    - name: apt update
      become: yes
      apt: update_cache=yes force_apt_get=yes cache_valid_time=3600

    - name: jdk-install
      become: yes
      apt:
        name: "openjdk-17-jdk"
        state: present

    - name: jre-install
      become: yes
      apt:
        name: "openjdk-17-jre"
        state: present

    - name: check-jdk-jre-installation
      become: yes
      shell: 'java --version'

    - name: create-spark-dest-dir
      become: yes
      file:
        path: "{{ sparkdir }}"
        state: directory
        mode: '0755'

    - name: get spark
      become: yes
      ansible.builtin.get_url:
        url: https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
        dest: "{{ tempdir }}"
        mode: '0755'

    - name: extract spark
      become: yes
      ansible.builtin.unarchive:
        src: "{{ tempdir }}/spark-3.3.0-bin-hadoop3.tgz"
        dest: "{{ basedir }}"
        remote_src: yes
      environment:
        PATH: "{{ sparkdir }}/bin:{{ sparkdir }}/sbin:{{ ansible_env.PATH }}"

    - name: spark in environment
      become: yes
      ansible.builtin.lineinfile:
        path: "/etc/environment"
        line: "export PATH={{ sparkdir }}/bin:{{ sparkdir }}/sbin:{{ ansible_env.PATH }}"
        create: yes

    - name: check-spark-installation
      become: yes
      shell: 'spark-shell --version'

```

- To run: `ansible-playbook sample.yml -i . -k -K`
Works fine!

