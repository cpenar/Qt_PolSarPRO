#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
import logging
import json

from pprint import pformat

from PyQt5 import uic, QtWidgets, QtCore


class GenericWindow():
    def __init__(self, uiName, store, *args, **kwargs):
        self.logger = None
        self.ui = None
        self.uiName = uiName

        self.globalStore = store
        self.localconfig = copy.deepcopy(store['config'])

        self.initLogging(args, kwargs)

        self.ui = QtWidgets.QDialog()
        self.ui = uic.loadUi(uiName + '.ui', self.ui)

        # TODO: suppress Escape key closing event for Dialog window
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        # self.ui.keyPressEvent = self.dontCloseWithEscapeKey

        self.ui.closeEvent = self.closeEvent
        self.ui.show()

    def initLogging(self, args, kwargs):
        self.logger = logging.getLogger(self.uiName)
        self.logger.info('Opening window ' + self.uiName)
        self.logger.debug(
            'With arguments :\n' +
            '    uiName=' + self.uiName + '\n' +
            '    *args =' + pformat(args) + '\n' +
            '    **kwargs=' + pformat(kwargs) + '\n' +
            '    config=' + '\n' + pformat(self.localconfig))

    def closeEvent(self, event):
        # TODO: verify that localconfig doesnt differ with global Config
        # before closing
        self.logger.info('Closing window ' + self.uiName)

    def dontCloseWithEscapeKey(self, event):
        if event.key() != QtCore.Qt.Key_Escape:
            self.ui.savedKeyPressEvent(event)

    def saveAndExit(self):
        self.logger.info('Saving configuration')
        try:
            self.globalStore['config'].update(self.localconfig)
            # TODO: dont save to file every time,
            # only when closing PSP
            conffile = self.localconfig['rootDir'] + '/config/default.conf.txt'
            with open(conffile, 'w') as f:
                json.dump(self.localconfig, f, indent=4)
        except Exception as e:
            self.logger.error('Error when saving configuration')
            self.logger.debug(e)
        self.ui.close()
