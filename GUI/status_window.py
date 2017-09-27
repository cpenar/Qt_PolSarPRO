#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5 import QtWidgets

from lib.gen_window import GenWindow

class Window(GenWindow):
    def __init__(self, state, image=None):
        self.ui = QtWidgets.QDialog()
        super().__init__(__name__, state)
