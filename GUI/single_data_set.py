#!/usr/bin/env python3
# -*- codding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog

from lib.gen_window import GenericWindow


class Window(GenericWindow):
    def __init__(self, store):
        super().__init__(__name__, store)
        self.ui.pushButton_MainInputDir.clicked.connect(self.openFileDialog)
        self.ui.pushButton_SaveAndExit.clicked.connect(self.saveAndExit)

    def openFileDialog(self):
        try:
            chosenDirPath = QFileDialog.getExistingDirectory()
            self.localconfig['inputDir'] = chosenDirPath
            self.ui.pushButton_MainInputDir.setText(chosenDirPath)
        except Exception as e:
            self.logger.error('Error getting directory')
            self.logger.debug(e)

    def saveAndExit(self):
        self.globalStore['config'].update(self.localconfig)
        self.ui.close()
