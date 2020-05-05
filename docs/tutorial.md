# senzing-environment tutorial

The following demonstrations show how to augment Senzing projects with `senzing-environment`
to facilitate the use of Docker within a project.

The first demonstration shows how to use `docker-compose` with a Senzing project.
The second demonstration shows how to use independent docker containers within a Senzing project.

## Demonstration 1

### Create new Senzing project with Docker support

1. Specify the location of the Senzing project on the host system.
   Example:

    ```console
    export SENZING_PROJECT_DIR=~/senzing-demo-project-1
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
    export SENZING_PROJECT_NAME=demo01
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
      senzing/senzing-environment add-docker-support \
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

1. Perform work-around for sym-link in sub-directories.
   Example:

    ```console
    mv ${SENZING_PROJECT_DIR}/resources/config ${SENZING_PROJECT_DIR}/resources/config.$(date +%s)
    mv ${SENZING_PROJECT_DIR}/resources/schema ${SENZING_PROJECT_DIR}/resources/schema.$(date +%s)

    cp -r /opt/senzing/g2/resources/config/ ${SENZING_PROJECT_DIR}/resources/
    cp -r /opt/senzing/g2/resources/schema/ ${SENZING_PROJECT_DIR}/resources/
    ```

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
    1. [Senzing API](http://editor.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api/master/senzing-rest-api.yaml)
    1. [Entity search webapp](http://localhost:8251/)
    1. [Jupyter notebooks](http://localhost:9178/)
    1. [X-Term](http://localhost:8254/) for Senzing command line tools
        1. Command:

            ```console
            poc_snapshot.py -o /var/opt/senzing/test-snapshot
            ```

        1. Where did it go on the workstation?
           Answer:

            ```console
            ls ${SENZING_PROJECT_DIR}/var
            ```

### Bring down Docker formation

1. Bring down Docker formation.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo \
      --preserve-env \
      docker-compose --file resources/postgresql/docker-compose-rabbitmq-postgresql.yaml down
    ```

## Demonstration 2

### Create second Senzing project with Docker support

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
      senzing/senzing-environment add-docker-support \
        --project-name ${SENZING_PROJECT_NAME} \
        --project-dir ${SENZING_PROJECT_DIR}
    ```

1. Perform work-around for sym-link in sub-directories.
   Example:

    ```console
    mv ${SENZING_PROJECT_DIR}/resources/config ${SENZING_PROJECT_DIR}/resources/config.$(date +%s)
    mv ${SENZING_PROJECT_DIR}/resources/schema ${SENZING_PROJECT_DIR}/resources/schema.$(date +%s)

    cp -r /opt/senzing/g2/resources/config/ ${SENZING_PROJECT_DIR}/resources/
    cp -r /opt/senzing/g2/resources/schema/ ${SENZING_PROJECT_DIR}/resources/
    ```

### Bring up RabbitMQ

1. RabbitMQ needs to come up before `senzing/mock-data-generator` and `senzing/stream-loader`.
   Execute script to docker run `bitnami/rabbitmq`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-rabbitmq.sh
    ```

1. View [RabbitMQ](http://localhost:15672)

### Bring up mock-data-generator

1. Execute script to docker run `senzing/mock-data-generator`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-mock-data-generator.sh
    ```

### Bring up Senzing init container

1. Execute script to docker run `senzing/init-container`.
   `senzing/init-container` initialized configuration files (i.e. `.../etc` files)
   and initializes config in SQLite database.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-init-container.sh
    ```

### Bring up Senzing stream-loader

1. Execute script to docker run `senzing/stream-loader`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-stream-loader.sh
    ```

### Bring up SQLite  web viewer

1. Execute script to docker run `coleifer/sqlite-web`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-sqlite-web.sh
    ```

1. View [SQLite Web](http://localhost:9174)

### Bring up Senzing API Server

1. Execute script to docker run `senzing/senzing-api-server`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-api-server.sh
    ```

1. View [Senzing API](http://editor.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api/master/senzing-rest-api.yaml)

### Bring up Senzing Entity Search WebApp

1. Execute script to docker run `senzing/entity-search-web-app`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-webapp.sh
    ```

1. View  [Entity search webapp](http://localhost:8251/)

### Bring up Jupyter

1. Execute script to docker run `senzing/jupyter`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-jupyter.sh
    ```

1. View [Jupyter notebooks](http://localhost:9178/)

### Bring up X-Term

1. Execute script to docker run `senzing/xterm`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-xterm.sh
    ```

1. View [X-Term](http://localhost:8254/)

### Bring up Senzing debug

1. Execute script to docker run `senzing/senzing-debug`.
   Example:

    ```console
    ~/senzing-demo-project-2/docker-bin/senzing-debug.sh
    ```

1. Enter the Senzing debug docker container.
   Example:

    ```console
    docker exec -it ${SENZING_PROJECT_NAME}-debug /bin/bash
    ```
