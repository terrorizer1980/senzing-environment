#! /usr/bin/env python3

# -----------------------------------------------------------------------------
# senzing-environment.py
# -----------------------------------------------------------------------------

from glob import glob
from urllib.parse import urlparse, urlunparse
import argparse
import configparser
import json
import linecache
import logging
import os
import parse
import shutil
import signal
import socket
import stat
import string
import sys
import time

__all__ = []
__version__ = "1.0.0"  # See https://www.python.org/dev/peps/pep-0396/
__date__ = '2020-04-23'
__updated__ = '2020-04-30'

SENZING_PRODUCT_ID = "5015"  # See https://github.com/Senzing/knowledge-base/blob/master/lists/senzing-product-ids.md
log_format = '%(asctime)s %(message)s'

# Working with bytes.

KILOBYTES = 1024
MEGABYTES = 1024 * KILOBYTES
GIGABYTES = 1024 * MEGABYTES

# Lists from https://www.ietf.org/rfc/rfc1738.txt

xsafe_character_list = ['$', '-', '_', '.', '+', '!', '*', '(', ')', ',', '"' ] + list(string.ascii_letters)
xunsafe_character_list = [ '"', '<', '>', '#', '%', '{', '}', '|', '\\', '^', '~', '[', ']', '`']
xreserved_character_list = [ ';', ',', '/', '?', ':', '@', '=', '&']

# The "configuration_locator" describes where configuration variables are in:
# 1) Command line options, 2) Environment variables, 3) Configuration files, 4) Default values

configuration_locator = {
    "debug": {
        "default": False,
        "env": "SENZING_DEBUG",
        "cli": "debug"
    },
    "project_dir": {
        "default": "~/senzing",
        "env": "SENZING_PROJECT_DIR",
        "cli": "project-dir"
    },
    "sleep_time_in_seconds": {
        "default": 0,
        "env": "SENZING_SLEEP_TIME_IN_SECONDS",
        "cli": "sleep-time-in-seconds"
    },
    "subcommand": {
        "default": None,
        "env": "SENZING_SUBCOMMAND",
    }
}

# Enumerate keys in 'configuration_locator' that should not be printed to the log.

keys_to_redact = [
    "password",
]

report_warnings = []
report_errors = []

# -----------------------------------------------------------------------------
# Define argument parser
# -----------------------------------------------------------------------------


def get_parser():
    ''' Parse commandline arguments. '''

    subcommands = {
        'add-docker-support': {
            "help": 'Update a G2Project to support docker.',
            "arguments": {
                "--debug": {
                    "action": "store_true",
                    "dest": "debug",
                    "help": "Enable debugging. (SENZING_DEBUG) Default: False"
                },
                "--project-dir": {
                    "dest": "project_dir",
                    "help": "Specify location of G2Project Default: ~/senzing",
                    "metavar": "SENZING_PROJECT_DIR",
                    "required": True
                },
            },
        },
        'docker-host': {
            "help": 'Show information on docker host.',
            "arguments": {
                "--debug": {
                    "action": "store_true",
                    "dest": "debug",
                    "help": "Enable debugging. (SENZING_DEBUG) Default: False"
                },
            },
        },
        'sleep': {
            "help": 'Do nothing but sleep. For Docker testing.',
            "arguments": {
                "--sleep-time-in-seconds": {
                    "dest": "sleep_time_in_seconds",
                    "help": "Sleep time in seconds. DEFAULT: 0 (infinite)",
                    "metavar": "SENZING_SLEEP_TIME_IN_SECONDS",
                },
            },
        },
        'version': {
            "help": 'Print version of program.',
        },
        'docker-acceptance-test': {
            "help": 'For Docker acceptance testing.',
        },
    }

    parser = argparse.ArgumentParser(prog="senzing-environment.py", description="Manage Senzing runtime environment. For more information, see https://github.com/Senzing/senzing-environment")
    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommands (SENZING_SUBCOMMAND):')

    for subcommand_key, subcommand_values in subcommands.items():
        subcommand_help = subcommand_values.get('help', "")
        subcommand_arguments = subcommand_values.get('arguments', {})
        subparser = subparsers.add_parser(subcommand_key, help=subcommand_help)
        for argument_key, argument_values in subcommand_arguments.items():
            subparser.add_argument(argument_key, **argument_values)

    return parser

# -----------------------------------------------------------------------------
# Message handling
# -----------------------------------------------------------------------------

# 1xx Informational (i.e. logging.info())
# 3xx Warning (i.e. logging.warning())
# 5xx User configuration issues (either logging.warning() or logging.err() for Client errors)
# 7xx Internal error (i.e. logging.error for Server errors)
# 9xx Debugging (i.e. logging.debug())


MESSAGE_INFO = 100
MESSAGE_WARN = 300
MESSAGE_ERROR = 700
MESSAGE_DEBUG = 900

