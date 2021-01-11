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
    == portainer running on http://0.0.0.0:9170
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#portainer
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
    ==============================================================================
    == postgres listening on 0.0.0.0:5432
    == Username: na Password: na
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#postgres
    ==============================================================================
    ```

### senzing-api-server

1. **Synopsis:**

   Brings up [Senzing API server](https://github.com/Senzing/senzing-api-server) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-api-server.sh up
    ==============================================================================
    == api-server running on http://0.0.0.0:8250
    == Try http://0.0.0.0:8250/heartbeat
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-api-server.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-api-server
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
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-console
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
    == Log: /home/senzing/senzing-project/var/log/senzing-db2-driver-installer.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-db2-driver-installer
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
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-debug.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-debug
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
    == http://hub.senzing.com/senzing-environment/reference#senzing-down
    ==
    == Done.
    ==============================================================================
    ```

### senzing-environment

1. **Synopsis:**

   Runs [senzing-environment](https://github.com/Senzing/senzing-environment) task.

### senzing-info

1. **Synopsis:**

   Lists status of all Senzing containers. Format, by column:

    1. Container name
    1. Status:  **up** or **down**
    1. Host name and port
    1. Docker container image and version

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-info.sh
    ==============================================================================
    == senzing-info.sh M.m.P (yyyy-mm-dd)
    == senzing api: M.m.P  data: M.m.P
    ==
    == api-server    up http://0.0.0.0:8250   senzing/senzing-api-server:latest
    == jupyter     down http://0.0.0.0:9178   senzing/jupyter:latest
    == phppgadmin  down http://0.0.0.0:9171   senzing/phppgadmin:1.0.0
    == portainer   down http://0.0.0.0:9170   portainer/portainer:latest
    == quickstart  down http://0.0.0.0:8251   senzing/web-app-demo:latest
    == rabbit      down http://0.0.0.0:15672   bitnami/rabbitmq:3.8.2
    == sqlite-web  down http://0.0.0.0:9174   coleifer/sqlite-web:latest
    == swagger-ui  down http://0.0.0.0:9180   swaggerapi/swagger-ui:latest
    == webapp      down http://0.0.0.0:8251   senzing/entity-search-web-app:latest
    == xterm       down http://0.0.0.0:8254   senzing/xterm:latest
    ==
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-info
    ==============================================================================
    ```

### senzing-init-container

1. **Synopsis:**

   Runs [init-container](https://github.com/Senzing/docker-init-container) task.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-init-container.sh up
    ==============================================================================
    == init-container has completed.
    == Log: /home/senzing/senzing-project/var/log/senzing-init-container.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-init-container
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
    == jupyter running on http://0.0.0.0:9178
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /notebooks/shared > /home/senzing/senzing-project
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-jupyter.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-jupyter
    ==============================================================================
    ```

### senzing-mssql-driver-installer

1. **Synopsis:**

   Runs [apt](https://github.com/Senzing/docker-apt) install of `msodbcsql17`.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-mssql-driver-installer.sh up
    sudo access is required to change file ownership.  Please enter your password:
    ==============================================================================
    == mssql-driver-installer has completed.
    == Log: /home/senzing/senzing-project/var/log/senzing-mssql-driver-installer.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-mssql-driver-installer
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
    == phppgadmin running on http://0.0.0.0:9171
    == Log: /home/senzing/senzing-project/var/log/senzing-phppgadmin.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-phppgadmin
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
    == Log: /home/senzing/senzing-project/var/log/senzing-postgresql-init.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-postgresql-init
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
    == quickstart running on http://0.0.0.0:8251
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-quickstart-demo.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-quickstart-demo
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
    == rabbitmq running on http://0.0.0.0:15672
    == Username: user Password: bitnami
    == Mount information: (Format: in container > on host)
    ==   /bitnami  > /home/senzing/senzing-project/var/rabbitmq
    == Log: /home/senzing/senzing-project/var/log/senzing-rabbitmq.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-rabbitmq
    ==============================================================================
    ```

### senzing-sqlite-web

1. **Synopsis:**

   Brings up [coleifer/sqlite-web](https://hub.docker.com/r/coleifer/sqlite-web) service.

1. **Invocation:**

   Example:

    ```console
    $ ./docker-bin/senzing-sqlite-web.sh up
    ==============================================================================
    == sqlite-web running on http://0.0.0.0:9174
    == Mount information: (Format: in container > on host)
    ==   /data  > /home/senzing/senzing-project/var/sqlite
    == Log: /home/senzing/senzing-project/var/log/senzing-sqlite-web.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-sqlite-web
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
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-stream-loader.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-stream-loader
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
    == Log: /home/senzing/senzing-project/var/log/senzing-stream-producer.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-stream-producer
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
    == webapp running on http://0.0.0.0:8251
    == api-server running on http://0.0.0.0:8250/heartbeat
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-webapp-demo.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-webapp-demo
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
    == webapp running on http://0.0.0.0:8251
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-webapp.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-webapp
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
    == xterm running on http://0.0.0.0:8254
    == To enter xterm container, run:
    == docker exec -it xterm /bin/bash
    == Mount information: (Format: in container > on host)
    ==   /etc/opt/senzing  > /home/senzing/senzing-project/docker-etc
    ==   /opt/senzing/data > /home/senzing/senzing-project/data
    ==   /opt/senzing/g2   > /home/senzing/senzing-project
    ==   /var/opt/senzing  > /home/senzing/senzing-project/var
    == Log: /home/senzing/senzing-project/var/log/senzing-xterm.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#senzing-xterm
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
    ==============================================================================
    == swagger-ui running on http://0.0.0.0:9180
    == Log: /home/senzing/senzing-project/var/log/swagger-ui.log
    == For more information:
    == http://hub.senzing.com/senzing-environment/reference#swagger-ui
    ==============================================================================
    ```

   If running locally, it can be seen at
   [localhost:9180](http://localhost:9180).
