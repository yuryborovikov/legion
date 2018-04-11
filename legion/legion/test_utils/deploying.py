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
deploying module
"""
import os
import tempfile
import time
from argparse import Namespace
from unittest.mock import patch

import legion.config
import legion.containers.docker
import legion.edi.deploy as deploy
import legion.io
from legion.utils import remove_directory
import legion_core.model.model_id
from legion_core.model import ModelClient


def patch_environ(values, flush_existence=False):
    """
    Patch environment with values

    :param values: new values
    :type values: dict[str, str]
    :param flush_existence: flush (clear before overwrite) or not
    :type flush_existence: bool
    :return: unittest2.mock.patch result
    """
    if flush_existence:
        new_values = values
    else:
        new_values = os.environ.copy()
        new_values.update(values)

    return patch('os.environ', new_values)


class ModelTestDeployment:
    """
    Context manager for building and testing models
    Hides build and deploy process and provides model client
    """

    def __init__(self, model_id, model_version, model_builder):
        """
        Create context

        :param model_id: id of model (uses for building model and model client)
        :type model_id: str
        :param model_version: version of model (passes to model builder)
        :param model_builder: str
        """
        self._model_id = model_id
        self._model_version = model_version
        self._model_builder = model_builder
        self._docker_client = legion.containers.docker.build_docker_client(None)

        self._temp_directory = tempfile.mkdtemp()
        self._model_path = os.path.join(self._temp_directory, 'temp.model')

        self.image = None
        self.container = None
        self.container_id = None
        self.model_port = None
        self.client = None

    def _print_container_logs(self):
        try:
            logs = self.container.logs().decode('utf-8')

            print('--- CONTAINER LOGS ---')
            print(logs)
        except Exception:
            print('Cannot get logs of container')

    def __enter__(self):
        """
        Enter into context

        :return: self
        """
        try:
            print('Building model file {} v {}'.format(self._model_id, self._model_version))
            legion_core.model.model_id.init(self._model_id)
            self._model_builder(self._model_path, self._model_version)
            print('Model file has been built')

            print('Building model image {} v {}'.format(self._model_id, self._model_version))
            args = Namespace(
                model_file=self._model_path,
                model_id=None,
                base_docker_image=None,
                docker_network=None,
                build_packages_from_source=True,
                python_package_version=None,
                python_repository=None,
                docker_image_tag=None,
                push_to_registry=None
            )
            self.image = deploy.build_model(args)
            print('Model image has been built')

            print('Deploying model {} v {}'.format(self._model_id, self._model_version))
            additional_environment = {
                legion.config.REGISTER_ON_GRAFANA[0]: 'false',
                legion.config.REGISTER_ON_CONSUL[0]: 'false',
            }
            with patch_environ(additional_environment):
                args = Namespace(
                    model_id=self._model_id,
                    docker_image=None,
                    docker_network=None,
                    grafana_server=None,
                    grafana_user=None,
                    grafana_password=None,
                    expose_model_port=0
                )
                self.container = deploy.deploy_model(args)
                self.container_id = self.container.id
            print('Model image has been deployed')

            wait = 3
            print('Waiting {} sec'.format(wait))
            time.sleep(wait)
            self.container = self._docker_client.containers.get(self.container_id)
            if self.container.status != 'running':
                self._print_container_logs()

                raise Exception('Invalid container state: {}'.format(self.container.status))
            print('OK')

            print('Detecting bound ports')
            ports_information = [item for sublist in self.container.attrs['NetworkSettings']['Ports'].values()
                                 for item in sublist]
            ports_information = [int(x['HostPort']) for x in ports_information]
            print('Detected ports: {}'.format(', '.join(str(port) for port in ports_information)))

            if len(ports_information) != 1:
                raise Exception('Should be only one bound port')
            self.model_port = ports_information[0]
            print('Model port: {}'.format(self.model_port))

            print('Building client')
            url = 'http://{}:{}'.format('localhost', self.model_port)
            print('Target URI is {}'.format(url))
            self.client = ModelClient(self._model_id, url)

            print('Getting model information')
            self.model_information = self.client.info()

            return self
        except Exception as build_exception:
            self.__exit__(build_exception)

    def __exit__(self, *args):
        """
        Exit from context with cleaning fs temp directory, temporary container and image

        :param args: list of arguements
        :return: None
        """
        print('Removing temporary directory')
        remove_directory(self._temp_directory)

        self._print_container_logs()

        if self.container:
            try:
                print('Finding container')
                container = self._docker_client.containers.get(self.container.id)
                print('Stopping container')
                container.stop()
                print('Removing container')
                container.remove()
            except Exception as removing_exception:
                print('Cannot remove container: {}'.format(removing_exception))

        if self.image:
            try:
                print('Removing image')
                self._docker_client.images.remove(self.image.id)
            except Exception as removing_exception:
                print('Cannot remove image: {}'.format(removing_exception))

        if args[0]:
            raise args[0]