message_dictionary = {
    "100": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}I",
    "101": "------------------------------------------------------------------------------",
    "102": "Modifying {0}...",
    "103": "   Changing {0}.{1} from {2} to {3}",
    "104": "   Keeping  {0}.{1} as {2}",
    "105": "   {0}.{1} doesn't exist",
    "106": "   Removed  {0}.{1}",
    "151": "{0} - Changing permissions from {1:o} to {2:o}",
    "173": "{0} - Changing owner from {1} to {2}",
    "153": "{0} - Changing group from {1} to {2}",
    "154": "{0} - Creating file by copying {1}",
    "155": "{0} - Deleting",
    "156": "{0} - Modified. {1}",
    "157": "{0} - Creating file",
    "158": "{0} - Creating symlink to {1}",
    "159": "{0} - Downloading from {1}",
    "160": "{0} - Copying {1} and modifying",
    "161": "{0} - Backup of current {1}",
    "162": "{0} - Creating directory",
    "163": "{0} - Already exists.  Left unmodified.",
    "164": "{0} - Copying {1}",
    "165": "{0} - Creating file",
    "170": "---- Environment variables ---------------------------------------------------",
    "171": "  {0} = {1}",
    "172": "  {0} defaults to {1}",
    "173": "  {0} is not set",
    "181": "{0} ip address found by method: {1}",
    "190": "---- File --------------------------------------------------------------------",
    "191": "---- Path on workstation: {0}",
    "192": "---- Path inside  docker: {0}",
    "193": "---- Contents:",
    "194": "{0}",
    "210": "---- G2Module.ini inspection -------------------------------------------------",
    "211": "G2Module.ini {0}.{1} has correct value for docker: {2}",
    "212": "G2Module.ini {0}.{1} has incorrect value for docker: {2} should be {3}",
    "213": "G2Module.ini {0}.{1} Not specified. If specified, it needs to be {2}",
    "350": "---- Warnings ----------------------------------------------------------------",
    "292": "Configuration change detected.  Old: {0} New: {1}",
    "293": "For information on warnings and errors, see https://github.com/Senzing/stream-loader#errors",
    "294": "Version: {0}  Updated: {1}",
    "295": "Sleeping infinitely.",
    "296": "Sleeping {0} seconds.",
    "297": "Enter {0}",
    "298": "Exit {0}",
    "299": "{0}",
    "300": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}W",
    "350": "---- Warnings ----------------------------------------------------------------",
    "352": "Environment variable not set: {0}",
    "499": "{0}",
    "500": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "695": "Unknown database scheme '{0}' in database url '{1}'",
    "696": "Bad SENZING_SUBCOMMAND: {0}.",
    "697": "No processing done.",
    "698": "Program terminated with error.",
    "699": "{0}",
    "700": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}E",
    "702": "Could not create '{0}' directory. Error: {1}",
    "750": "---- Errors ------------------------------------------------------------------",
    "760": "shutil.Error Cannot copy {0} to {1} Error: {2}",
    "761": "OSError: Cannot copy {0} to {1} Error: {2}",
    "885": "License has expired.",
    "886": "G2Engine.addRecord() bad return code: {0}; JSON: {1}",
    "888": "G2Engine.addRecord() G2ModuleNotInitialized: {0}; JSON: {1}",
    "889": "G2Engine.addRecord() G2ModuleGenericException: {0}; JSON: {1}",
    "890": "G2Engine.addRecord() Exception: {0}; JSON: {1}",
    "891": "Original and new database URLs do not match. Original URL: {0}; Reconstructed URL: {1}",
    "892": "Could not initialize G2Product with '{0}'. Error: {1}",
    "893": "Could not initialize G2Hasher with '{0}'. Error: {1}",
    "894": "Could not initialize G2Diagnostic with '{0}'. Error: {1}",
    "895": "Could not initialize G2Audit with '{0}'. Error: {1}",
    "896": "Could not initialize G2ConfigMgr with '{0}'. Error: {1}",
    "897": "Could not initialize G2Config with '{0}'. Error: {1}",
    "898": "Could not initialize G2Engine with '{0}'. Error: {1}",
    "899": "{0}",
    "900": "senzing-" + SENZING_PRODUCT_ID + "{0:04d}D",
    "998": "Debugging enabled.",
    "999": "{0}",
}


def message(index, *args):
    index_string = str(index)
    template = message_dictionary.get(index_string, "No message for index {0}.".format(index_string))
    return template.format(*args)


def message_generic(generic_index, index, *args):
    index_string = str(index)
    return "{0} {1}".format(message(generic_index, index), message(index, *args))


def message_info(index, *args):
    return message_generic(MESSAGE_INFO, index, *args)


def message_warning(index, *args):
    return message_generic(MESSAGE_WARN, index, *args)


def message_error(index, *args):
    return message_generic(MESSAGE_ERROR, index, *args)


def message_debug(index, *args):
    return message_generic(MESSAGE_DEBUG, index, *args)


def get_exception():
    ''' Get details about an exception. '''
    exception_type, exception_object, traceback = sys.exc_info()
    frame = traceback.tb_frame
    line_number = traceback.tb_lineno
    filename = frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_number, frame.f_globals)
    return {
        "filename": filename,
        "line_number": line_number,
        "line": line.strip(),
        "exception": exception_object,
        "type": exception_type,
        "traceback": traceback,
    }

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


