#
#    Copyright 2017 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""
legion k8s functions
"""
import logging
import os
import shutil

import docker
import docker.errors
import legion
import legion.config
import legion.io
import legion.utils

LOGGER = logging.getLogger('docker')


def build_docker_client(args=None):
    """
    Create docker client

    :param args: command arguments
    :type args: :py:class:`argparse.Namespace` or None
    :return: :py:class:`docker.Client`
    """
    client = docker.from_env()
    return client


def generate_docker_labels_for_image(model_file, model_id, args):
    """
    Generate docker image labels from model file

    :param model_file: path to model file
    :type model_file: str
    :param model_id: model id
    :type model_id: str
    :param args: command arguments
    :type args: :py:class:`argparse.Namespace`
    :return: dict[str, str] of labels
    """
    with legion.io.ModelContainer(model_file, do_not_load_model=True) as container:
        base = {
            'com.epam.legion.model.id': model_id,
            'com.epam.legion.model.version': container.get('model.version', 'undefined'),
            'com.epam.legion.class': 'pyserve',
            'com.epam.legion.container_type': 'model'
        }
        for key, value in container.items():
            base['com.epam.' + key] = value

        return base


def generate_docker_labels_for_container(image):
    """
    Build container labels from image labels (copy)

    :param image: source Docker image
    :type image: :py:class:`docker.models.image.Image`
    :return: dict[str, str] of labels
    """
    return image.labels


def find_network(client, args):
    """
    Find legion network on docker host

    :param client: Docker client
    :type client: :py:class:`docker.client.DockerClient`
    :param args: command arguments
    :type args: :py:class:`argparse.Namespace`
    :return: str id of network
    """
    network_id = args.docker_network

    if network_id is None:
        LOGGER.debug('No network provided, trying to detect an active legion network')
        nets = client.networks.list()
        for network in nets:
            name = network.name
            if name.endswith('legion_root'):
                LOGGER.info('Detected network %s', name)
                network_id = network.id
                break
    else:
        if network_id not in client.networks.list():
            network_id = None

    if not network_id:
        LOGGER.error('Using empty docker network')

    return network_id


def get_stack_containers_and_images(client, network_id):
    """
    Get information about legion containers and images

    :param client: Docker client
    :type client: :py:class:`docker.client.DockerClient`
    :param network_id: docker network
    :type network_id: str
    :return: dict with lists 'services', 'models' and 'model_images'
    """
    containers = client.containers.list(True)
    containers = [c
                  for c in containers
                  if 'com.epam.legion.container_type' in c.labels
                  and (not network_id
                       or network_id in (n['NetworkID'] for n in c.attrs['NetworkSettings']['Networks'].values()))]

    images = client.images.list(filters={'label': 'com.epam.legion.container_type'})

    return {
        'services': [c for c in containers if c.labels['com.epam.legion.container_type'] == 'service'],
        'models': [c for c in containers if c.labels['com.epam.legion.container_type'] == 'model'],
        'model_images': [i for i in images if i.labels['com.epam.legion.container_type'] == 'model'],
    }
