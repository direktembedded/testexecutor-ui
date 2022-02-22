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
from PySide6.QtCore import Signal
from PySide6.QtCore import Property
from PySide6.QtCore import QObject


class MultiSelectDetails(QObject):

    def __init__(self, name, description, owner="default"):
        QObject.__init__(self)
        self.lock = threading.RLock()
        self._name = name
        self._owner = owner
        self._selected = False
        self._description = description

    def _set_name(self, name):
        """ Setter for name Property """
        changed = False
        with self.lock:
            if self._name != name:
                self._name = name
                changed = True
        if changed:
            self.name_changed.emit()

    def _get_name(self):
        """ Getter for name Property """
        with self.lock:
            v = self._name
        return v

    name_changed = Signal()
    name = Property(str, _get_name, _set_name, notify=name_changed)

    def _set_owner(self, owner):
        """ Setter for owner Property """
        changed = False
        with self.lock:
            if self._owner != owner:
                self._owner = owner
                changed = True
        if changed:
            self.owner_changed.emit()

    def _get_owner(self):
        """ Getter for owner Property """
        with self.lock:
            v = self._owner
        return v

    owner_changed = Signal()
    owner = Property(str, _get_owner, _set_owner, notify=owner_changed)

    def _set_description(self, description):
        """ Setter for description Property """
        changed = False
        with self.lock:
            if self._description != description:
                self._description = description
                changed = True
        if changed:
            self.description_changed.emit()

    def _get_description(self):
        """ Getter for description Property """
        with self.lock:
            v = self._description
        return v

    description_changed = Signal()
    description = Property(str, _get_description, _set_description, notify=description_changed)

    def _set_selected(self, selected):
        """ Setter for selected Property """
        changed = False
        with self.lock:
            if self._selected != selected:
                self._selected = selected
                changed = True
        if changed:
            self.selected_changed.emit()

    def _get_selected(self):
        """ Getter for selected Property """
        with self.lock:
            v = self._selected
        return v

    selected_changed = Signal()
    selected = Property(bool, _get_selected, _set_selected, notify=selected_changed)