def get_configuration(args):
    ''' Order of precedence: CLI, OS environment variables, INI file, default. '''
    result = {}

    # Copy default values into configuration dictionary.

    for key, value in list(configuration_locator.items()):
        result[key] = value.get('default', None)

    # "Prime the pump" with command line args. This will be done again as the last step.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace('-', '_'))
        if value:
            result[new_key] = value

    # Copy OS environment variables into configuration dictionary.

    for key, value in list(configuration_locator.items()):
        os_env_var = value.get('env', None)
        if os_env_var:
            os_env_value = os.getenv(os_env_var, None)
            if os_env_value:
                result[key] = os_env_value

    # Copy 'args' into configuration dictionary.

    for key, value in list(args.__dict__.items()):
        new_key = key.format(subcommand.replace('-', '_'))
        if value:
            result[new_key] = value

    # Special case: subcommand from command-line

    if args.subcommand:
        result['subcommand'] = args.subcommand

    # Special case: Change boolean strings to booleans.

    booleans = ['debug']
    for boolean in booleans:
        boolean_value = result.get(boolean)
        if isinstance(boolean_value, str):
            boolean_value_lower_case = boolean_value.lower()
            if boolean_value_lower_case in ['true', '1', 't', 'y', 'yes']:
                result[boolean] = True
            else:
                result[boolean] = False

    # Special case: Remove trailing /

    key = "project_dir"
    result[key] = os.path.abspath(result[key])

    # Special case: Change integer strings to integers.

    integers = [
        'sleep_time_in_seconds'
    ]
    for integer in integers:
        integer_string = result.get(integer)
        result[integer] = int(integer_string)

    return result


def validate_configuration(config):
    ''' Check aggregate configuration from commandline options, environment variables, config files, and defaults. '''

    user_warning_messages = []
    user_error_messages = []

    # Perform subcommand specific checking.

    subcommand = config.get('subcommand')

    if subcommand in ['task1', 'task2']:

        if not config.get('senzing_dir'):
            user_error_messages.append(message_error(414))

    # Log warning messages.

    for user_warning_message in user_warning_messages:
        logging.warning(user_warning_message)

    # Log error messages.

    for user_error_message in user_error_messages:
        logging.error(user_error_message)

    # Log where to go for help.

    if len(user_warning_messages) > 0 or len(user_error_messages) > 0:
        logging.info(message_info(293))

    # If there are error messages, exit.

    if len(user_error_messages) > 0:
        exit_error(697)


def redact_configuration(config):
    ''' Return a shallow copy of config with certain keys removed. '''
    result = config.copy()
    for key in keys_to_redact:
        try:
            result.pop(key)
        except:
            pass
    return result

# -----------------------------------------------------------------------------
# Database URL parsing
# -----------------------------------------------------------------------------


def xtranslate(map, astring):
    new_string = str(astring)
    for key, value in map.items():
        new_string = new_string.replace(key, value)
    return new_string


def xget_unsafe_characters(astring):
    result = []
    for unsafe_character in unsafe_character_list:
        if unsafe_character in astring:
            result.append(unsafe_character)
    return result


def xget_safe_characters(astring):
    result = []
    for safe_character in safe_character_list:
        if safe_character not in astring:
            result.append(safe_character)
    return result


def xparse_database_url(original_senzing_database_url):
    ''' Given a canonical database URL, decompose into URL components. '''

    result = {}

    # Get the value of SENZING_DATABASE_URL environment variable.

    senzing_database_url = original_senzing_database_url

    # Create lists of safe and unsafe characters.

    unsafe_characters = get_unsafe_characters(senzing_database_url)
    safe_characters = get_safe_characters(senzing_database_url)

    # Detect an error condition where there are not enough safe characters.

    if len(unsafe_characters) > len(safe_characters):
        logging.error(message_error(730, unsafe_characters, safe_characters))
        return result

    # Perform translation.
    # This makes a map of safe character mapping to unsafe characters.
    # "senzing_database_url" is modified to have only safe characters.

    translation_map = {}
    safe_characters_index = 0
    for unsafe_character in unsafe_characters:
        safe_character = safe_characters[safe_characters_index]
        safe_characters_index += 1
        translation_map[safe_character] = unsafe_character
        senzing_database_url = senzing_database_url.replace(unsafe_character, safe_character)

    # Parse "translated" URL.

    parsed = urlparse(senzing_database_url)
    schema = parsed.path.strip('/')

    # Construct result.

    result = {
        'scheme': translate(translation_map, parsed.scheme),
        'netloc': translate(translation_map, parsed.netloc),
        'path': translate(translation_map, parsed.path),
        'params': translate(translation_map, parsed.params),
        'query': translate(translation_map, parsed.query),
        'fragment': translate(translation_map, parsed.fragment),
        'username': translate(translation_map, parsed.username),
        'password': translate(translation_map, parsed.password),
        'hostname': translate(translation_map, parsed.hostname),
        'port': translate(translation_map, parsed.port),
        'schema': translate(translation_map, schema),
    }

    # For safety, compare original URL with reconstructed URL.

    url_parts = [
        result.get('scheme'),
        result.get('netloc'),
        result.get('path'),
        result.get('params'),
        result.get('query'),
        result.get('fragment'),
    ]
    test_senzing_database_url = urlunparse(url_parts)
    if test_senzing_database_url != original_senzing_database_url:
        logging.warning(message_warning(891, original_senzing_database_url, test_senzing_database_url))

    # Return result.

    return result


