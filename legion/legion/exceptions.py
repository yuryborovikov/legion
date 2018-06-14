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


class MissedFileError(LegionException):
    __message__ = 'Cannot find file: {path}'
    path = str


class InvalidImageFile(LegionException):
    __message__ = '{path} is a invalid image file'
    path = str


# Invalid artifact
class NotAZipFileError(LegionException):
    __message__ = '{path} not a zip file'
    path = str


class InvalidJSONStructure(LegionException):
    __message__ = '{data} is a invalid JSON: {cause}'
    data = str
    cause = str


class RecievedErrorFromServerError(LegionException):
    __message__ = 'Server returns error message: {error_message}'
    error_message = str


class FailedToConnectError(LegionException):
    __message__ = ' Failed to connect to {url}: {cause}'
    url = str
    cause = str


class MissedFileOrDirectoryError(LegionException):
    __message__ = 'Cannot find file or directory: {path}'
    path = str


class UnknownExternalResourceTypeError(LegionException):
    __message__ = 'Unknown resource type: {path}'
    path = str


class ExternalResourceDoesNotContainProtocolError(LegionException):
    __message__ = 'External resource {path} does not contain //'
    path = str


class WrongHTTPResponseError(LegionException):
    __message__ = 'Wrong HTTP response code {code} for {url}'
    code = int
    url = str


class ModelIdIsMissedInModelBinary(LegionException):
    __message__ = 'Cannot get model id (not setted in container and not setted in arguments)'


class InvalidRegistryFormatError(LegionException):
    __message__ = 'Invalid registry format. Valid format: host:port/repository/image:tag'
    registry = str


class ModelDeploymentNotFoundAfterDeployError(LegionException):
    __message__ = 'Cannot find model deployment after deploy procedure'
    image = str


class InvalidAPIHandlerResponseError(LegionException):
    ___message__ = 'API handler returns wrong type: {type_name}'
    type_name = str


class CastFailedError(LegionException):
    __message__ = 'Failed to cast {field_name} to {target_type}: {cast_error}'
    field_name = str
    target_type = str
    cast_error = str


class UnknownParameterError(LegionException):
    __message__ = 'Unknown field {field_name} found'
    field_name = str


class RequestFieldIsMissedError(LegionException):
    __message__ = 'Request field {field_name} is missed'
    field_name = str


class AccessDeniedError(LegionException):
    ___message__ = 'Access denied'


class RequestWithWrongModelID(LegionException):
    __message__ = 'Request with wrong model id: {model_id}'
    model_id = str


class ParameterMissedError(LegionException):
    __message__ = 'Parameter {name} missed'
    name = str


class EnvironmentVariableMissedError(LegionException):
    __message__ = 'Environment variable {name} missed'
    name = str


class UnknownServingParameterError(LegionException):
    __message__ = 'Unknown serving parameter value: {value}'
    value = str


class CodeShouldBeExecutedInClusterError(LegionException):
    __message__ = 'This function should be executed in cluster'


class InvalidK8SObjectError(LegionException):
    __message__ = 'Invalid {object_type} for introspection: {cause}'
    object_type = str
    cause = str


class TemplateDoesNotUseAnyPluginError(LegionException):
    __message__ = 'Template does not use any plugin'


class CannotParseBuildNumber(LegionException):
    __message__ = 'Cannot parse build number'


class ModelIDHasNotBeenInitializedError(LegionException):
    __message__ = 'Cannot get model_id. Please set using legion.init_model(<name>)'


class WrongArgumentType(LegionException):
    __message__ = '{argument_name} have wrong type: {cause}'
    argument_name = str
    cause = str
