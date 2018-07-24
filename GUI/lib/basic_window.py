#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

        # Key press event management to intercept Esc key
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.cleanCloseWithEscapeKey

        self.ui.show()

    def initLogging(self, args, kwargs):
        debugmsg = ('with arguments :\n    uiName=' + self.uiName)

        if args:
            debugmsg += '\n\n    *args =\n' + pformat(args) + '\n'
        if kwargs:
            debugmsg += '\n\n    **kwargs = \n' + pformat(kwargs) + '\n'

        self.logger = logging.getLogger(self.uiName)
        self.logger.info('Opening window ' + self.uiName)
        self.logger.debug(debugmsg)

    def cleanCloseWithEscapeKey(self, event):
        # Intercept Esc key press for clean window close
        if event.key() != QtCore.Qt.Key_Escape:
            self.ui.savedKeyPressEvent(event)
        else:
            self.ui.close()
