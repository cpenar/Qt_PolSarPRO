#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import os
import sys
from os.path import abspath
import logging

from PyQt5 import uic, QtWidgets


class MainWindow():
    def __init__(self):
        # SETTING LOGGER

        level = logging.INFO
        level = logging.DEBUG

        if level <= logging.DEBUG:
            log_format = '%(levelname)s:%(thread)s:%(name)s:%(module)s:%(funcName)s: %(message)s'
        else:
            log_format = '%(levelname)s: %(message)s'

        logging.basicConfig(level=level, format=log_format)
        self.logger = logging.getLogger('main')

        # Initializing window

        self.ui = QtWidgets.QDialog()
        self.ui.open_window = self.open_window_from_menu_entry
        # env variable pointing to the root of a PolSARpro compiled version
        try:
            compiled_psp_path = os.environ["COMPILED_PSP_PATH"]
        except KeyError:
            self.logger.warning(
                "ERROR: missing environment variable COMPILED_PSP_PATH.\n"
                + "Necessary for Dev phase.\n"
                + "Set COMPILED_PSP_PATH and relaunch the app, example :\n\n"
                + "export COMPILED_PSP_PATH=/some/path/to/bleh")
            sys.exit(1)

        # Creating the state instance variable storing all the
        # datas shared between differents parts of the application
        guiDir = abspath(__file__)
        rootDir = abspath(guiDir + '/../../')

        # default config
        # TODO: should be in a config file
        self.state = {
            'logger': self.logger,
            'config': {
                'compiled_psp_path': compiled_psp_path,
                'localDir': guiDir,
                'rootDir': rootDir,
                'tempDir': rootDir + '/tmp/',
                'data_set_choosen': '',
                'rootDir': rootDir,
                'inputDir': rootDir,
                'colorMapDir': abspath(guiDir + '/ColorMap/'),
                'displaySize': {'rows': 934, 'columns': 934},
                'inputMasterDir': rootDir,
                'inputSlaveDir': rootDir,
            }
        }

        # .ui loader
        self.ui = uic.loadUi('main.ui', self.ui)

        # opening and showing the window
        self.ui.show()

        # connecting menu actions
        #self.ui.action_Single_Data_Set_Pol_SAR.triggered.connect(
            #self.open('single_data_set'))

    def open_window_from_menu_entry(self):
        window_name = self.ui.sender().objectName()
        self.logger.info('Opening window ' + window_name)
        ui = __import__(window_name)
        ui.Window(self.state)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
