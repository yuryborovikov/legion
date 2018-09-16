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
import sys
import time
import threading
import typing

import dill

LOGGER = logging.getLogger(__name__)

STORE_DATA = {}  # type: typing.Dict[str, typing.Dict[str, typing.Any]]
LAST_SYNC_DATE_TIME = 0

STORE_DUMP_LOCATION = '/app/store'
UPDATE_DATA_SIGNAL = 22

TIME_MARKER_PAGE_ID = 0
TIME_MARKER_OFFSET = 0
TIME_MARKER_SYNC_TIME = 2  # in seconds

try:
    import uwsgi
    IN_UWSGI_CONTEXT = True
    LOGGER.info('System now in uWSGI context')
except ImportError:
    IN_UWSGI_CONTEXT = False
    LOGGER.info('System now not in uWSGI context')


class SharedStore:
    """
    Store for saving shared model-callback data
    """

    def __init__(self, store_id=None):
        """
        Build shared store

        :param store_id: id of store. Should be uniqu across model
        :type store_id: str
        """
        super().__setattr__('_id', store_id)
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
        try:
            # Dumping data
            LOGGER.info('Dumping data to {}'.format(STORE_DUMP_LOCATION))
            with open(STORE_DUMP_LOCATION, 'wb') as file:
                dill.dump(STORE_DATA, file)

            # Syncing time marker
            try:
                global LAST_SYNC_DATE_TIME
                LAST_SYNC_DATE_TIME = int(time.time())
                LOGGER.info('Setting global store to new time: {!r}'.format(LAST_SYNC_DATE_TIME))
                uwsgi.sharedarea_write32(TIME_MARKER_PAGE_ID, TIME_MARKER_OFFSET, LAST_SYNC_DATE_TIME)
            except Exception as write_date_exc:
                LOGGER.error('Cannot update shared store time: {}'.format(write_date_exc))
        except Exception as dumping_exception:
            LOGGER.error('Cannot dump state to {}:{}'.format(STORE_DUMP_LOCATION, dumping_exception))

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

        LOGGER.info('Checking value before notification')
        if value is not None and IN_UWSGI_CONTEXT:
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


def update_signal_handler(sig):
    """
    Handle timer signal: check shared variable and import data if shared variable greater then local

    :param sig: id of signal
    :type sig: int
    :return: None
    """
    global LAST_SYNC_DATE_TIME

    try:
        time_val = uwsgi.sharedarea_read32(TIME_MARKER_PAGE_ID, TIME_MARKER_OFFSET)
        if time_val and time_val != LAST_SYNC_DATE_TIME:
            LOGGER.info('Updating due to getting new time marker = {!r} (old is {!r}). PID: {}'
                        .format(time_val, LAST_SYNC_DATE_TIME, os.getpid()))
            LAST_SYNC_DATE_TIME = time_val

            LOGGER.debug('Trying to open exchange file')

            with open(STORE_DUMP_LOCATION, 'rb') as file:
                global STORE_DATA
                STORE_DATA = dill.load(file)
                LOGGER.debug('New data is {!r}'.format(STORE_DATA))

            LOGGER.info('Data has been updated')
    except Exception as sync_exception:
        LOGGER.exception('Cannot sync data: {}'.format(sync_exception), exc_info=sync_exception)


if IN_UWSGI_CONTEXT:
    uwsgi.register_signal(UPDATE_DATA_SIGNAL, 'workers', update_signal_handler)
    uwsgi.add_timer(UPDATE_DATA_SIGNAL, TIME_MARKER_SYNC_TIME)
    LOGGER.info('Signal handler and timer have been registered on PID {}'.format(os.getpid()))
else:
    LOGGER.debug('Registration of signal handler and creation of time have been skipped')
