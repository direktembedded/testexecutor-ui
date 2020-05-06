"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QObject
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import Property, Signal


class KeyValue(QObject):
    def __init__(self, label, value):
        QObject.__init__(self)
        self._value = value
        self._label = label

    def _setvalue(self, value):
        """ Setter for value Property """
        if self._value != value:
            self._value = value
            self.value_changed.emit()

    def _getvalue(self):
        """ Getter for value Property """
        return self._value

    value_changed = Signal()
    value = Property(str, _getvalue, _setvalue, notify=value_changed)

    def _setlabel(self, label):
        """ Setter for label Property """
        if self._label != label:
            self._label = label
            self.label_changed.emit()

    def _getlabel(self):
        """ Getter for label Property """
        return self._label

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

    def data(self, index, role):
        d = self._data[index.row()]
        if role == KeyValueModel.KeyRole:
            return d[KeyValueModel.KeyKey]
        elif role == KeyValueModel.ValueRole:
            return d[KeyValueModel.ValueKey]
        elif role == KeyValueModel.PossibleValuesRole:
            return d[KeyValueModel.PossibleValuesKey]
        return None

    def add(self, key, value, possibleValues=[]):
        rowCount = self.rowCount(QModelIndex())
        self.beginInsertRows(QModelIndex(), rowCount, rowCount)
        self._data.append({KeyValueModel.KeyKey: key, KeyValueModel.ValueKey: value, KeyValueModel.PossibleValuesKey: possibleValues})
        self.endInsertRows()

    def setData(self, index, value, role=None):
        self._data[index.row()] = value
        self.dataChanged.emit(index, index, self.roleNames())

    def setValue(self, key, value):
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                self._data[row][KeyValueModel.ValueKey].value = value
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break

    def setPossibleValues(self, key, values):
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                self._data[row][KeyValueModel.PossibleValuesKey] = values
                ix = self.index(row, 0)
                self.dataChanged.emit(ix, ix, self.roleNames())
                break

    def getValue(self, key):
        value = None
        for row in range(len(self._data)):
            if self._data[row][KeyValueModel.KeyKey] == key:
                value = self._data[row][KeyValueModel.ValueKey].value
        return value

    def clearData(self):
        """
        Clear the data content, namely the values and active value.
        :return: None
        """
        for row in range(len(self._data)):
            self._data[row][KeyValueModel.ValueKey].value = ""
            self._data[row][KeyValueModel.PossibleValuesKey] = []
            ix = self.index(row, 0)
            self.dataChanged.emit(ix, ix, self.roleNames())
