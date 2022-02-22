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

"""
A class based on GenericListModel for use in a list with selected and owner as a properties.
Where owner can be used as the listview section and selected used to define an item is selected or not.
These properties can be accessed within qml models through model.item.<property_name>
"""

from PySide6.QtCore import Slot
from ..GenericListModel import GenericListModel
from .MultiSelectDetails import MultiSelectDetails


class MultiSelectListModel(GenericListModel):

    def __init__(self, parent=None):
        GenericListModel.__init__(self, parent)

    @Slot(str, result=int)
    def selected_count(self, owner):
        count = 0
        for item in self._data:
            if item.selected and item.owner == owner:
                count = count + 1
        return count

    def appendChild(self, name, description, owner):
        child = MultiSelectDetails(name, description, owner)
        self.add(child)

    def selectedItems(self):
        selected_items = []
        for item in self._data:
            if item.selected:
                selected_items.append(item)
        return selected_items
