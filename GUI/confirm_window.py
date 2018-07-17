#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from lib.basic_window import BasicWindow


class ConfirmWindow(BasicWindow):
    def __init__(self, parent):
        self.parent = parent

        super().__init__('confirm_window')

        # Connecting buttons
        self.ui.pushButton_SaveAndExit.clicked.connect(
            self.saveAndExit)
        self.ui.pushButton_ExitNoSave.clicked.connect(
            self.exitNoSave)
        self.ui.pushButton_Cancel.clicked.connect(
            self.cancel)

    def saveAndExit(self):
        self.ui.close()
        self.parent.saveAndExit()

    def exitNoSave(self):
        self.ui.close()
        self.parent.forceClose()

    def cancel(self, event):
        self.ui.close()
