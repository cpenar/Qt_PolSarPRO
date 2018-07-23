#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store, **kwargs):
        super().__init__(__name__, store, **kwargs)

        self.allLabels = self.ui.findChildren(QtWidgets.QLabel)

        self.ui.pushButton_SaveAndExit.clicked.connect(self.saveAndExit)
        self.ui.pushButton_OutputDir.clicked.connect(
            self.openFileDialogOutputDir)
        self.ui.pushButton_SarLeaderFile.clicked.connect(
            self.openFileDialogSarLeaderFile)
        self.ui.pushButton_CheckFiles.clicked.connect(self.checkLeaderFile)

        if self.localconfig['inputDir']:
            self.startDir = self.localconfig['inputDir']
            self.ui.label_InputDir.setText(self.startDir)
        else:
            self.startDir = self.localconfig['rootDir']

        self.ui.pushButton_OutputDir.setText(self.startDir)

    def openFileDialogOutputDir(self):
        try:
            chosenDirPath = QFileDialog.getExistingDirectory(
                directory=self.startDir)
            if chosenDirPath:
                self.localconfig['outputDir'] = chosenDirPath
                self.ui.pushButton_OutputDir.setText(chosenDirPath)
        except Exception as e:
            self.logger.error('Error getting directory')
            self.logger.exception(e)

    def openFileDialogSarLeaderFile(self):
        try:
            chosenFilePath = QFileDialog.getOpenFileName(
                directory=self.startDir)[0]
            if chosenFilePath:
                self.localconfig['sarLeaderFile'] = chosenFilePath
                self.ui.pushButton_SarLeaderFile.setText(chosenFilePath)
                self.ui.pushButton_CheckFiles.setEnabled(True)
        except:
            self.logger.error('Error getting directory')
            self.logger.exception(e)

    def checkLeaderFile(self):
        path, leaderBaseName = os.path.split(self.localconfig['sarLeaderFile'])
        leaderPrefix = 'LED-'
        trailerPrefix = 'TRL-'
        prefix_image_files = [
            'HH',
            'VH',
            'HV',
            'VV']

        commonBaseName = leaderBaseName[4:]


        # Looking for the Sar Trailer File
        trailerFileFullPath = path + '/' + trailerPrefix + commonBaseName
        try:
            os.access(trailerFileFullPath, os.R_OK)
            self.ui.label_SarTrailerFile.setText(trailerFileFullPath)
            self.localconfig['sarTrailerFile'] = trailerFileFullPath
        except Exception as e:
            self.logger.error('Cant find Sar Trailer File')
            self.logger.debug(e)
            return False

        # Looking for the IMG files
        for prefix in prefix_image_files:
            full_prefix = 'IMG-' + prefix + '-'
            imageFileFullPath = path + '/' + full_prefix + commonBaseName
            try:
                os.access(imageFileFullPath, os.R_OK)
                self.getQLabelWithName('label_' + prefix).setText(imageFileFullPath)
                self.localconfig['IMG-' + prefix] = imageFileFullPath
            except Exception as e:
                self.logger.error('Cant find Image File ' + full_prefix + commonBaseName)
                self.logger.exception(e)
                return False

    def getQLabelWithName(self, name):
        for label in self.allLabels:
            if label.objectName() == name:
                return label
