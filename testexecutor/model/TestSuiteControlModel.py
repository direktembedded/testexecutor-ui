#  Copyright 2020 Direkt, Australia
#  Copyright 2021 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import threading
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal, Property, Slot
from .selector.MultiSelectListModel import MultiSelectListModel
from testexecutor.model.selector.FilterGroupModel import FilterGroupModel


class TestSuiteControlModel(QObject):
    """
    A Test Suite Control is a model for selecting tests to be executed. The tests can be filtered.
    """

    def __init__(self, filtercallback=None, filters=None):
        """
        The suite control calls the supplied callback when a change occurs in the filters. The callback is to the
        execution test system, and should return a list of suites and associated tests, as well as a new set of
        allowed filters, given the new suites and tests.
        These will be 'merged' with the current suite and tests in the test selector.
        What the filters are and how the filters effect the list of tests is entirely up to the calling test system.
        Once the user has filtered and/or selected the tests, the getTests() method can be used by the test system
        to get the list of suites and tests to execute. If this model is used in conjunction with the TestSuiteModel
        then the test run will be seen on that associated UI.
        :param filtercallback: Callback executed when a filter item changes, including on first creation
        :param filters: A list of filter groups to be displayed
        """
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._testselector = MultiSelectListModel()
        self._filterchangedcallback = filtercallback
        self._errors = ""
        if filters:
            self._filter_changed_signal = Signal()
            self._filters = FilterGroupModel(filters, onSelectedChanged=self.on_filters_changed)

    @Slot(str, object)
    def on_filters_changed(self, name, selected):
        try:
            self._filterchangedcallback(name, selected)
        except Exception as err:
            self.errors = str(err)

    def _setfilters(self, filters):
        """ Setter for filters Property """
        changed = False
        with self.lock:
            if self._filters != filters:
                self._filters = filters
                changed = True
        if changed:
            self.filters_changed.emit()

    def _getfilters(self):
        """
        Getter for filters Property
        """
        filters = None
        with self.lock:
            filters = self._filters
        return filters

    """
    Filters is a list of possible filter controls that can be used to control the suite filtering.
    Each filter is then another list of items which are the filtering 'fields'
    """
    filters_changed = Signal()
    filters = Property(QObject, _getfilters, _setfilters, notify=filters_changed)


    def _settestselector(self, testselector):
        """ Setter for testselector Property """
        changed = False
        with self.lock:
            if self._testselector != testselector:
                self._testselector = testselector
                changed = True
        if changed:
            self.testselector_changed.emit()

    def _gettestselector(self):
        """
        Getter for testselector Property
        """
        testselector = None
        with self.lock:
            testselector = self._testselector
        return testselector

    """
    testselector is a tree of suites and associated tests which can be selected to create a subset of tests
    to be executed.
    Should be of type TreeSelectorModel
    """
    testselector_changed = Signal()
    testselector = Property(QObject, _gettestselector, _settestselector, notify=testselector_changed)

    def _seterrors(self, errors):
        """ Setter for errors Property """
        changed = False
        with self.lock:
            if self._errors != errors:
                self._errors = errors
                changed = True
        if changed:
            self.errors_changed.emit()

    def _geterrors(self):
        """
        Getter for errors Property
        """
        errors = None
        with self.lock:
            errors = self._errors
        return errors

    """
    errors is a tree of suites and associated tests which can be selected to create a subset of tests
    to be executed.
    Should be of type TreeSelectorModel
    """
    errors_changed = Signal()
    errors = Property(str, _geterrors, _seterrors, notify=errors_changed)

    def selectedItems(self):
        return self._testselector.selectedItems()
