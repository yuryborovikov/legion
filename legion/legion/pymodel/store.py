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
Model shared store (for using with callbacks)
"""
import logging
import inspect
import threading


LOGGER = logging.getLogger(__name__)


class SharedStore:
    """
    Store for saving shared model-callback data
    """

    def __init__(self):
        """
        Build shared store
        """
        LOGGER.info('Creating {!r}'.format(self))
        super().__setattr__('_store', {})

    def _print_call_stack(self):
        """
        Log current call stack

        :return: None
        """
        current_frame = inspect.currentframe()
        if not current_frame:
            return
        entries = inspect.getouterframes(current_frame)
        if len(entries) > 2:
            entries = entries[2:]

        LOGGER.debug('Current thread: {!r}'.format(threading.current_thread()))
        LOGGER.debug('Current frame\'s globals id: {}'.format(id(current_frame.f_globals)))
        LOGGER.debug('Call stack of operation:')
        for entry in entries:
            LOGGER.debug('Call stack {}:{} ({})'.format(entry.filename, entry.lineno, entry.function))

    def __setattr__(self, key, value):
        """
        Set store attribute

        :param key: key
        :type key: str
        :param value: value
        :type value: Any
        :return: None
        """
        LOGGER.info('Setting key = {!r} to value (id: {}) in {!r}'.format(key, id(value), self))
        self._print_call_stack()
        self._store[key] = value

    def __getattr__(self, item):
        """
        Get store attribute

        :param item: key
        :type item: str
        :return: Any
        """
        LOGGER.info('Retrieving key = {!r} with from {!r}'.format(item, self))
        self._print_call_stack()
        value = self._store[item]
        LOGGER.info('Id of key {!r} value is {}'.format(item, id(value)))
        return value

    def __delattr__(self, item):
        """
        Delete item from shared store. Raises Exception

        :param item: name of item
        :type item: str
        :return: None
        """
        raise Exception('Attribute in shared store can not be deleted')

    def __repr__(self):
        """
        Get string representation of store

        :return: str -- string representation of store
        """
        return '<Shared store #{}>'.format(id(self))
