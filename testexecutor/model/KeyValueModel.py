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

# This Python file uses the following encoding: utf-8
import threading
from PySide6.QtCore import QAbstractListModel
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Property, Signal


class KeyValue(QObject):
    def __init__(self, label, value):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._value = value
        self._label = label

    def _setvalue(self, value):
        """ Setter for value Property """
        changed = False
        with self.lock:
            if self._value != value:
                self._value = value
                changed = True
        if changed:
            self.value_changed.emit()

    def _getvalue(self):
        """ Getter for value Property """
        with self.lock:
            v = self._value
        return v

    value_changed = Signal()
    value = Property(str, _getvalue, _setvalue, notify=value_changed)

    def _setlabel(self, label):
        """ Setter for label Property """
        changed = False
        with self.lock:
            if self._label != label:
                self._label = label
                changed = True
        if changed:
            self.label_changed.emit()

    def _getlabel(self):
        """ Getter for label Property """
        with self.lock:
            l = self._label
        return l

    label_changed = Signal()
    label = Property(str, _getlabel, _setlabel, notify=label_changed)



class KeyValueModel(QAbstractListModel):

    KeyRole = Qt.UserRole + 1
    ValueRole = Qt.UserRole + 2
    PossibleValuesRole = Qt.UserRole + 3
    KeyKey = b'key'
    ValueKey = b'value'
    PossibleValuesKey = b'possibles'

    def __init__(self, parent = None, clone = None):
        QAbstractListModel.__init__(self, parent)
        self.lock = threading.RLock()
        if clone:
            self._data = clone._data
        else:
            self._data = []

    def rowCount(self, index):
        return len(self._data)

    def roleNames(self):
        return {KeyValueModel.KeyRole: KeyValueModel.KeyKey,
                KeyValueModel.PossibleValuesRole: KeyValueModel.PossibleValuesKey,
                KeyValueModel.ValueRole: KeyValueModel.ValueKey}

    def data(self, index, role=None):
        with self.lock:
            d = self._data[index.row()]
        if role == KeyValueModel.KeyRole:
            return d[KeyValueModel.KeyKey]
        elif role == KeyValueModel.ValueRole:
            return d[KeyValueModel.ValueKey]
        elif role == KeyValueModel.PossibleValuesRole:
            return d[KeyValueModel.PossibleValuesKey]
        return None

    def add(self, key, value, possibleValues=None):
        if possibleValues is None:
            possibleValues = []
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        with self.lock:
            self._data.append({KeyValueModel.KeyKey: key, KeyValueModel.ValueKey: value, KeyValueModel.PossibleValuesKey: possibleValues})
        self.endInsertRows()

    def setData(self, index, value, role=None):
        with self.lock:
            self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def setValue(self, key, value=None, label=None):
        changed = False
        for row in range(len(self._data)):
            with self.lock:
                if self._data[row][KeyValueModel.KeyKey] == key:
                    if value:
                        self._data[row][KeyValueModel.ValueKey].value = value
                    if label:
                        self._data[row][KeyValueModel.ValueKey].label = label
                    break

    def setLabel(self, key, label):
        self.setValue(key, value=None, label=label)

    def setPossibleValues(self, key, values):
        with self.lock:
            for row in range(len(self._data)):
                if self._data[row][KeyValueModel.KeyKey] == key:
                    self._data[row][KeyValueModel.PossibleValuesKey] = values
                    ix = self.index(row, 0)
                    changed = True
                    break
        if changed:
            self.dataChanged.emit(ix, ix, self.roleNames())

    def getValue(self, key):
        value = None
        for row in range(len(self._data)):
            with self.lock:
                if self._data[row][KeyValueModel.KeyKey] == key:
                    value = self._data[row][KeyValueModel.ValueKey].value
        return value

    def getValues(self):
        """
        Returns dictionary with key:value pairs as string:string. Note the label is not included.
        :return: Returns dictionary with key:value pairs
        """
        values = {}
        with self.lock:
            for row in range(len(self._data)):
                item = self._data[row]
                values[item[KeyValueModel.KeyKey]] = item[KeyValueModel.ValueKey].value
        return values

    def clearData(self):
        """
        Clear the data content, namely the values and active value.
        :return: None
        """
        for row in range(len(self._data)):
            with self.lock:
                self._data[row][KeyValueModel.ValueKey].value = ""
                self._data[row][KeyValueModel.PossibleValuesKey] = []
                ix = self.index(row, 0)
            self.dataChanged.emit(ix, ix, self.roleNames())
