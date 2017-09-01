#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import os
import sys
import logging
import json
from os.path import abspath
from pprint import pformat

from PyQt5 import QtWidgets

from lib.gen_window import GenWindow
from status_window import Window as StatusWindow


class MainWindow(GenWindow):
    def __init__(self):
        # Reserved attribut name
        self.ui = None
        self.logger = None
        self.status = None

        self.guiDir = abspath(__file__)
        self.rootDir = abspath(self.guiDir + '/../../')
        conffile = abspath(self.rootDir + '/config/genconf.txt')

        self.set_logger()

        # env variable pointing to the root of a PolSARpro compiled version
        try:
            compiled_psp_path = os.environ["COMPILED_PSP_PATH"]
        except KeyError:
            self.logger.warning(
                "ERROR: missing environment variable COMPILED_PSP_PATH.\n"
                + "Necessary for Dev phase.\n"
                + "Set COMPILED_PSP_PATH and relaunch the app, example :\n\n"
                + "export COMPILED_PSP_PATH=/some/path/to/PolSARpro\n")
            sys.exit(1)

        # loading default config
        try:
            with open(conffile, 'r') as fp:
                self.state = json.load(fp)
        except Exception as e:
            self.logger.exception(e)

        self.state['config']['log_file'] = self.log_file

        # Initializing window

        super().__init__('main', self.state)
        screenGeo = QtWidgets.QApplication.desktop().screenGeometry(self.ui)
        w, h = screenGeo.width(), screenGeo.height()
        self.ui.resize(w - 60, h - 60)
        self.ui.move(30, 30)

        #TODO
        # connecter tous les menuAction avec open_window_from_menu_entry
        # recursivement à partir de la QMenuBar 'menubar'
        self.connectMenuActions()

        # Status window
        self.status = StatusWindow(self.state)
        self.status.ui.resize(w - 60, h - 60)
        self.status.ui.move(30, h - 150)
    
    def set_logger(self):
        #level = logging.INFO
        level = logging.DEBUG

        if level <= logging.DEBUG:
            log_format = '%(levelname)s:%(threadName)s:%(name)s:%(module)s:%(funcName)s: %(message)s'
        else:
            log_format = '%(levelname)s:%(message)s'

        self.log_file = self.rootDir + '/log/log.txt'

        logging.basicConfig(filename=self.log_file, level=level, format=log_format)
        self.logger = logging.getLogger('MainWindow')

    def connectMenuActions(self):
        for elem in self.ui.menubar.findChildren(QtWidgets.QAction):
            #if not elem.isSeparator():
            pass

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

def start_qt_application():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_qt_application()
