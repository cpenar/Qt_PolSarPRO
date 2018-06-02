#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from lib.gen_window import GenericWindow


class Window(GenericWindow):
    def __init__(self, store):
        super().__init__(__name__, store)
        self.ui.pushButton_MainInputDir.clicked.connect(self.openFileDialog)

    def openFileDialog(self):
        try:
            QFileDialog.getExistingDirectory()
        except Exception:
            self.logger.error('Error getting directory')
