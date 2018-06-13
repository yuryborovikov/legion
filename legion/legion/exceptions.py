#
#    Copyright 2018 EPAM Systems
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
legion exceptions
"""
from legion.utils import LegionException



class FileNotFoundError(LegionException):
    __message__ = 'Cannot find file: {path}'
    path = str


class CannotFindModelBinary(LegionException):
    __message__ = 'Cannot find model file: {path}'
    path = str


class ModelIdIsMissedInModelBinary(LegionException):
    __message__ = 'Cannot get model id (not setted in container and not setted in arguments)'


class InvalidRegistryFormat(LegionException):
    __message__ = 'Invalid registry format. Valid format: host:port/repository/image:tag'


class CannotFindModelDeploymentAfterDeploy(LegionException):
    __message__ = 'Cannot find model deployment after deploy procedure'
    image = str
