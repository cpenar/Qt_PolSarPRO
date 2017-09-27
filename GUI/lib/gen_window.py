#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
from pprint import pformat
import logging

from PyQt5 import uic


class GenWindow():
    def __init__(self, uiName, state, **kargs):

        self.logger = logging.getLogger(uiName)
        print(uiName)
        self.logger.info('Opening window ' + uiName)
        self.logger.debug(
            'With arguments :\n' +
            'uiName=' + uiName + '\n' +
            'kargs=' + pformat(kargs) + '\n' +
            'state=' + pformat(state))

        self.globState = state
        self.config = copy.deepcopy(state['config'])

        self.ui = uic.loadUi(uiName + '.ui', self.ui)
        self.ui.show()
