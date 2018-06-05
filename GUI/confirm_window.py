#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from lib.basic_window import BasicWindow


class ConfirmWindow(BasicWindow):
    def __init__(self, store, closeEvent):
        super().__init__('confirm_window', store)
        self.parentCloseEvent = closeEvent

        # Connecting buttons
        self.ui.pushButton_SaveAndExit.clicked.connect(
            self.saveAndExit)
        self.ui.pushButton_ExitNoSave.clicked.connect(
            self.exitNoSave)
        self.ui.pushButton_Cancel.clicked.connect(
            self.cancel)

    def closeEvent(self):
        self.cancel()

    def saveAndExit(self):
        pass

    def exitNoSave(self):
        pass

    def cancel(self):
        pass
