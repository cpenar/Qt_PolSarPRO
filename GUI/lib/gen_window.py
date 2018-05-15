#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
import logging
from pprint import pformat

from PyQt5 import uic, QtWidgets


class GenWindow():
    def __init__(self, uiName, store, **kargs):
        self.logger = logging.getLogger(uiName)
        self.logger.info('Opening window ' + uiName)
        self.logger.debug(
            'With arguments :\n' +
            '    uiName=' + uiName + '\n' +
            '    kargs=' + pformat(kargs) + '\n' +
            '    store=' + pformat(store))

        self.globalStore = store
        self.config = copy.deepcopy(store['config'])

        self.ui = QtWidgets.QDialog()
        self.ui = uic.loadUi(uiName + '.ui', self.ui)
        self.ui.show()
