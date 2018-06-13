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

import legion.utils


class PlainExceptionWithoutMessage(legion.utils.LegionException):
    pass


class PlainExceptionWithMessage(legion.utils.LegionException):
    __message__ = 'Test message'


class ExceptionWithoutMessageAndArguments(legion.utils.LegionException):
    a = int


class ExceptionWithMessageAndArgument(legion.utils.LegionException):
    __message__ = 'Test message with a={a}'
    a = int


class ExceptionWithMessageAndArguments(legion.utils.LegionException):
    __message__ = 'Test message with a={a} and b={b}'
    a = int
    b = float


class TestExceptionSystem(unittest2.TestCase):
    def test_plain_exception_positive(self):
        exception = PlainExceptionWithMessage()

        self.assertEqual('PlainExceptionWithMessage', exception.name)
        self.assertEqual('Test message', str(exception))
        self.assertEqual('PlainExceptionWithMessage()', repr(exception))

    def test_plain_exception_traceback_positive(self):
        with self.assertRaises(PlainExceptionWithoutMessage) as exception:
            raise PlainExceptionWithoutMessage()

        serialized = exception.exception.serialize()
        self.assertIn('traceback', serialized.keys())
        self.assertIsInstance(serialized['traceback'], list, 'traceback object is not a list')
        self.assertGreater(len(serialized['traceback']), 0, 'traceback list is empty')
        self.assertIsInstance(serialized['traceback'][0], str, 'traceback list item not a string')
        self.assertGreater(len(serialized['traceback'][0]), 0, 'traceback list item is empty string')

    def test_plain_exception_serialization_keys_positive(self):
        arguments = {
            'a': 10
        }
        exception = ExceptionWithoutMessageAndArguments(**arguments)

        serialized = exception.serialize()
        self.assertIn('name', serialized.keys())
        self.assertEqual('ExceptionWithoutMessageAndArguments', serialized['name'])
        self.assertIn('arguments', serialized.keys())
        self.assertDictEqual(arguments, serialized['arguments'])
        self.assertIn('module', serialized.keys())
        self.assertEqual(self.__class__.__module__, serialized['module'])
        self.assertIn('message', serialized.keys())
        self.assertEqual('ExceptionWithoutMessageAndArguments', serialized['message'])
        self.assertIn('traceback', serialized.keys())
        self.assertIsNone(serialized['traceback'])

    def test_exception_without_message_and_argument_positive(self):
        arguments = {
            'a': 10
        }
        exception = ExceptionWithoutMessageAndArguments(**arguments)

        self.assertEqual('ExceptionWithoutMessageAndArguments', exception.name)
        self.assertEqual('ExceptionWithoutMessageAndArguments', str(exception))
        self.assertEqual('ExceptionWithoutMessageAndArguments(a={a})'.format(**arguments), repr(exception))

    def test_exception_with_message_and_argument_positive(self):
        arguments = {
            'a': 10
        }

        exception = ExceptionWithMessageAndArgument(**arguments)

        self.assertEqual('ExceptionWithMessageAndArgument', exception.name)
        self.assertEqual('Test message with a={a}'.format(**arguments), str(exception))
        self.assertEqual('ExceptionWithMessageAndArgument(a={a})'.format(**arguments), repr(exception))

        serialized = exception.serialize()
        self.assertEqual('ExceptionWithMessageAndArgument', serialized['name'])
        self.assertDictEqual(arguments, serialized['arguments'])

    def test_exception_with_message_and_arguments_messages_equal(self):
        arguments = {
            'a': 10,
            'b': 25.0
        }

        exception = ExceptionWithMessageAndArguments(**arguments)

        self.assertEqual('ExceptionWithMessageAndArguments', exception.name)

        self.assertEqual('Test message with a={a} and b={b}'.format(**arguments), str(exception))
        self.assertEqual('Test message with a={a} and b={b}'.format(**arguments), exception.message)

    def test_exception_with_message_and_arguments_positive(self):
        arguments = {
            'a': 10,
            'b': 25.0
        }

        exception = ExceptionWithMessageAndArguments(**arguments)

        self.assertEqual('ExceptionWithMessageAndArguments', exception.name)

        self.assertEqual('Test message with a={a} and b={b}'.format(**arguments), str(exception))

        serialized = exception.serialize()
        self.assertEqual('ExceptionWithMessageAndArguments', serialized['name'])
        self.assertDictEqual(arguments, serialized['arguments'])

    def test_exception_with_message_and_arguments_negative_missed_key(self):
        arguments = {
            'a': 10
        }

        with self.assertRaises(legion.utils.MissedExceptionArguments) as exception:
            ExceptionWithMessageAndArguments(**arguments)

        self.assertEqual(exception.exception.message,
                         "Arguments ['b'] are missing for exception class ExceptionWithMessageAndArguments")

    def test_exception_with_message_and_arguments_negative_unknown_key(self):
        arguments = {
            'a': 10,
            'b': 25.0,
            'c': 'oops!'
        }

        with self.assertRaises(legion.utils.UnknownExceptionArguments) as exception:
            ExceptionWithMessageAndArguments(**arguments)

        self.assertEqual(exception.exception.message,
                         "Arguments ['c'] unknown for exception class ExceptionWithMessageAndArguments")


if __name__ == '__main__':
    unittest2.main()
