#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import json
from os.path import abspath

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint

from lib.basic_window import BasicWindow
from status_window import StatusWindow


class MainWindow(BasicWindow):
    def __init__(self):
        # Reserved attribut name
        self.ui = None
        self.status = None
        self.log_file = None
        self.log_level = None
        self.store = {}

        self.guiDir = abspath(__file__)
        self.rootDir = abspath(self.guiDir + '/../../')
        self.log_file = self.rootDir + '/log/log.txt'
        conffile = abspath(self.rootDir + '/config/config.txt')

        # Initialize Store
        try:
            with open(conffile, 'r') as fp:
                self.store['config'] = json.load(fp)
        except Exception as e:
            # TODO : This is wrong, cant use logger here !!
            # still unset
            self.store['logger'].debug(e, exc_info=True)

        # Setting logger
        self.set_logger()

        self.store['config']['log_file'] = self.log_file

        # env variable pointing to the root of a PolSARpro compiled version
        try:
            self.store['config']['compiled_psp_path'] = os.environ['COMPILED_PSP_PATH']
        except KeyError:
            err_message = """ERROR: missing environment variable COMPILED_PSP_PATH.
                Necessary for development phase.
                Set COMPILED_PSP_PATH and relaunch the app, example :\n
                export COMPILED_PSP_PATH=/some/path/to/PolSARpro"""
            self.store['logger'].critical(err_message)
            print(err_message)
            sys.exit(1)

        # Initializing config variable if they are not
        if self.store['config']['tempDir'] == '':
            self.store['config']['tempDir'] = self.store['rootDir'] + '/tmp'

        # Initializing main window

        super().__init__('main', self.store)
        self.ui.closeEvent = self.closeEvent

        # Resizing to fit screen
        desktop = QApplication.desktop()
        screen = desktop.screenNumber(desktop.cursor().pos())
        screenGeo = desktop.screenGeometry(screen)
        w, h = screenGeo.width(), screenGeo.height()
        self.ui.resize(w - 60, h - 60)
        self.ui.move(screenGeo.topLeft() + QPoint(20, 20))

        # Opening Status window and resizing
        self.status = StatusWindow(self.store)
        self.status.ui.resize(w - 60, h - 60)
        self.status.ui.move(screenGeo.bottomLeft() + QPoint(20, -150))

        # Connecting all menu QActions with unique callback
        for action in self.ui.findChildren(QtWidgets.QAction):
            action.triggered.connect(self.open_window_from_menu_entry)

    def set_logger(self):
        self.log_level = self.store['config']['log_level']

        # # Dirty trick for easily
        # # changing log level during dev phase
        # # TODO: remove it

        self.log_level = logging.INFO
        #self.log_level = logging.DEBUG

        # # END # #

        if self.log_level <= logging.DEBUG:
            log_format = ('%(levelname)s:%(threadName)s:%(name)s:%(module)s:'
                          '%(funcName)s: %(message)s')
        else:
            log_format = '%(levelname)s:%(message)s'

        logging.basicConfig(
            filename=self.log_file,
            level=self.log_level,
            format=log_format)

        self.store['logger'] = logging.getLogger('main')
        # Shortcut for logger
        self.logger = self.store['logger']

    def open_window_from_menu_entry(self):
        # Unique function to dynamically manage all Qactions
        try:
            # The QAction name MUST be the exact ui file name targeted
            window_name = self.ui.sender().objectName()
            ui = __import__(window_name)
            ui.Window(self.store, parent=self)
        except Exception as e:
            if self.log_level <= logging.DEBUG:
                self.store['logger'].debug(e, exc_info=True)
            else:
                self.store['logger'].error(e)

    def closeEvent(self, event):
        self.status.closeFromMain()


def start_qt_application():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_qt_application()
