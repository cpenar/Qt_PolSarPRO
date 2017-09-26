#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
from pprint import pformat

from PyQt5 import uic, QtWidgets


class GenWindow():
    def __init__(self, uiName, state, **kargs):
        self.logger = state['logger']
        self.logger.debug('Initializing ' + __name__)
        self.logger.debug('With arguments :\n' +
            'uiName=' + uiName + '\n' +
            'kargs=' + pformat(kargs) +'\n' +
            'state=' + pformat(state))

        self.globState = state
        self.config = copy.deepcopy(state['config'])
        self.ui = QtWidgets.QDialog()
        self.ui = uic.loadUi(uiName + '.ui', self.ui)
        self.ui.show()
