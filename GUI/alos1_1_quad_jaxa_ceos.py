#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import strftime
from pprint import pformat

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets

from lib.store_window import StoreWindow
from lib.tools import exec_psp_bin


class Window(StoreWindow):
    def __init__(self, store, **kwargs):
        super().__init__(__name__, store, **kwargs)

        # This variable is used later in getQLabelWithName
        self.allLabels = self.ui.findChildren(QtWidgets.QLabel)

        self.ui.pushButton_SaveAndExit.clicked.connect(self.saveAndExit)
        self.ui.pushButton_Cancel.clicked.connect(self.ui.close)
        self.ui.pushButton_OutputDir.clicked.connect(
            self.openFileDialogOutputDir)
        self.ui.pushButton_SarLeaderFile.clicked.connect(
            self.openFileDialogSarLeaderFile)
        self.ui.pushButton_CheckFiles.clicked.connect(self.checkLeaderFile)
        self.ui.pushButton_ReadHeaders.clicked.connect(self.readHeaders)

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
            self.logger.debug(e, exc_info=True)

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
            self.logger.debug(e, exc_info=True)

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
        if os.access(trailerFileFullPath, os.R_OK):
            self.ui.label_SarTrailerFile.setText(trailerFileFullPath)
            self.localconfig['sarTrailerFile'] = trailerFileFullPath
        else:
            self.logger.error('Cant find Sar Trailer File : ' + trailerFileFullPath)
            self.logger.debug('with localconfig value :\n' + pformat(self.localconfig, indent=4))
            return False

        # Looking for the IMG files
        for prefix in prefix_image_files:
            full_prefix = 'IMG-' + prefix + '-'
            imageFileFullPath = path + '/' + full_prefix + commonBaseName
            if os.access(imageFileFullPath, os.R_OK):
                self.getQLabelWithName('label_' + prefix).setText(imageFileFullPath)
                self.localconfig['IMG-' + prefix] = imageFileFullPath
            else:
                self.logger.error('Cant find IMG file : ' + imageFileFullPath)
                self.logger.debug('with localconfig value :\n' + pformat(self.localconfig, indent=4))
                return False

        # If everything went ok we can enabled the ReadHeaders button
        self.ui.pushButton_ReadHeaders.setEnabled(True)

    def getQLabelWithName(self, name):
        for label in self.allLabels:
            if label.objectName() == name:
                return label

    def readHeaders(self):
        exe_file = self.localconfig['compiled_psp_path'] \
            + '/Soft/bin/data_import/alos_header.exe'

        self.localconfig['alosConfigFile'] = self.localconfig['tempDir'] + '/' \
            + strftime("%Y_%m_%d_%H_%M_%S") + '_alos_config.txt'

        exe_args = [
            '-od', self.localconfig['outputDir'],
            '-ilf', self.localconfig['sarLeaderFile'],
            '-iif', self.localconfig['IMG-HH'],
            '-itf', self.localconfig['sarTrailerFile'],
            '-ocf', self.localconfig['alosConfigFile'],
        ]

        self.logger.debug('Executing :')
        self.logger.debug(exe_file)
        self.logger.debug(exe_args)
        try:
            (_, return_code) = exec_psp_bin(exe_file, exe_args)
        except Exception as e:
            self.logger.error('Error reading header')
            self.logger.debug(e, exc_info=True)

        if not (return_code is 1):
            # return should be 1 ?
            self.logger.error('Error executing alos_header.exe')
            raise Exception('Wrong return code')

        with open(self.localconfig['alosConfigFile'], 'r') as output:
            lines = output.read().splitlines()
            self.localconfig['initial_rows_number'] = lines[1]
            self.localconfig['initial_cols_number'] = lines[4]

        # remove the temp file
        os.remove(self.localconfig['alosConfigFile'])

        # update the entries
        self.ui.label_InitialRows.setText(
            self.localconfig['initial_rows_number'])
        self.ui.label_InitialCols.setText(
            self.localconfig['initial_cols_number'])
