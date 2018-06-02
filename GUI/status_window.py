#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5.QtCore import QTimer

from lib.gen_window import GenericWindow


class StatusWindow(GenericWindow):
    def __init__(self, store):
        super().__init__(__name__, store)

        self.log_file = self.localconfig['log_file']

        self.fp = open(self.log_file, 'r')

        self.line = ' '
        self.log2status()

    def log2status(self):
        # Repeatedly update status text from log file
        try:
            while self.line:
                self.line = self.line.rstrip()
                print(self.line)
                self.ui.logBrowser.append(self.line)
                self.line = self.fp.readline()
        finally:
            self.line = self.fp.readline()
            QTimer.singleShot(100, self.log2status)
