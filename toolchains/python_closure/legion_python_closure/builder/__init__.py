import logging
import os
import shutil

import docker
import docker.errors
import legion
import legion.config
import legion.containers.headers
import legion.io
import legion.utils

import legion_python_closure

VALID_SERVING_WORKERS = 'uwsgi', 'gunicorn'


def build(model_class, temp_directory, base_data, args):
    serving = args.serving

    if serving not in VALID_SERVING_WORKERS:
        raise Exception('Unknown serving parameter. Should be one of %s' % (', '.join(VALID_SERVING_WORKERS),))

    # Copy additional payload from templates / docker_files / <serving>
    additional_directory = os.path.join(
        os.path.dirname(__file__), '..', 'templates', 'docker_files', serving)

    for file in os.listdir(additional_directory):
        path = os.path.join(additional_directory, file)
        if os.path.isfile(path) and file != 'Dockerfile':
            shutil.copy2(path, os.path.join(temp_directory, file))

    additional_docker_file = os.path.join(additional_directory, 'Dockerfile')
    with open(additional_docker_file, 'r') as additional_docker_file_stream:
        additional_docker_file_content = additional_docker_file_stream.read()

    data = {}

    data.update(base_data)
    data.update({
        'ADDITIONAL_DOCKER_CONTENT': additional_docker_file_content,
    })

    docker_file_content = legion.utils.render_template('Dockerfile.tmpl', data, package_name=legion_python_closure.__name__)

    with open(os.path.join(temp_directory, 'Dockerfile'), 'w') as file:
        file.write(docker_file_content)