database_connection_formats = {
    "db2": "{scheme}://{username}:{password}@{schema}",
    "mssql": "{scheme}://{username}:{password}@{schema}",
    "mysql": "{scheme}://{username}:{password}@{hostname}:{port}/?schema={schema}",
    "postgresql": "{scheme}://{username}:{password}@{hostname}:{port}:{schema}/",
    "sqlite3": "{scheme}://{username}:{password}@{path}",
}


def parse_database_connection(senzing_database_connection):
    result = {}
    scheme = senzing_database_connection[:senzing_database_connection.index(":")]

    result = parse.parse(database_connection_formats.get(scheme, ""), senzing_database_connection)
    if not result:
        logging.error(message_error(695, "", senzing_database_connection))
    else:
        result = result.named

    assert type(result) == dict
    return result


def get_g2_database_url_raw(parsed_database_url):
    ''' Given a canonical database URL, transform to the specific URL. '''

    result = ""
    scheme = parsed_database_url.get('scheme')
    result = database_connection_formats.get(scheme, "").format(**parsed_database_url)
    if not result:
        logging.error(message_error(695, scheme, generic_database_url))

    assert type(result) == dict
    return result


def get_g2_database_url(parsed_database_connection):
    ''' Given a parsed database URL, transform to the normalized URL. '''

    result = ""
    scheme = parsed_database_connection.get('scheme')

    if scheme in ['mysql', 'postgresql', 'db2', 'mssql']:
        result = "{scheme}://{username}:{password}@{hostname}:{port}/{schema}".format(**parsed_database_connection)
    elif scheme in ['sqlite3']:
        result = "{scheme}://{username}:{password}@{path}".format(**parsed_database_connection)
    else:
        logging.error(message_error(695, scheme, parsed_database_connection))

    return result

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def bootstrap_signal_handler(signal, frame):
    sys.exit(0)


def create_signal_handler_function(args):
    ''' Tricky code.  Uses currying technique. Create a function for signal handling.
        that knows about "args".
    '''

    def result_function(signal_number, frame):
        logging.info(message_info(298, args))
        sys.exit(0)

    return result_function


def entry_template(config):
    ''' Format of entry message. '''
    debug = config.get("debug", False)
    config['start_time'] = time.time()
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(297, config_json)


def exit_template(config):
    ''' Format of exit message. '''
    debug = config.get("debug", False)
    stop_time = time.time()
    config['stop_time'] = stop_time
    config['elapsed_time'] = stop_time - config.get('start_time', stop_time)
    if debug:
        final_config = config
    else:
        final_config = redact_configuration(config)
    config_json = json.dumps(final_config, sort_keys=True)
    return message_info(298, config_json)


def exit_error(index, *args):
    ''' Log error message and exit program. '''
    logging.error(message_error(index, *args))
    logging.error(message_error(698))
    sys.exit(1)


def exit_silently():
    ''' Exit program. '''
    sys.exit(0)

# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------


def file_docker_environment_vars():
    """#! /usr/bin/env bash

# For more information about the environment variables, see
# https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md

export DATABASE_DATABASE={database_database}
export POSTGRES_DIR={project_dir}/var/postgres
export RABBITMQ_DIR={project_dir}/var/rabbitmq
export SENZING_API_SERVER_URL="http://{local_ip_addr}:8250"
export SENZING_DATABASE_URL={senzing_database_url}
export SENZING_DATA_DIR={project_dir}/data
export SENZING_DATA_VERSION_DIR={project_dir}/data
export SENZING_DOCKER_SOCKET=/var/run/docker.sock
export SENZING_ETC_DIR={project_dir}/docker-etc
export SENZING_G2_DIR={project_dir}
export SENZING_INPUT_URL="https://s3.amazonaws.com/public-read-access/TestDataSets/loadtest-dataset-1M.json"
export SENZING_LOCAL_IP_ADDR={local_ip_addr}
export SENZING_PORTAINER_DIR={project_dir}/var/portainer
export SENZING_PROJECT_DIR={project_dir}
export SENZING_RABBITMQ_PASSWORD=bitnami
export SENZING_RABBITMQ_QUEUE=senzing-rabbitmq-queue
export SENZING_RABBITMQ_USERNAME=user
export SENZING_RECORD_MAX=5000
export SENZING_SQL_CONNECTION="{sql_connection}"
export SENZING_VAR_DIR={project_dir}/var
"""
    return 0


def file_docker_pull_latest():
    """#! /usr/bin/env bash

docker pull portainer/portainer:latest
docker pull senzing/senzing-debug:latest
docker pull senzing/entity-search-web-app:latest
docker pull senzing/init-container:latest
docker pull senzing/jupyter:latest
docker pull senzing/mock-data-generator:latest
docker pull senzing/senzing-api-server:latest
docker pull senzing/stream-loader:latest
docker pull senzing/xterm:latest
"""
    return 0


def file_senzing_api_server():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest
PORT=8250

echo "senzing-api-server running on http://localhost:${PORT}"

