"""

An object which provides filtering information.
Each filter has
 - a list of allowable filter items
 - a list of active filter items

Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""

import threading
from PySide6.QtCore import QObject
from PySide6.QtCore import QStringListModel, QAbstractListModel, Qt, QModelIndex
from PySide6.QtCore import Signal, Property, Slot

"""
class SelectionList(QStringListModel):
    def __init__(self):
        QStringListModel.__init__(self)

    @Slot(str)
    def prepend(self, data):
        print("prepend", data)
        if self.insertRow(0):
            index = self.index(0)
            self.setData(index, data)
"""

class ItemList(QAbstractListModel):

    ItemRole = Qt.UserRole
    ItemKey = b"item"

    _roles = {
              ItemRole: ItemKey
             }

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._datas = []

    def addData(self, data):
        index = QModelIndex()
        self.beginInsertRows(index, self.rowCount(), self.rowCount())
        self._datas.append(data)
        self.endInsertRows()

    def setData(self, index, value, role):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return False
        if role == self.ItemRole:
            self._datas[index.row()] = value
            self.dataChanged.emit(index, index, {self.ItemRole: self.ItemKey})
        return True

    def rowCount(self, parent=QModelIndex()):
        return len(self._datas)

    def data(self, index, role=Qt.DisplayRole):
        try:
            data = self._datas[index.row()]
        except IndexError:
            return None

        if role == self.ItemRole:
            return data

        return None

    def roleNames(self):
        return self._roles

    def getItems(self):
        """
        Returns dictionary with key:value pairs as string:string. Note the label is not included.
        :return: Returns dictionary with key:value pairs
        """
        values = []
        for row in range(len(self._datas)):
            item = self._datas[row]
            values.append(item)
        return values

    def updateItems(self, content_list):
        """
        Update the items to match data, ensuring we remove and add rather than dump the whole set and replace.
        :param data: the new content to be added
        :return:
        """
        rowCount = self.rowCount()
        alreadyPresent = []
        for i in range(rowCount):
            existingItem = self.index(i, 0).data(self.ItemRole)
            if existingItem not in content_list:
                self.beginRemoveRows(QModelIndex(), i, i)
                self.removeRow(i)
                self.endRemoveRows()
            elif existingItem in content_list:
                alreadyPresent.append(existingItem)
        for item in content_list:
            if item not in alreadyPresent:
                row = self.rowCount()
                self.beginInsertRows(QModelIndex(), row, row)
                self.addData(item)
                self.endInsertRows()

    @Slot(str)
    def prepend(self, data):
        index = QModelIndex()
        self.beginInsertRows(index, 0, 0)
        self._datas.insert(0, data)
        self.endInsertRows()
        self.changed.emit()

    @Slot(int)
    def remove(self, i):
        index = QModelIndex()
        self.beginRemoveRows(index, i, i)
        del self._datas[i]
        self.endRemoveRows()
        self.changed.emit()

    changed = Signal()


class FilterModel(QObject):
    
    def __init__(self, name=None, allowable=[]):
        QObject.__init__(self)
        #self._proposed = QStringListModel()
        #self._proposed.setStringList(allowable)
        self._proposed = ItemList()
        for item in allowable:
            self._proposed.prepend(item)
        self._selected = ItemList()
        self._selected.changed.connect(self._onSelectedChanged, Qt.QueuedConnection)
        self._name = name
        self.lock = threading.RLock()

    def _setproposed(self, proposed):
        """ Setter for proposed Property """
        changed = False
        with self.lock:
            if self._proposed != proposed:
                self._proposed = proposed
                changed = True
        if changed:
            self.proposed_changed.emit()

    def _getproposed(self):
        """
        Getter for proposed Property
        """
        proposed = None
        with self.lock:
            proposed = self._proposed
        return proposed

    """
    proposed is a list of possible filter values that can be used to control the suite filtering.
    """
    proposed_changed = Signal()
    proposed = Property(QObject, _getproposed, _setproposed, notify=proposed_changed)
    
    def _setselected(self, selected):
        """ Setter for selected Property """
        changed = False
        with self.lock:
            if self._selected != selected:
                self._selected = selected
                changed = True
        if changed:
            self.selected_changed.emit()

    def _getselected(self):
        """
        Getter for selected Property
        """
        selected = None
        with self.lock:
            selected = self._selected
        return selected

    """
    selected is a list of chosen filter values
    """
    selected_changed = Signal()
    selected = Property(QObject, _getselected, _setselected, notify=selected_changed)

    @Slot(str, object)
    def _onSelectedChanged(self):
        self.updated_selected.emit(self.name, self.selected)

    updated_selected = Signal(str, QObject)

    def _setname(self, name):
        """ Setter for name Property """
        changed = False
        with self.lock:
            if self._name != name:
                self._name = name
                changed = True
        if changed:
            self.name_changed.emit()

    def _getname(self):
        """
        Getter for name Property
        """
        name = None
        with self.lock:
            name = self._name
        return name

    """
    name is a list of chosen filter values
    """
    name_changed = Signal()
    name = Property(str, _getname, _setname, notify=name_changed)
