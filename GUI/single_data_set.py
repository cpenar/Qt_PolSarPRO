#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store, **kwargs):
        super().__init__(__name__, store, **kwargs)

        self.ui.pushButton_SaveAndExit.clicked.connect(self.saveAndExit)
        self.ui.pushButton_MainInputDir.clicked.connect(self.openFileDialog)

        if self.localconfig['inputDir']:
            self.startDir = self.localconfig['inputDir']
        else:
            self.startDir = self.localconfig['rootDir']

        self.ui.pushButton_MainInputDir.setText(self.startDir)

    def openFileDialog(self):
        try:
            chosenDirPath = QFileDialog.getExistingDirectory(
                directory=self.startDir)
            if chosenDirPath:
                self.localconfig['inputDir'] = chosenDirPath
                self.ui.pushButton_MainInputDir.setText(chosenDirPath)
        except Exception as e:
            self.logger.error('Error getting directory')
            self.logger.debug(e)
