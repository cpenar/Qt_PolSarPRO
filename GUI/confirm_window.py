#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from lib.basic_window import BasicWindow


class ConfirmWindow(BasicWindow):
    def __init__(self, parent):
        self.parent = parent

        super().__init__('confirm_window')

        # Saving QCloseEvent for later use
        self.savedCloseEvent = self.ui.closeEvent
        # Replace closeEvent to ignore QCloseEvent at start
        self.ui.closeEvent = self.cancel

        # Connecting buttons
        self.ui.pushButton_SaveAndExit.clicked.connect(
            self.saveAndExit)
        self.ui.pushButton_ExitNoSave.clicked.connect(
            self.exitNoSave)
        self.ui.pushButton_Cancel.clicked.connect(
            self.cancel)

    def saveAndExit(self):
        pass

    def exitNoSave(self):
        self.parent.closeEvent = self.parent.forceClose
        # Restoring normal close event
        self.ui.closeEvent = self.savedCloseEvent
        self.ui.close()

    def cancel(self):
        pass
