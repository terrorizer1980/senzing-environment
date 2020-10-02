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

   Pulls docker images from the docker repository to the local workstation.

1. **Invocation:**

   Example:

    ```console
    ./docker-bin/docker-pull-latest.sh
    ```

### portainer

1. **Synopsis:**

   Brings up
   [Portainer](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/portainer.md)
   service.
   Portainer helps visualize and manage Docker.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/portainer.sh up
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

   Brings up
   [PostgreSQL](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/postgresql.md)
   service.

1. **Invocation:**

   Example:

    ```console
    $ ./postgres.sh up
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
    $ ./docker-bin/senzing-api-server.sh up
     :
    ==============================================================================
    == api-server running on http://nnn.nnn.nnn.nnn:8250
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
    $ ./docker-bin/senzing-console.sh up
    ==============================================================================
    == To exit console, type 'exit'
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-console
    ==============================================================================
    I have no name!@aaaaaaaaaaaa:/app$
    ```

   After invocation, the prompt is from inside the container.

### senzing-db2-driver-installer

1. **Synopsis:**

   Runs [docker-db2-driver-installer](https://github.com/Senzing/docker-db2-driver-installer) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-db2-driver-installer.sh up
    sudo access is required to change file ownership.  Please enter your password:
    ==============================================================================
    == db2-driver-installer has completed.
    ==============================================================================
    ```

### senzing-debug

1. **Synopsis:**

   Brings up [Senzing debug](https://github.com/Senzing/docker-senzing-debug) service.
   Functionally equivalent to [senzing-console](#senzing-console) plus
   `docker run ... --cap-add=ALL` parameter and runs as `root` user.
   Unlike [senzing-console](#senzing-console),
   [Senzing debug](https://github.com/Senzing/docker-senzing-debug) runs in the background
   and `docker exec ...` is used to enter the container.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-debug.sh up
    ==============================================================================
    == debug is running.
    == To enter debug container, run:
    == sudo docker exec -it debug /bin/bash
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-debug
    ==============================================================================
    ```

   After invocation, use `docker exec` to enter the container.
   Example:

    ```console
    docker exec -it ${SENZING_PROJECT_NAME}-debug /bin/bash
    ```

### senzing-down

1. **Synopsis:**

   Brings down all containers launched from project folder.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-down.sh
    ==============================================================================
    == Bringing down all docker containers.
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-down
    ==
    == Done.
    ==============================================================================
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
    $ ./docker-bin/senzing-init-container.sh up
    ==============================================================================
    == init-container has completed.
    ==============================================================================
    ```

### senzing-jupyter

1. **Synopsis:**

   Brings up [Senzing Jupyter](https://github.com/Senzing/docker-jupyter) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-jupyter.sh up
    ==============================================================================
    == jupyter running on http://nnn.nnn.nnn.nnn:9178
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-jupyter
    ==============================================================================
    ```

### senzing-phppgadmin

1. **Synopsis:**

   Brings up [phpPgAdmin](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/phppgadmin.md) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-phppgadmin.sh up
    ==============================================================================
    == phppgadmin running on http://nnn.nnn.nnn.nnn:9171
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-phppgadmin
    ==============================================================================
    ```

### senzing-postgresql-init

1. **Synopsis:**

   Used with PostgreSQL database.
   Brings up [postgresql-client](https://github.com/Senzing/postgresql-client) and
   runs an SQL file to create tables in the PostgreSQL database.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-postgresql-init.sh up
    ==============================================================================
    == postgresql-init has completed.
    ==============================================================================
    ```

### senzing-quickstart-demo

1. **Synopsis:**

   Brings up [docker-web-app-demo](https://github.com/Senzing/docker-web-app-demo) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-quickstart-demo.sh up
    ==============================================================================
    == quickstart running on http://nnn.nnn.nnn.nnn:8251
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-quickstart-demo
    ==============================================================================
    ```

### senzing-rabbitmq

1. **Synopsis:**

   Brings up [bitnami/rabbitmq](https://hub.docker.com/r/bitnami/rabbitmq) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-rabbitmq.sh up
    ==============================================================================
    == rabbitmq running on http://nnn.nnn.nnn.nnn:15672
    == Username: xxxxxxxx Password: xxxxxxxx
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-rabbitmq
    ==============================================================================
    ```

### senzing-sqlite-web

1. **Synopsis:**

   Brings up [coleifer/sqlite-web](https://hub.docker.com/r/coleifer/sqlite-web) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-sqlite-web.sh up
     :
    ==============================================================================
    == sqlite-web running on http://nnn.nnn.nnn.nnn:9174
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-sqlite-web
    ==============================================================================
    ```

### senzing-stream-loader

1. **Synopsis:**

   Brings up [stream-loader](https://github.com/Senzing/stream-loader) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-stream-loader.sh up
    ==============================================================================
    == stream-loader is running.
    For more information:
    http://senzing.github.io/senzing-environment/reference#senzing-stream-loader
    ==============================================================================
    ```

### senzing-stream-producer

1. **Synopsis:**

   Runs [stream-producer](https://github.com/Senzing/stream-producer) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-stream-producer.sh up
    ==============================================================================
    == stream-producer is running.
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-stream-producer
    ==============================================================================
    ```

### senzing-webapp-demo

1. **Synopsis:**

   Brings up
   [senzing-api-server](https://github.com/Senzing/senzing-api-server) and
   [entity-search-web-app](https://github.com/Senzing/entity-search-web-app)
   services.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-webapp-demo.sh up
    ==============================================================================
    == webapp running on http://nnn.nnn.nnn.nnn:8251
    == api-server running on http://nnn.nnn.nnn.nnn:8250/heartbeat
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-webapp-demo
    ==============================================================================
    ```

### senzing-webapp

1. **Synopsis:**

   Brings up [entity-search-web-app](https://github.com/Senzing/entity-search-web-app) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-webapp.sh up
    ==============================================================================
    == webapp running on http://nnn.nnn.nnn.nnn:8251
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-webapp
    ==============================================================================
    ```

### senzing-xterm

1. **Synopsis:**

   Brings up [docker-xterm](https://github.com/Senzing/docker-xterm) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-xterm.sh up
    ==============================================================================
    == xterm running on http://nnn.nnn.nnn.nnn:8254
    == To enter xterm container, run:
    == docker exec -it xterm /bin/bash
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#senzing-xterm
    ==============================================================================
    ```

### senzing-yum

1. **Synopsis:**

   Runs [docker-yum](https://github.com/Senzing/docker-yum) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-yum.sh up
    :
    ```

### swagger-ui

1. **Synopsis:**

   Brings up [Senzing UI](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/swagger-ui.md) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/swagger-ui.sh up
     :
    ==============================================================================
    == swagger-ui running on http://nnn.nnn.nnn.nnn:9180
    == For more information:
    == http://senzing.github.io/senzing-environment/reference#swagger-ui
    ==============================================================================
    ```

   If running locally, it can be seen at
   [localhost:9180](http://localhost:9180).
