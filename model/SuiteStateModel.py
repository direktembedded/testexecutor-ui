"""
Copyright (c) 2020 Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE.txt
"""
# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtCore import QAbstractListModel
from PySide2.QtCore import Qt
from PySide2.QtCore import QModelIndex
from PySide2.QtCore import QObject
from PySide2.QtCore import Slot, Signal, Property

class SuiteStateModel(QObject):
    def __init__(self):
        pass

    # move this to own class for 'state'
    @Slot()
    def on_stopstart(self):
        """
        Over-ride this as needed
        :return: If state change was affected
        """
        print("TestSuiteModel on_stopstart()")
        return True