docker run \\
  --env SENZING_DATABASE_URL=${SENZING_DATABASE_URL} \\
  --interactive \\
  --name senzing-api-server \\
  --publish ${PORT}:${PORT} \\
  --rm \\
  --tty \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/senzing-api-server:${DOCKER_IMAGE_VERSION} \\
    -httpPort ${PORT} \\
    -bindAddr all \\
    -iniFile /etc/opt/senzing/G2Module.ini \\
    -allowedOrigins "*" \\
    -enableAdmin
"""
    return 0


def file_senzing_debug():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest

docker run \\
  --cap-add=ALL \\
  --interactive \\
  --name senzing-debug \\
  --rm \\
  --tty \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/senzing-debug:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_init_container():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest

docker run \\
  --env SENZING_DATABASE_URL=${SENZING_DATABASE_URL} \\
  --name senzing-init-container \\
  --rm \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/init-container:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_jupyter():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest
PORT=9178

echo "senzing-jupyter running on http://localhost:${PORT}"

docker run \\
  --env SENZING_SQL_CONNECTION=${SENZING_SQL_CONNECTION} \\
  --interactive \\
  --name senzing-jupyter \\
  --publish ${PORT}:8888 \\
  --rm \\
  --tty \\
  --volume ${SENZING_PROJECT_DIR}:/notebooks/shared \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/jupyter:${DOCKER_IMAGE_VERSION} start.sh jupyter notebook --NotebookApp.token=''
"""
    return 0


def file_senzing_mock_data_generator():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=1.1.1

docker run \\
  --env SENZING_INPUT_URL=${SENZING_INPUT_URL} \\
  --env SENZING_RABBITMQ_HOST=${SENZING_LOCAL_IP_ADDR} \\
  --env SENZING_RABBITMQ_PASSWORD=${SENZING_RABBITMQ_PASSWORD} \\
  --env SENZING_RABBITMQ_QUEUE=${SENZING_RABBITMQ_QUEUE} \\
  --env SENZING_RABBITMQ_USERNAME=${SENZING_RABBITMQ_USERNAME} \\
  --env SENZING_RECORD_MAX=${SENZING_RECORD_MAX} \\
  --env SENZING_RECORD_MONITOR=1000 \\
  --env SENZING_SUBCOMMAND=url-to-rabbitmq \\
  --interactive \\
  --name senzing-mock-data-generator \\
  --rm \\
  --tty \\
  senzing/mock-data-generator:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_phppgadmin():
    pass


def file_senzing_postgres():
    pass


def file_senzing_postgresql_init():
    pass


def file_senzing_rabbitmq():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=3.8.2

echo "senzing-rabbitmq running on http://localhost:15672"

mkdir -p ${RABBITMQ_DIR}
chmod 777 ${RABBITMQ_DIR}

docker run \\
  --env RABBITMQ_PASSWORD=${SENZING_RABBITMQ_PASSWORD} \\
  --env RABBITMQ_USERNAME=${SENZING_RABBITMQ_USERNAME} \\
  --interactive \\
  --name senzing-rabbitmq \\
  --publish 15672:15672 \\
  --publish 5672:5672 \\
  --rm \\
  --tty \\
  --volume ${RABBITMQ_DIR}:/bitnami \\
  bitnami/rabbitmq:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_sqlite_web():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest

echo "senzing-sqlite-web running on http://localhost:9174"

docker run \\
  --env SQLITE_DATABASE=${DATABASE_DATABASE} \\
  --interactive \\
  --name senzing-sqlite-web \\
  --publish 9174:8080 \\
  --rm \\
  --tty \\
  --volume ${SENZING_VAR_DIR}/sqlite:/data \\
  coleifer/sqlite-web:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_stream_loader():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest

docker run \\
  --env LC_CTYPE="en_us.utf8" \\
  --env SENZING_DATA_SOURCE=TEST \\
  --env SENZING_DATABASE_URL=${SENZING_DATABASE_URL} \\
  --env SENZING_ENTITY_TYPE=TEST \\
  --env SENZING_RABBITMQ_HOST=${SENZING_LOCAL_IP_ADDR} \\
  --env SENZING_RABBITMQ_PASSWORD=${SENZING_RABBITMQ_PASSWORD} \\
  --env SENZING_RABBITMQ_QUEUE=${SENZING_RABBITMQ_QUEUE} \\
  --env SENZING_RABBITMQ_USERNAME=${SENZING_RABBITMQ_USERNAME} \\
  --env SENZING_SUBCOMMAND=rabbitmq \\
  --interactive \\
  --name senzing-stream-loader \\
  --rm \\
  --tty \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/stream-loader:${DOCKER_IMAGE_VERSION}
