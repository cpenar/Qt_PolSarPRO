#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import os
import sys
import logging
from os.path import abspath
from pprint import pformat

from PyQt5 import QtWidgets

from lib.gen_window import GenWindow
from status_window import Window as StatusWindow


class MainWindow(GenWindow):
    def __init__(self):
        guiDir = abspath(__file__)
        rootDir = abspath(guiDir + '/../../')

        # SETTING LOGGER

        level = logging.INFO
        level = logging.DEBUG

        if level <= logging.DEBUG:
            log_format = '%(levelname)s:%(threadName)s:%(name)s:%(module)s:%(funcName)s: %(message)s'
        else:
            log_format = '%(levelname)s: %(message)s'

        log_file = rootDir + '/log/log.txt'
        open(log_file, 'w').close()
        logging.basicConfig(filename=log_file, level=level, format=log_format)
        self.logger = logging.getLogger('MainWindow')

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

        # default config
        # TODO: should be in a config file
        self.state = {
            'config': {
                'log_format': log_format,
                'log_level': level,
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

        # Initializing window

        self.ui = QtWidgets.QDialog()
        self.ui.open_window = self.open_window_from_menu_entry
        super().__init__('main', self.state)
        self.ui.move(30, 30)

        # Status window
        try:
            status = __import__('status_window')
            status.Window(self.state)
        except Exception as e:
            self.logger.error(pformat(e))
            if self.state['config']['log_level'] <= logging.DEBUG:
                self.logger.exception(e)

    def open_window_from_menu_entry(self):
        try:
            window_name = self.ui.sender().objectName()
            self.logger.info('Opening window ' + window_name)
            ui = __import__(window_name)
            ui.Window(self.state)
        except Exception as e:
            self.logger.error(pformat(e))
            if self.state['config']['log_level'] <= logging.DEBUG:
                self.logger.exception(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
