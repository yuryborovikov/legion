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
legion model export / load
"""

import sys
import tempfile

import legion
import legion.config
import legion.io
from legion.utils import send_header_to_stderr, save_file
from legion_core.model.types import ColumnInformation
import legion_core.headers

from legion_pyserve.model.model import ScipyModel


def _export(filename=None,
            apply_func=None, prepare_func=None,
            column_types=None,
            version=None, use_df=True):
    """
    Export simple Pandas based model as a bundle

    :param filename: the location to write down the model
    :type filename: str
    :param apply_func: an apply function DF->DF
    :type apply_func: func(x) -> y
    :param prepare_func: a function to prepare input DF->DF
    :type prepare_func: func(x) -> y
    :param column_types: result of deduce_param_types or prepared column information or None
    :type column_types: dict[str, :py:class:`legion.model.types.ColumnInformation`] or None
    :param use_df: use pandas DF for prepare and apply function
    :type use_df: bool
    :param version: of version
    :type version: str
    :return: :py:class:`legion.model.ScipyModel` -- model instance
    """
    if not hasattr(apply_func, '__call__'):
        raise Exception('Provided non-callable object as apply_function')

    if column_types:
        if not isinstance(column_types, dict) \
                or not column_types.keys() \
                or not isinstance(list(column_types.values())[0], ColumnInformation):
            raise Exception('Bad param_types / input_data_frame provided')

    if prepare_func is None:
        def prepare_func(input_dict):
            """
            Return input value (default prepare function)
            :param x: dict of values
            :return: dict of values
            """
            return input_dict

    file_name_has_been_deduced = False
    if filename:
        print('Warning! If you pass filename, CI tools would not work correctly', file=sys.stderr)
    else:
        filename = legion.io.deduce_model_file_name(version)
        file_name_has_been_deduced = True

    model = ScipyModel(apply_func=apply_func,
                       column_types=column_types,
                       prepare_func=prepare_func,
                       version=version,
                       use_df=use_df)

    temp_file = tempfile.mktemp('model-temp')
    with legion.io.ModelContainer(temp_file, is_write=True) as container:
        container.save(model)

    result_path = save_file(temp_file, filename)

    if file_name_has_been_deduced:
        print('Model has been saved to %s' % result_path, file=sys.stderr)

    send_header_to_stderr(legion_core.headers.MODEL_PATH, result_path)
    send_header_to_stderr(legion_core.headers.MODEL_VERSION, version)

    return model


def export_df(apply_func, input_data_frame,
              filename=None, prepare_func=None,
              version=None):
    """
    Export simple Pandas DF based model as a bundle

    :param apply_func: an apply function DF->DF
    :type apply_func: func(x) -> y
    :param input_data_frame: pandas DF
    :type input_data_frame: :py:class:`pandas.DataFrame`
    :param filename: the location to write down the model
    :type filename: strlegion.io.
    :param prepare_func: a function to prepare input DF->DF
    :type prepare_func: func(x) -> y
    :param version: of version
    :type version: str
    :return: :py:class:`legion.model.ScipyModel` -- model instance
    """
    column_types = legion.io._get_column_types(input_data_frame)
    return _export(filename, apply_func, prepare_func, column_types, version, True)


def export(apply_func, column_types,
           filename=None, prepare_func=None,
           version=None):
    """
    Export simple parameters defined model as a bundle

    :param apply_func: an apply function DF->DF
    :type apply_func: func(x) -> y
    :param column_types: result of deduce_param_types or prepared column information
    :type column_types: dict[str, :py:class:`legion.model.types.ColumnInformation`]
    :param filename: the location to write down the model
    :type filename: str
    :param prepare_func: a function to prepare input DF->DF
    :type prepare_func: func(x) -> y
    :param version: of version
    :type version: str
    :return: :py:class:`legion.model.ScipyModel` -- model instance
    """
    return _export(filename, apply_func, prepare_func, column_types, version, False)


def export_untyped(apply_func,
                   filename=None, prepare_func=None,
                   version=None):
    """
    Export simple untyped model as a bundle

    :param apply_func: an apply function DF->DF
    :type apply_func: func(x) -> y
    :param filename: the location to write down the model
    :type filename: str
    :param prepare_func: a function to prepare input DF->DF
    :type prepare_func: func(x) -> y
    :param version: of version
    :type version: str
    :return: :py:class:`legion.model.ScipyModel` -- model instance
    """
    return _export(filename, apply_func, prepare_func, None, version, False)