"""


def file_senzing_webapp():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest
PORT=8251

echo "senzing-webapp running on http://localhost:${PORT}"

docker run \\
  --env SENZING_API_SERVER_URL=${SENZING_API_SERVER_URL} \\
  --env SENZING_WEB_SERVER_PORT=${PORT} \\
  --interactive \\
  --name senzing-webapp \\
  --publish ${PORT}:${PORT} \\
  --rm \\
  --tty \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/entity-search-web-app:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_senzing_xterm():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest
PORT=8254

echo "senzing-xterm running on http://localhost:${PORT}"

docker run \\
  --interactive \\
  --name senzing-xterm \\
  --publish ${PORT}:5000 \\
  --rm \\
  --tty \\
  --volume ${SENZING_DATA_VERSION_DIR}:/opt/senzing/data \\
  --volume ${SENZING_ETC_DIR}:/etc/opt/senzing \\
  --volume ${SENZING_G2_DIR}:/opt/senzing/g2 \\
  --volume ${SENZING_VAR_DIR}:/var/opt/senzing \\
  senzing/xterm:${DOCKER_IMAGE_VERSION}
"""
    return 0


def file_portainer():
    """#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${SCRIPT_DIR}/docker-environment-vars.sh

DOCKER_IMAGE_VERSION=latest
PORT=9170

echo "portainer running on http://localhost:${PORT}"

sudo docker run \\
   --detach \\
   --name portainer \\
   --publish ${PORT}:9000 \\
   --restart always \\
   --volume ${SENZING_DOCKER_SOCKET}:/var/run/docker.sock \\
   --volume ${SENZING_PORTAINER_DIR}:/data \\
   portainer/portainer:${DOCKER_IMAGE_VERSION}
"""
    return 0

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def inspect_g2module_ini():

    g2module_ini_for_docker = {
        "PIPELINE" : {
            "CONFIGPATH" : "/etc/opt/senzing",
            "LICENSEFILE" : "/etc/opt/senzing/g2.lic",
            "RESOURCEPATH" : "/opt/senzing/g2/resources",
            "SUPPORTPATH" : "/opt/senzing/data",
        },
    }

    # Read G2Module.ini.

    filename = "{0}/G2Module.ini".format(os.environ.get("SENZING_ETC_DIR", "/etc/opt/senzing"))
    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str  # Maintain case of keys.
    config_parser.read(filename)

    #  Verify values.

    logging.info(message_info(210))
    for section, options in g2module_ini_for_docker.items():
        for option, docker_value in options.items():
            try:
                value = config_parser.get(section, option)
                if value == docker_value:
                    logging.info(message_info(211, section, option, value))
                else:
                    logging.info(message_info(212, section, option, value, docker_value))
                    report_warnings.append(message_warning(212, section, option, value, docker_value))
            except:
                logging.info(message_info(213, section, option, docker_value))


def log_environment_variables():

    # List variables and default values.

    environment_variables = {
        "GIT_ACCOUNT": None,
        "GIT_REPOSITORY": None,
        "GIT_ACCOUNT_DIR": None,
        "GIT_REPOSITORY_DIR": None,
        "JUPYTER_NOTEBOOKS_SHARED_DIR": "~",
        "POSTGRES_PASSWORD": "postgres",
        "POSTGRES_USERNAME": "postgres",
        "RABBITMQ_DIR": None,
        "RABBITMQ_USERNAME": "user",
        "RABBITMQ_PASSWORD": "bitnami",
        "SENZING_DATA_SOURCE": "TEST",
        "SENZING_DATA_VERSION_DIR": "/opt/senzing/data/1.0.0",
        "SENZING_ENTITY_TYPE": "TEST",
        "SENZING_ETC_DIR": "/etc/opt/senzing",
        "SENZING_G2_DIR": "/opt/senzing/g2",
        "SENZING_VAR_DIR": "/var/opt/senzing",
    }

    # Log values.

    logging.info(message_info(170))
    for key, default_value in environment_variables.items():
        environment_value = os.environ.get(key)
        if environment_value:
            logging.info(message_info(171, key, environment_value))
        elif default_value:
            logging.info(message_info(172, key, default_value))
        else:
            logging.info(message_info(173, key))
            report_warnings.append(message_warning(352, key))


def log_files():

    # List variables and default values.

    files = {
        "G2Module.ini": {
            "docker": "/etc/opt/senzing/G2Module.ini",
            "dockerHost": "{0}/G2Module.ini".format(os.environ.get("SENZING_ETC_DIR", "/etc/opt/senzing"))
        }
    }

    # Log file contents.

    for file, values in files.items():
        logging.info(message_info(190))
        logging.info(message_info(191, values.get("dockerHost")))
        logging.info(message_info(192, values.get("docker")))
        logging.info(message_info(193))
        with open(values.get("dockerHost"), "r", newline=None) as input_file:
            for input_line in input_file:
                logging.info(message_info(194, input_line.rstrip()))
    logging.info(message_info(101))


def project_copy_etc(config):

    # Pull configuration variables

    project_dir = config.get("project_dir")

    # Synthesize variables.

    host_etc = "{0}/etc".format(project_dir)
    docker_etc = "{0}/docker-etc".format(project_dir)
    docker_etc_old = "{0}/docker-etc.{1}".format(project_dir, int(time.time()))

    # If directory exists, back it up.

    if os.path.exists(docker_etc):
        logging.info(message_info(161, docker_etc_old, docker_etc))
        shutil.move(docker_etc, docker_etc_old)

    # Copy directory.

    try:
        logging.info(message_info(164, docker_etc, host_etc))
        shutil.copytree(host_etc, docker_etc)
    except shutil.Error as err:
        exit_error(760, host_etc, docker_etc, err)
    except OSError as err:
        exit_error(761, host_etc, docker_etc, err)


