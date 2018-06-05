#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store):
        super().__init__(__name__, store)
        self.ui.pushButton_MainInputDir.clicked.connect(self.openFileDialog)
        self.ui.pushButton_SaveAndExit.clicked.connect(self.saveAndExit)

        if self.localconfig['inputDir']:
            self.ui.pushButton_MainInputDir.setText(
                    self.localconfig['inputDir'])
        else:
            self.ui.pushButton_MainInputDir.setText(
                    self.localconfig['rootDir'])

    def openFileDialog(self):
        try:
            chosenDirPath = QFileDialog.getExistingDirectory()
            self.localconfig['inputDir'] = chosenDirPath
            self.ui.pushButton_MainInputDir.setText(chosenDirPath)
        except Exception as e:
            self.logger.error('Error getting directory')
            self.logger.debug(e)
