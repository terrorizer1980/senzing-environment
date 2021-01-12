# senzing-environment tutorial

The following demonstrations show how to augment Senzing projects with `senzing-environment`
to facilitate the use of Docker within a project.

The first demonstration shows how to use `docker-compose` with a Senzing project.
The second demonstration shows how to use independent docker containers within a Senzing project.

## Prerequisites for Tutorial

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-docker.md)

## Demonstrations

1. [Demonstration 1](#demonstration-1)
    1. Show how to
1. [Demonstration 2](#demonstration-2)
    1. Bring up `docker-compose` formation.
1. [Demonstration 3](#demonstration-3)
    1. Show use of most `docker-bin` shell scripts.

## Demonstration 1

Quick start demonstrations.
See:

1. [Quick Start for Linux](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/quickstart-linux.md)
1. [Quick Start for macOS](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/quickstart-macos.md)

## Demonstration 2

### Create Docker support for second Senzing project

1. Specify the location of the Senzing project on the host system.
   Example:

    ```console
    export SENZING_PROJECT_DIR=~/senzing-demo-project-2
    ```

1. Create the Senzing project.
   Example:

    ```console
    /opt/senzing/g2/python/G2CreateProject.py ${SENZING_PROJECT_DIR}
    ```

1. Give the Senzing project a name.
   The name is used as a prefix for docker containers.
   Example:

    ```console
    export SENZING_PROJECT_NAME=demo02
    ```

1. View the Senzing project.
   Example:

    ```console
    ls ${SENZING_PROJECT_DIR}
    ```

1. :pencil2: Identify the IP address of the host system.
   Example:

    ```console
    export SENZING_DOCKER_HOST_IP_ADDR=10.1.1.100
    ```

    1. To find the value for `SENZING_DOCKER_HOST_IP_ADDR` use Python interactively:
       Example:

        ```console
        python3
        ```

       Copy and paste the following lines into the Python REPL (Read-Evaluate-Print Loop):

        ```python
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        print("export SENZING_DOCKER_HOST_IP_ADDR={0}".format(sock.getsockname()[0]))
        sock.close()
        quit()
        ```

       Copy and paste the printed `export` statement into the host terminal.

1. Add Docker support to the Senzing project directory.
   Example:

    ```console
    docker run \
      --env SENZING_DOCKER_HOST_IP_ADDR=${SENZING_DOCKER_HOST_IP_ADDR} \
      --interactive \
      --rm \
      --tty \
      --user $(id -u):$(id -g) \
      --volume ${SENZING_PROJECT_DIR}:${SENZING_PROJECT_DIR} \
      senzing/senzing-environment add-docker-support-linux \
        --project-name ${SENZING_PROJECT_NAME} \
        --project-dir ${SENZING_PROJECT_DIR}
    ```

1. View the Senzing project again.
   Example:

    ```console
    ls ${SENZING_PROJECT_DIR}
    ```

   Notice the addition of `docker-bin`, `docker-etc`, and `docker-setupEnv`.
   The rest of `${SENZING_PROJECT_DIR}` is not modified.

### Bring up Docker formation

This Docker formation uses the docker-compose YAML file described in
[docker-compose-rabbitmq-postgresql](https://github.com/Senzing/docker-compose-demo/tree/master/docs/docker-compose-rabbitmq-postgresql#view-data).

1. View `docker-setupEnv`.
   Example:

    ```console
    cat ${SENZING_PROJECT_DIR}/docker-setupEnv
    ```

   When sourced, environment variables are set for docker formations using `${SENZING_PROJECT_DIR}` directories.
   `docker-setupEnv` also creates empty directories for use with PostgreSQL and RabbitMQ.

   Something worthy of noting:  the `SENZING_ETC_DIR` references the `docker-etc` directory.
   `docker-etc` is similar to the `etc` directory, but the files have been modified
   to reflect the paths of files being **inside** a docker container, not **outside** on the host system's Senzing project.

1. Set environment variables using `source`.
   Example:

    ```console
    source ${SENZING_PROJECT_DIR}/docker-setupEnv
    ```

1. Verify environment variables.
   Example:

    ```console
    env | grep SENZING
    ```

1. Clone repository containing `docker-compose` YAML files.

    1. Set environment variable of where to clone repository.
       Example:

        ```console
        export GIT_ACCOUNT=senzing
        export GIT_REPOSITORY=docker-compose-demo
        export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
        export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
        ```

    1. Follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/clone-repository.md) to install the Git repository.

1. Bring up docker formation.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo \
      --preserve-env \
      docker-compose --file resources/postgresql/docker-compose-rabbitmq-postgresql.yaml up
    ```

### View data

1. [View](https://github.com/Senzing/docker-compose-demo/tree/master/docs/docker-compose-rabbitmq-postgresql#view-data)
   data in different phases of the data flow:
    1. [RabbitMQ](http://localhost:15672) (username: user  password: bitnami)
    1. [PostgreSQL](http://localhost:9171) (username: postgres password: postgres)
    1. [Senzing API](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api-specification/master/senzing-rest-api.yaml)
    1. [Entity search webapp](http://localhost:8251/)
    1. [Jupyter notebooks](http://localhost:9178/)
    1. [X-Term](http://localhost:8254/) for Senzing command line tools

### Bring down Docker formation

1. Bring down Docker formation.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo \
      --preserve-env \
      docker-compose --file resources/postgresql/docker-compose-rabbitmq-postgresql.yaml down
    ```

## Demonstration 3

This demonstration creates a local PostgreSQL database and RabbitMQ queue.
It shows how to bring up individual Docker containers.

The demonstration works on the Linux operating system
(e.g. not macOS, nor Windows).

### Install Senzing

:thinking: Installing Senzing on Linux is a "one-time task".
If Senzing is already installed,
proceed to [Create third Senzing project](#create-third-senzing-project).

Depending on the distribution of Linux, there are different ways of installing Senzing.

1. For installation on Red Hat, CentOS, openSuse and
   [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#RPM-based).
    1. Visit to [How to install Senzing API - CentOS](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-senzing-api.md#centos).
1. For installation on Debian, Ubuntu and
   [others](https://en.wikipedia.org/wiki/List_of_Linux_distributions#Debian-based).
    1. Visit to [How to install Senzing API - Ubuntu](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-senzing-api.md#ubuntu).

### Create third Senzing project

1. Specify the location of the Senzing project on the host system.
   Example:

    ```console
    export SENZING_PROJECT_DIR=~/senzing-demo-project-3
    ```

1. Create the Senzing project.
   Example:

    ```console
    /opt/senzing/g2/python/G2CreateProject.py ${SENZING_PROJECT_DIR}
    ```

### Identify host IP address

1. :pencil2: Set the [SENZING_DOCKER_HOST_IP_ADDR](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#senzing_docker_host_ip_addr) environment variable.
   Example:

    ```console
    export SENZING_DOCKER_HOST_IP_ADDR=10.1.1.100
    ```

    1. To find the value for `SENZING_DOCKER_HOST_IP_ADDR` use Python interactively:
       Example:

        ```console
        python3
        ```

       Copy and paste the following lines into the Python REPL (Read-Evaluate-Print Loop):

        ```python
        import socket

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        print("export SENZING_DOCKER_HOST_IP_ADDR={0}".format(sock.getsockname()[0]))
        sock.close()
        quit()
        ```

       Copy and paste the printed `export` statement into the host terminal.

### Identify Senzing database

1. Edit `${SENZING_PROJECT_DIR}/etc/G2Module.ini`
   Example:

    ```console
    vi ${SENZING_PROJECT_DIR}/etc/G2Module.ini
    ```

1. :pencil2: Modify contents of `${SENZING_PROJECT_DIR}/etc/G2Module.ini`.
   Change the SQL.CONNECTION value to point to the PostgreSQL instance
   using the `username`, `password`, and `hostname` of the PostgreSQL instance.
   Example:

    ```ini
    [SQL]
       CONNECTION=postgresql://username:password@hostname:5432:G2/
    ```

   :thinking: When complete, the entire file might look something like this:

    ```ini
    [PIPELINE]
     SUPPORTPATH=/home/username/senzing-demo-project-3/data
     CONFIGPATH=/home/username/senzing-demo-project-3/etc
     RESOURCEPATH=/home/username/senzing-demo-project-3/resources

    [SQL]
     CONNECTION=postgresql://postgres:postgres@10.1.1.100:5432:G2/
    ```

### Create Docker support for third Senzing project

1. Give the Senzing project a name.
   The name is used as a prefix in docker container names.
   Example:

    ```console
    export SENZING_PROJECT_NAME=demo03
    ```

1. Add Docker support to the Senzing project directory.
   Example:

    ```console
    docker run \
      --env SENZING_DOCKER_HOST_IP_ADDR=${SENZING_DOCKER_HOST_IP_ADDR} \
      --env SENZING_PROJECT_NAME=${SENZING_PROJECT_NAME} \
      --env SENZING_PROJECT_DIR=${SENZING_PROJECT_DIR} \
      --interactive \
      --rm \
      --tty \
      --user $(id -u):$(id -g) \
      --volume ${SENZING_PROJECT_DIR}:${SENZING_PROJECT_DIR} \
      senzing/senzing-environment add-docker-support-linux
    ```

### Bring up PostgreSQL database

:thinking: **Optional:** If a PostgreSQL is not already available,

1. Bring up PostgreSQL database engine.
   This will use the database information previously specified in
   [Identify Senzing database](#identify-senzing-database).
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/postgres.sh up
    ```

1. Bring up phpPgAdmin.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-phppgadmin.sh up
    ```

1. View [phpPgAdmin](http://localhost:9171)

1. Create Senzing schema in PostgreSQL.
   This is a job that will run to completion and exit.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-postgresql-init.sh up
    ```

### Bring up RabbitMQ

1. RabbitMQ needs to come up before `senzing/mock-data-generator` and `senzing/stream-loader`.
   Execute script to docker run `bitnami/rabbitmq`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-rabbitmq.sh up
    ```

1. View [RabbitMQ](http://localhost:15672)

### Bring up Senzing stream-producer

1. Execute script to docker run `senzing/mock-data-generator`.
   This is a job that will run to completion and exit.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-stream-producer.sh up
    ```

### Bring up Senzing init container

1. Work-around for permission problem.
   Example:

    ```console
    sudo chmod -R 777 ~/senzing-demo-project-3/var/postgres
    ```

1. Execute script to docker run `senzing/init-container`.
   `senzing/init-container` initialized configuration files (i.e. `.../etc` files)
   and initializes config in SQLite database.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-init-container.sh up
    ```

### Bring up Senzing stream-loader

1. Execute script to docker run `senzing/stream-loader`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-stream-loader.sh up
    ```

### Bring up Senzing API Server

1. Execute script to docker run `senzing/senzing-api-server`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-api-server.sh up
    ```

1. View [Senzing API](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api-specification/master/senzing-rest-api.yaml)

### Bring up Senzing Entity Search WebApp

1. Execute script to docker run `senzing/entity-search-web-app`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-webapp.sh up
    ```

1. View  [Entity search webapp](http://localhost:8251/)

### Bring up Jupyter

1. Execute script to docker run `senzing/jupyter`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-jupyter.sh up
    ```

1. View [Jupyter notebooks](http://localhost:9178/)

### Bring up X-Term

1. Execute script to docker run `senzing/xterm`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-xterm.sh up
    ```

1. View [X-Term](http://localhost:8254/)

### Bring up Swagger UI

1. Execute script to docker run `senzing/xterm`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/swagger-ui.sh up
    ```

1. View [Swagger UI](http://localhost:9180/)

### Show info

1. Execute script to view status of docker containers.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-info.sh
    ```

1. View [X-Term](http://localhost:8254/)

### Bring up Senzing console

1. Execute script to docker run `senzing/senzing-console`.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-console.sh up
    ```

1. When done, type "exit".

### Bring down everything

1. Execute script to stop all containers in this demonstration.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-down.sh
    ```

1. Verify containers are down.
   Example:

    ```console
    ~/senzing-demo-project-3/docker-bin/senzing-info.sh
    ```