def project_create_setupenv_docker(config):

    # Pull configuration variables

    project_dir = config.get("project_dir")

    output_filename = "{0}/docker-setupEnv".format(project_dir)

    docstring = """#! /usr/bin/env bash
export SENZING_DATA_DIR={0}/data
export SENZING_DATA_VERSION_DIR={0}/data
export SENZING_ETC_DIR={0}/docker-etc
export SENZING_G2_DIR={0}
export SENZING_VAR_DIR={0}/var

export POSTGRES_DIR={0}/var/postgres
export RABBITMQ_DIR={0}/var/rabbitmq

mkdir -p  {0}/var/postgres
chmod 777 {0}/var/postgres

mkdir -p  {0}/var/rabbitmq
chmod 777 {0}/var/rabbitmq

""".format(project_dir)

    logging.info(message_info(165, output_filename))
    with open(output_filename, "w") as text_file:
        text_file.write(docstring)

    os.chmod(output_filename, 0o755)


def project_modify_G2Module_ini(config):

    g2module_ini_for_docker = {
        "PIPELINE" : {
            "CONFIGPATH" : "/etc/opt/senzing",
            "LICENSEFILE" : "/etc/opt/senzing/g2.lic",
            "RESOURCEPATH" : "/opt/senzing/g2/resources",
            "SUPPORTPATH" : "/opt/senzing/data",
        },
    }

    # Pull configuration variables

    project_dir = config.get("project_dir")

    # Synthesize variables.

    filename = "{0}/docker-etc/G2Module.ini".format(project_dir)

    # Read G2Module.ini.

    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str  # Maintain case of keys.
    config_parser.read(filename)

    #  Verify values.

    logging.info(message_info(102, filename))
    for section, options in g2module_ini_for_docker.items():
        for option, docker_value in options.items():
            try:
                value = config_parser.get(section, option)
                if value != docker_value:
                    config_parser[section][option] = docker_value
                    logging.info(message_info(103, section, option, value, docker_value))
                else:
                    logging.info(message_info(104, section, option, value))
            except:
                logging.info(message_info(105, section, option))

    # If needed, modify SQL.CONNECTION

    section = "SQL"
    option = "CONNECTION"
    try:
        old_database_url = config_parser.get(section, option)
        if old_database_url.find("sqlite") == 0:
            new_database_url = "sqlite3://na:na@/var/opt/senzing/sqlite/G2C.db"
            config_parser[section][option] = new_database_url
            logging.info(message_info(103, section, option, old_database_url, new_database_url))
    except:
        logging.info(message_info(105, section, option))

    # Remove SQL.G2CONFIGFILE option.

    config_parser.remove_option('SQL', 'G2CONFIGFILE')
    logging.info(message_info(106, 'SQL', 'G2CONFIGFILE'))

    # Write out contents.

    logging.info(message_info(156, filename, ""))
    with open(filename, 'w') as output_file:
        config_parser.write(output_file)


def create_bin_docker(config):

    # Pull configuration variables.

    project_dir = config.get("project_dir")

    # Map filenames to functions.

    output_files = {
        "docker-pull-latest.sh": file_docker_pull_latest,
        "senzing-api-server.sh": file_senzing_api_server,
        "senzing-debug.sh": file_senzing_debug,
        "senzing-init-container.sh": file_senzing_init_container,
        "senzing-jupyter.sh": file_senzing_jupyter,
        "senzing-mock-data-generator.sh": file_senzing_mock_data_generator,
        "senzing-rabbitmq.sh": file_senzing_rabbitmq,
        "senzing-sqlite-web.sh": file_senzing_sqlite_web,
        "senzing-stream-loader.sh": file_senzing_stream_loader,
        "senzing-webapp.sh": file_senzing_webapp,
        "senzing-xterm.sh": file_senzing_xterm
    }

    # Specify output directory and backup directory.

    output_directory = "{0}/docker-bin".format(project_dir)
    backup_directory = "{0}.{1}".format(output_directory, int(time.time()))

    # If output directory exists, back it up.

    if os.path.exists(output_directory):
        logging.info(message_info(161, backup_directory, output_directory))
        shutil.move(output_directory, backup_directory)

    # Make .../docker-bin directory.

    try:
        os.makedirs(output_directory, exist_ok=True)
    except PermissionError as err:
        exit_error(702, output_directory, err)

    # Calculate local_ip_addr.

    local_ip_addr_method = "SENZING_LOCAL_IP_ADDR"
    local_ip_addr = os.environ.get(local_ip_addr_method)
    if not local_ip_addr:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.connect(("8.8.8.8", 80))
        local_ip_addr = my_socket.getsockname()[0]
        my_socket.close()
        local_ip_addr_method = "socket.connect"
    logging.info(message_info(181, local_ip_addr, local_ip_addr_method))

    # Calculate sql_connection.

    # # FIXME:  Get path from setupEnv script
    project_config_file = "{0}/docker-etc/G2Module.ini".format(project_dir)

    # Read configuration file.

    config_parser = configparser.ConfigParser()
    config_parser.optionxform = str  # Maintain case of keys.
    config_parser.read(project_config_file)
    sql_connection = ""
    try:
        sql_connection = config_parser.get("SQL", "CONNECTION")
    except:
        pass

    # Calculate senzing_database_url.

    parsed_database_connection = parse_database_connection(sql_connection)
    senzing_database_url = get_g2_database_url(parsed_database_connection)

    print(parsed_database_connection)

    schema = parsed_database_connection.get("schema", "")
    if parsed_database_connection.get("scheme", "") == "sqlite3":
        schema = os.path.basename(parsed_database_connection.get("path", ""))

    # Create docker-environment-vars.sh

    variables = {
        "database_database": schema,
        "local_ip_addr": local_ip_addr,
        "project_dir": project_dir,
        "senzing_database_url": senzing_database_url,
        "sql_connection": sql_connection
    }

    filename = "{0}/docker-environment-vars.sh".format(output_directory)
    with open(filename, 'w') as file:
        logging.info(message_warning(165, filename))
        file.write(file_docker_environment_vars.__doc__.format(**variables))
    os.chmod(filename, 0o755)

    # Write files from function docstrings.

    for filename, function in output_files.items():
        full_filename = "{0}/{1}".format(output_directory, filename)
        if not os.path.exists(full_filename):
            logging.info(message_info(165, full_filename))
            with open(full_filename, 'w') as file:
                file.write(function.__doc__)
            os.chmod(full_filename, 0o755)
        else:
            logging.info(message_info(163, full_filename))

