How to quickly setup Development Environment on Windows
==============

# Install Chocolatey

Go to https://chocolatey.org/install

Install using the steps given there, or use further instructions:

Open in 'Administrative Mode' a 'PowerShell' command line tool.

Run following command:

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

--

> DO NOT INSTALL ALL !!!

> CHOOSE YOUR TOOL AND THEN INSTALL !!!


----

# Install tools:

In the same PowerShell command line tool having administrative access, run following commands:

- Ever needed tools:

```
choco install vscode -y
# -or-
choco install intellijidea-edu -y

choco install python3 -y
choco install docker-desktop -y
choco install adobereader -y
choco install javaruntime -y
choco install googlechrome -y
```

- For Java and Web related dev:

```
choco install oraclejdk -y
choco install openjdk11 -y
choco install vscode-java -y
choco install postman -y
choco install maven -y
```

--

- Git related tools:
```
choco install git -y
choco install git.install -y
choco install github-desktop -y
```

--

- Designer and Modeling tools:
  
```
choco install gimp -y
choco install inkscape -y
choco install drawio -y
choco install vscode-drawio -y
```

--

- Linux command line support:

```
choco install wsl -y
choco install msys2 --params "/NoUpdate /InstallDir:C:\msys2"
choco install curl -y
choco install wget -y
choco install vim -y
```

--

- Network and related utilities:
```
choco install openssh -y
choco install winscp.install -y
choco install wireshark -y
choco install putty -y
choco install superputty -y
```

--

- Other tools:
```
choco install winmerge -y
choco install 7zip.install -y
choco install notepadplusplus -y
choco install spotify -y
```

--

- For C++:
```
choco install llvm -y
choco install cmake -y
choco install conan -y
choco install bazel -y
choco install mingw -y
```

--

- Install postgresql DB:

```
choco install postgresql -y '/Password:password'
```


# Setup your GitLab SSH Key:

Create new key, change the "<comment>" string:
```
ssh-keygen -t ed25519 -C "<comment>"
```

then,
```
cat ~/.ssh/id_ed25519.pub | clip
```

then, go to: 
https://gitlab.com/-/profile/keys/
paste the key
