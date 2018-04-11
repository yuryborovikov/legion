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
from __future__ import print_function

import unittest2
from legion.extensions import get_available_toolchain_packages, get_toolchain_information

import legion_pyserve.info

PACKAGE_NAME = 'legion_pyserve'


class TestAddon(unittest2.TestCase):
    def test_addon_available(self):
        packages = get_available_toolchain_packages()
        print('Found packages: {}'.format(','.join(packages)))
        self.assertTrue(PACKAGE_NAME in packages)

        package_detail = get_toolchain_information(PACKAGE_NAME)
        self.assertEqual(package_detail.package_name, PACKAGE_NAME)
        self.assertTupleEqual(package_detail.valid_classes, legion_pyserve.info.VALID_CLASSES)


if __name__ == '__main__':
    unittest2.main()
