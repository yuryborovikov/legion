import os
import tempfile

import legion.config
import legion.containers.docker
import legion.io
from legion.utils import remove_directory
import legion_core.model.model_id
from legion.test_utils.deploying import patch_environ

from legion_pyserve.serving import pyserve


class ModelServeTestBuild:
    """
    Context manager for building and testing models with pyserve
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

        self._temp_directory = tempfile.mkdtemp()
        self._model_path = os.path.join(self._temp_directory, 'temp.model')

        self.application = None
        self.client = None

    def __enter__(self):
        """
        Enter into context

        :return: self
        """
        try:
            print('Building model file {} v {}'.format(self._model_id, self._model_version))
            legion_core.model.model_id._model_id = self._model_id
            legion_core.model.model_id._model_initialized_from_function = True
            self._model_builder(self._model_path, self._model_version)
            print('Model file has been built')

            print('Creating pyserve')
            additional_environment = {
                legion.config.REGISTER_ON_GRAFANA[0]: 'false',
                legion.config.REGISTER_ON_CONSUL[0]: 'false',
                legion.config.MODEL_ID[0]: self._model_id,
                legion.config.MODEL_FILE[0]: self._model_path
            }
            with patch_environ(additional_environment):
                self.application = pyserve.init_application(None)
                self.application.testing = True
                self.client = self.application.test_client()

            return self
        except Exception as build_exception:
            self.__exit__(exception=build_exception)

    def __exit__(self, *args, exception=None):
        """
        Exit from context with cleaning fs temp directory, temporary container and image

        :param args: list of arguements
        :return: None
        """
        print('Removing temporary directory')
        remove_directory(self._temp_directory)

        if exception:
            raise exception