#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from lib.gen_window import GenWindow

class Window(GenWindow):
    def __init__(self, state):
        super().__init__(__name__, state)

        self.log_file = self.config['log_file']

        self.fp = open(self.log_file, 'r')

        self.line = ' '
        self.log2status()

    def log2status(self):
        # Repeatedly update status text from log file
        try:
            while self.line:
                self.ui.logBrowser.append(self.line.rstrip())
                print(self.line.rstrip())
                self.line = self.fp.readline()
        finally:
            QTimer.singleShot(200, self.log2status)
