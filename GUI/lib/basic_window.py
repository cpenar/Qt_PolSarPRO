#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import logging

from pprint import pformat

from PyQt5 import uic, QtWidgets, QtCore


class BasicWindow():
    def __init__(self, uiName, *args, **kwargs):
        """
        Create a Qt window from a ui file which name is passed as argument.
        Also initialise logger.
        """
        self.logger = None
        self.ui = None
        self.uiName = uiName

        self.initLogging(args, kwargs)

        self.ui = QtWidgets.QDialog()
        self.ui = uic.loadUi(uiName + '.ui', self.ui)

        # TODO: suppress Escape key closing event for Dialog window
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.cleanCloseWithEscapeKey

        self.ui.show()

    def initLogging(self, args, kwargs):
        self.logger = logging.getLogger(self.uiName)
        self.logger.info('Opening window ' + self.uiName)
        self.logger.debug(
            'With arguments :\n' +
            '    uiName=' + self.uiName + '\n\n' +
            '    *args =\n' + pformat(args) + '\n\n' +
            '    **kwargs=\n' + pformat(kwargs) + '\n\n')

    def cleanCloseWithEscapeKey(self, event):
        if event.key() != QtCore.Qt.Key_Escape:
            self.ui.savedKeyPressEvent(event)
        else:
            self.ui.close()