# -----------------------------------------------------------------------------
# do_* functions
#   Common function signature: do_XXX(args)
# -----------------------------------------------------------------------------


def do_add_docker_support(args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(args)

    # Prolog.

    logging.info(entry_template(config))

    # Do work.

    project_copy_etc(config)
    project_modify_G2Module_ini(config)
    project_create_setupenv_docker(config)
    create_bin_docker(config)

    # Epilog.

    logging.info(exit_template(config))


def do_docker_acceptance_test(args):
    ''' For use with Docker acceptance testing. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(args)

    # Prolog.

    logging.info(entry_template(config))

    # Epilog.

    logging.info(exit_template(config))


def do_docker_host(args):
    ''' Do a task. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(args)

    # Prolog.

    logging.info(entry_template(config))

    # Do work.

    log_environment_variables()
    log_files()
    inspect_g2module_ini()

    # TODO:
    # Print contents of G2Module.ini

    logging.warning(message_warning(350))
    for report_warning in report_warnings:
        logging.warning(report_warning)

    # Epilog.

    logging.info(exit_template(config))


def do_sleep(args):
    ''' Sleep.  Used for debugging. '''

    # Get context from CLI, environment variables, and ini files.

    config = get_configuration(args)

    # Prolog.

    logging.info(entry_template(config))

    # Pull values from configuration.

    sleep_time_in_seconds = config.get('sleep_time_in_seconds')

    # Sleep

    if sleep_time_in_seconds > 0:
        logging.info(message_info(296, sleep_time_in_seconds))
        time.sleep(sleep_time_in_seconds)

    else:
        sleep_time_in_seconds = 3600
        while True:
            logging.info(message_info(295))
            time.sleep(sleep_time_in_seconds)

    # Epilog.

    logging.info(exit_template(config))


def do_version(args):
    ''' Log version information. '''

    logging.info(message_info(294, __version__, __updated__))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


if __name__ == "__main__":

    # Configure logging. See https://docs.python.org/2/library/logging.html#levels

    log_level_map = {
        "notset": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "fatal": logging.FATAL,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    log_level_parameter = os.getenv("SENZING_LOG_LEVEL", "info").lower()
    log_level = log_level_map.get(log_level_parameter, logging.INFO)
    logging.basicConfig(format=log_format, level=log_level)
    logging.debug(message_debug(998))

    # Trap signals temporarily until args are parsed.

    signal.signal(signal.SIGTERM, bootstrap_signal_handler)
    signal.signal(signal.SIGINT, bootstrap_signal_handler)

    # Parse the command line arguments.

    subcommand = os.getenv("SENZING_SUBCOMMAND", None)
    parser = get_parser()
    if len(sys.argv) > 1:
        args = parser.parse_args()
        subcommand = args.subcommand
    elif subcommand:
        args = argparse.Namespace(subcommand=subcommand)
    else:
        parser.print_help()
        if len(os.getenv("SENZING_DOCKER_LAUNCHED", "")):
            subcommand = "sleep"
            args = argparse.Namespace(subcommand=subcommand)
            do_sleep(args)
        exit_silently()

    # Catch interrupts. Tricky code: Uses currying.

    signal_handler = create_signal_handler_function(args)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Transform subcommand from CLI parameter to function name string.

    subcommand_function_name = "do_{0}".format(subcommand.replace('-', '_'))

    # Test to see if function exists in the code.

    if subcommand_function_name not in globals():
        logging.warning(message_warning(696, subcommand))
        parser.print_help()
        exit_silently()

    # Tricky code for calling function based on string.

    globals()[subcommand_function_name](args)
