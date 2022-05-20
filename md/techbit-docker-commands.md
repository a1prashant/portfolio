# Docker Commands

## Run

| use | command | comment |
|-----|---------|---------|
| run in background | ```docker run --detach jenkins``` |  |
| in interactive mode | ```docker run -it ubuntu bash``` |  |
| export port | ```docker run -p 80:80 nginx``` |  |
| with name | ```docker run --name mydb redis``` |  |
| restart container | ```docker start mydb``` |  |
| stop container | ```docker stop mydb``` |  |
| open new process on running container | ```docker exec -it c2332 bash``` |  |
| see logs of running container | ```docker logs -f c2332``` |  |
| show ports of running container | ```docker port c23332``` |  |
| bring up group of containers | ```docker-compose up -d``` | CWD should have 'docker-compose.yml' |
|  |  |  |

## Build

| use | command | comment |
|-----|---------|---------|
| build | ```docker build .``` |  |
| with name | ```docker build --tag myimage .``` |  |
| convert to image | ```docker commit c2332 myimage``` |  |
| compose to build | ```docker-compose build``` | CWD should have 'docker-compose.yml' |

## Remove

| use | command | comment |
|-----|---------|---------|
| remove all unused | ```docker rmi $(docker images -q -f dangling=true)``` |  |
| kill running | ```docker kill $(docker ps -q)``` |  |

## Manage

| use | command | comment |
|-----|---------|---------|
| list running | ```docker ps``` |  |
| running and stopped | ```docker ps -a``` |  |
| check metadata | ```docker inspect c23332``` |  |
| list images | ```docker images``` |  |
| list having labels | ```docker ps --filter label=abc.backend``` |  |
|  |  |  |

## Volume

| use | command | comment |
|-----|---------|---------|
| local volume | ```docker volume create --name myvol``` |  |
| mount | ```docker run -v myvol:/data redis``` | host path mapped to container path |
| remove | ```docker volume rm myvol``` |  |
| list volumes | ```docker volume ls``` |  |
|  |  |  |

# Kill

| use | command | comment |
|-----|---------|---------|
|  | ```docker rmi $(docker images -q -f "dangling=true")``` |  |
|  |  |  |

TODO: