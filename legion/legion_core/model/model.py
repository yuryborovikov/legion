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
Models (base, interfaces and proxies)
"""

import logging

from interface import Interface

LOGGER = logging.getLogger('deploy')


class IMLModel(Interface):
    """
    Definition of an interface for ML model usable for the engine
    """

    @property
    def description(self):  # pragma: no cover
        """
        Get model description

        :return: None
        """
        return None

    def apply(self, input_vector):  # pragma: no cover
        """
        Apply the model to the provided input_vector

        :param input_vector: the input vector
        :return: an arbitrary JSON serializable object
        """
        pass

    @property
    def version_string(self):  # pragma: no cover
        """
        Get model version

        :return: None
        """
        return None
