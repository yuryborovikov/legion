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
packaging module
"""
import os
import glob
from setuptools import sandbox


def find_directory_with_setup_py(module):
    """
    Find directory with setup.py file

    :param module: python module
    :return: str or None -- path to directory with setup.py if present
    """
    file = module.__file__
    directory = os.path.abspath(os.path.dirname(file))

    for i in range(1000):
        setup_py = os.path.join(directory, 'setup.py')

        if os.path.exists(setup_py):
            return directory

        new_directory = os.path.abspath(os.path.join(directory, os.path.pardir))
        if new_directory == directory:
            return False

        directory = new_directory

    return False


def get_latest_distribution(setup_py_directory):
    """
    Get path to latest distribution file

    :param setup_py_directory: directory with setup.py
    :type setup_py_directory: str
    :return: str -- path to file
    """
    dist_dir = os.path.abspath(os.path.join(setup_py_directory, 'dist'))
    if not os.path.exists(dist_dir):
        raise Exception('Cannot find dist dir: %s' % dist_dir)

    list_of_files = glob.glob('%s/*.whl' % (dist_dir,))
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def build_module_distribution(module):
    """
    Build module wheel

    :param module: python module
    :return: str -- path to wheel
    """
    setup_py_directory = find_directory_with_setup_py(module)

    if not setup_py_directory:
        raise Exception('Cannot find directory with setup.py for module {}'.format(module))

    setup_py = os.path.join(setup_py_directory, 'setup.py')
    sandbox.run_setup(setup_py, ['clean', 'bdist_wheel'])

    return get_latest_distribution(setup_py_directory)
