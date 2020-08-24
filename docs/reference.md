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
   Brings up [Portainer](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/portainer.md).

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

### senzing-api-server

1. **Synopsis:**
   Brings up [Senzing API server](https://github.com/Senzing/senzing-api-server).

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
   [localhost:9170/heartbeat](http://localhost:9170/heartbeat).

1. **swagger-ui:**
   The [Senzing REST API specification](https://github.com/Senzing/senzing-rest-api-specification)
   can be viewed with the online
   [Swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/Senzing/senzing-rest-api-specification/master/senzing-rest-api.yaml).

   However, there may be an issue when interacting with the Senzing API Server.
   Another approach to viewing and interacting with the Senzing REST API is by using
   [swagger-ui.sh](#swagger-ui).

### senzing-console

### senzing-db2-driver-installer

### senzing-debug

### senzing-environment.py

### senzing-init-container

### senzing-jupyter

### senzing-phppgadmin

### senzing-postgresql-init

### senzing-quickstart-demo

### senzing-rabbitmq

### senzing-sqlite-web

### senzing-stream-loader

### senzing-stream-producer

### senzing-webapp-demo-01

### senzing-webapp-demo

### senzing-webapp

### senzing-xterm-shell

### senzing-xterm

### senzing-yum

### swagger-ui
