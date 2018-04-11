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
legion_core utils functional
"""

import re
import sys


def normalize_name(name):
    """
    Normalize name

    :param name: name to normalize
    :type name: str
    :return: str -- normalized name
    """
    for char in ' ', '_', '+':
        name = name.replace(char, '-')
    return re.sub('[^a-zA-Z0-9\-\.]', '', name)


def send_header_to_stderr(header, value):
    """
    Send header with specific prefix to stderr

    :param header: name of header (without common prefix)
    :type header: str
    :param value: value of header
    :type value: str
    :return: None
    """
    message = 'X-Legion-%s:%s' % (header, value)
    print(message, file=sys.__stderr__, flush=True)
