#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
import json
from pprint import pformat

from PyQt5 import QtCore

from lib.basic_window import BasicWindow
from lib.confirm_window import ConfirmWindow


class StoreWindow(BasicWindow):
    """
    A window that has a store and a local copy of the config part.
    Manage closing events to ask confirmation when there are
    unsaved changes.
    """
    def __init__(self, uiName, store):
        super().__init__(__name__, store)

        self.globalStore = store
        self.localconfig = copy.deepcopy(store['config'])

        self.logger.debug('    config=' + '\n' + pformat(self.localconfig))

    def closeEvent(self, event):
        self.logger.info('Asked for closing')
        if self.localconfig != self.globalStore['config']:
            event.ignore()
            ConfirmWindow()
        else:
            self.logger.info('Closing window ' + self.uiName)
            event.accept()

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
