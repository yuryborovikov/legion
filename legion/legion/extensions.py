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
Extensions (toolchains) logic for legion
"""
import pkg_resources
import pip
import importlib
import typing
from tabulate import tabulate

SEARCH_KEY = 'Classifier: '
SEARCH_VALUE = 'Legion :: Extension'
PACKAGE_CLASSIFIER = 'Legion :: Extension :: Package ::'

ToolchainInformation = typing.NamedTuple('ToolchainInformation', [
    ('package_name', str),
    ('valid_classes', list),
    ('builder', typing.Callable),
])


def get_toolchain_packages(distribution_name):
    """
    Get available package names in distributions

    :param distribution_name: name of distribution
    :type distribution_name: str
    :return: list[str] -- package names
    """
    try:
        detailed = pkg_resources.get_distribution(distribution_name)
        classifiers = detailed.get_metadata('PKG-INFO').splitlines()
        classifiers = [val[val.find(':') + 1:].strip()
                       for val in classifiers
                       if val.lower().startswith(SEARCH_KEY.lower())]
    except Exception:
        return None

    target_classifier = SEARCH_VALUE.strip().lower()
    if any(classifier.lower() == target_classifier for classifier in classifiers):
        return [val[val.rfind(':') + 1:].strip()
                for val in classifiers
                if val.lower().startswith(PACKAGE_CLASSIFIER.lower())]


def get_available_toolchain_packages():
    """
    Get list of names of available legion toolchain packages

    :return: list[str] -- names of packages
    """
    all_distributions = pip.get_installed_distributions()

    toolchain_packages = filter(None, (get_toolchain_packages(distribution.key) for distribution in all_distributions))
    return sum(toolchain_packages, [])


def get_toolchain_information(package_name):
    """
    Get toolchain information

    :param package_name: name of package
    :type package_name: str
    :return: :py:class:`legion.addons.ToolchainInformation` -- information about toolchain
    """
    try:
        package = importlib.import_module(package_name + '.info')
        if not hasattr(package, 'VALID_CLASSES'):
            raise Exception('VALID_CLASSES not found')

        return ToolchainInformation(package_name=package_name,
                                    valid_classes=getattr(package, 'VALID_CLASSES'),
                                    builder=getattr(package, 'BUILDER'))
    except Exception as import_error:
        raise Exception('{} is not valid package: {}'.format(package_name, import_error))


def search_builder_by_class(class_name):
    """
    Get builder for model class

    :param class_name: name of model class
    :return:
    """
    packages = (get_toolchain_information(package) for package in get_available_toolchain_packages())
    valid_packages = [package for package in packages if class_name in package.valid_classes]

    if not valid_packages:
        raise Exception('Cannot find valid package for class {}'.format(class_name))

    if len(valid_packages) > 1:
        raise Exception('Found to many packages for class {}: {}'
                        .format(class_name, ','.join(package.package_name for package in valid_packages)))

    return valid_packages[0].builder


def list_extensions_cmd(_):
    """
    Print list of available extensions

    :param _: command arguments
    :type _: :py:class:`argparse.Namespace`
    :return: None
    """
    packages = (get_toolchain_information(package) for package in get_available_toolchain_packages())

    print(tabulate((
        (package.package_name, ','.join(package.valid_classes))
        for package in packages
    ), headers=['Package', 'Class(es)'], tablefmt='simple'))
