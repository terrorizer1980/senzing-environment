# senzing-environment reference

## Scripts

### docker-environment-vars

1. **Synopsis:**

   Sets environment variable for use by shell scripts.
   Generally, it does not need to be run on the command line.

1. With care, it can be modified.
   Example:
   Old:

     ```bash
    export SENZING_INPUT_URL="https://s3.amazonaws.com/public-read-access/TestDataSets/loadtest-dataset-1M.json"
     ```

   New:

     ```bash
    export SENZING_INPUT_URL="https://example.com/my/dataset.json"
     ```

### docker-pull-latest

1. **Synopsis:**

   Pulls the latest version of all docker images from the docker repository to the local workstation.

1. **Invocation:**

   Example:

    ```console
    ./docker-bin/docker-pull-latest.sh
    ```

### portainer

1. **Synopsis:**

   Brings up [Portainer](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/portainer.md) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/portainer.sh
     :
    ==============================================================================
    == portainer running on http://nnn.nnn.nnn.nnn:9170
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#portainer
    ==============================================================================
    ```

   If running locally, it can be seen at
   [localhost:9170](http://localhost:9170).

### postgres

1. **Synopsis:**

   Brings up [PostgreSQL](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/postgresql.md)
   docker container, `postgres`, service.

1. **Invocation:**

   Example:

    ```console
    $ ./postgres.sh
     :
    ==============================================================================
    == postgres listening on nnn.nnn.nnn.nnn:5432
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#postgres
    ==============================================================================
    ```

### senzing-api-server

1. **Synopsis:**

   Brings up [Senzing API server](https://github.com/Senzing/senzing-api-server) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-api-server.sh
     :
    ==============================================================================
    == api-server running on http://nnn.nnn.nnn.nnn:9170
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-api-server
    ==============================================================================
    ```

   If running locally, the "heartbeat" can be seen at
   [localhost:8250/heartbeat](http://localhost:8250/heartbeat).

1. **swagger-ui:**

   The [Senzing REST API specification](https://github.com/Senzing/senzing-rest-api-specification)
   can be viewed with the online
   [Swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api-specification/master/senzing-rest-api.yaml).

   However, there may be an issue when interacting with the Senzing API Server.
   Modern web browsers use
   [CORS](https://www.w3.org/wiki/CORS)
   and prevent
   [mixed content](https://developers.google.com/web/fundamentals/security/prevent-mixed-content/what-is-mixed-content)
   to protect users.
   These preventative measures may interfere with using the "Swagger UI" to interact with the Senzing API server.

   To avoid this issue, use
   [swagger-ui.sh](#swagger-ui).
   It brings up a docker container that will allow `http://` support.

### senzing-console

1. **Synopsis:**

   Brings up [Senzing console](https://github.com/Senzing/docker-senzing-console) service.
   Functionally equivalent to [senzing-debug](#senzing-debug) minus
   `docker run ... --cap-add=ALL` parameter.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-console.sh
     :
    I have no name!@aaaaaaaaaaaa:/app$
    ```

   After invocation, the prompt is from inside the container.

### senzing-db2-driver-installer

1. **Synopsis:**

   Runs [docker-db2-driver-installer](https://github.com/Senzing/docker-db2-driver-installer) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-db2-driver-installer.sh
     :
    yyyy-mm-dd hh:mm:ss,nnn senzing-50080297I Enter {...}
    yyyy-mm-dd hh:mm:ss,nnn senzing-50080150I /opt/IBM-template copied to /opt/IBM/.
    yyyy-mm-dd hh:mm:ss,nnn senzing-50080298I Exit {...}
    sudo access is required to change file ownership.  Please enter your password:
    ```

### senzing-debug

1. **Synopsis:**

   Brings up [Senzing debug](https://github.com/Senzing/docker-senzing-debug) service.
   Functionally equivalent to [senzing-console](#senzing-console) plus
   `docker run ... --cap-add=ALL` parameter and runs as `root` user.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-debug.sh
     :
    /app/sleep-infinitely.sh is sleeping infinitely.
    ```

   After invocation, use `docker-exec` to enter the container.
   Example:

    ```console
    docker exec -it ${SENZING_PROJECT_NAME}-debug /bin/bash
    ```

### senzing-environment

1. **Synopsis:**

   Runs [senzing-environment](https://github.com/Senzing/senzing-environment) task.

### senzing-init-container

1. **Synopsis:**

   Runs [init-container](https://github.com/Senzing/docker-init-container) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-init-container.sh
     :
    yyyy-mm-dd hh:mm:ss,nnn senzing-50070297I Enter {...}
     :
    yyyy-mm-dd hh:mm:ss,nnn senzing-50070171I Default config in SYS_CFG already exists having ID nnnnnnnnn
    yyyy-mm-dd hh:mm:ss,nnn senzing-50070155I /etc/opt/senzing/g2config.json - Deleting
    yyyy-mm-dd hh:mm:ss,nnn senzing-50070298I Exit {...}
    ```

### senzing-jupyter

1. **Synopsis:**

   Brings up [Senzing Jupyter](https://github.com/Senzing/docker-jupyter) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-jupyter.sh
     :
    ==============================================================================
    == jupyter running on http://nnn.nnn.nnn.nnn:9178
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-jupyter
    ==============================================================================
     :
    Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    ```

### senzing-phppgadmin

### senzing-postgresql-init

### senzing-quickstart-demo

### senzing-rabbitmq

### senzing-sqlite-web

### senzing-stream-loader

### senzing-stream-producer

### senzing-webapp-demo

### senzing-webapp

### senzing-xterm-shell

### senzing-xterm

### senzing-yum

### swagger-ui

1. **Synopsis:**

   Brings up [Senzing UI](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/swagger-ui.md).

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/swagger-ui.sh
     :
    ==============================================================================
    == swagger-ui running on http://nnn.nnn.nnn.nnn:9180
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#swagger-ui
    ==============================================================================
    ```

   If running locally, it can be seen at
   [localhost:9180](http://localhost:9180).
