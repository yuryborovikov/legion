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
import os
import threading
import typing

try:
    import uwsgi
    UWSGI_LOADED = True
except ImportError:
    UWSGI_LOADED = False


LOGGER = logging.getLogger(__name__)
STORE_DATA = {}  # type: typing.Dict[str, typing.Dict[str, typing.Any]]
UPDATE_STORAGE_SIGNAL = 15


class SharedStore:
    """
    Store for saving shared model-callback data
    """

    def __init__(self, id=None, persist=True):
        """
        Build shared store

        :param id: id of store. Should be uniqu across model
        :type id: str
        """
        super().__setattr__('_id', id)
        super().__setattr__('_persist', persist)
        LOGGER.info('Creating {!r}'.format(self))

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

        LOGGER.info('Current thread: {!r}, PID: {}, PPID: {}'.format(threading.current_thread(),
                                                                     os.getpid(),
                                                                     os.getppid()))
        LOGGER.debug('Current frame\'s globals id: {}'.format(id(current_frame.f_globals)))
        LOGGER.debug('Call stack of operation:')
        for entry in entries:
            LOGGER.debug('Call stack {}:{} ({})'.format(entry.filename, entry.lineno, entry.function))

    def _on_state_update(self, key):
        """
        Handle all key state update

        :param key: key
        :type key: str or None
        :return: None
        """
        if UWSGI_LOADED:
            LOGGER.info('Emitting signal to workers about store update')
            uwsgi.signal(UPDATE_STORAGE_SIGNAL)

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
        # Build store if it is not present
        if self._id not in STORE_DATA:
            STORE_DATA[self._id] = {}
        # Save value
        STORE_DATA[self._id][key] = value
        self._on_state_update(key)

    def __getattr__(self, item):
        """
        Get store attribute

        :param item: key
        :type item: str
        :return: Any
        """
        LOGGER.info('Retrieving key = {!r} with from {!r}'.format(item, self))
        self._print_call_stack()

        if self._id not in STORE_DATA:
            LOGGER.warning('Storage {!r} has not been initialized. Initializing'.format(self._id))
            STORE_DATA[self._id] = {}

        value = STORE_DATA[self._id][item]
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
        return '<Shared store {} #{} PID #{} PPID #{}>'.format(self._id,
                                                               id(self),
                                                               os.getpid(),
                                                               os.getppid())

    def __getstate__(self):
        """
        Serialize state for pickle process. It doesn't persist store state

        :return: dict[str, Any] -- persisted store
        """
        LOGGER.debug('Serializing store {!r}'.format(self))
        self._print_call_stack()

        return {
            'id': self._id
        }

    def __setstate__(self, state):
        """
        De-Serialize state for pickle process. It doesn't persist store state

        :param state: data, gathered from serialization process
        :type state: dict[str, Any]
        :return: None
        """
        object.__setattr__(self, '_id', state['id'])
        LOGGER.debug('De-serializing store {!r}'.format(self))
        self._print_call_stack()

    def has_key(self, key):
        """
        Check that store has key

        :param key: key
        :type key: str
        :return: bool -- is key in store or not
        """
        return self._id in STORE_DATA and key in STORE_DATA[self._id]

    @staticmethod
    def update_all_storages():
        """
        React on signal about storages syncronisation

        :return: None
        """
        LOGGER.info('Process {} have to syncronize store'.format(os.getpid()))


if UWSGI_LOADED:
    """
    Register uWSGI signal for property storage update
    """
    uwsgi.register_signal(UPDATE_STORAGE_SIGNAL, "workers", SharedStore.update_all_storages)
