#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import copy
import json

from lib.basic_window import BasicWindow
from confirm_window import ConfirmWindow


class StoreWindow(BasicWindow):
    """
    A window that has a store and a local copy of the config part.
    Manage closing events to ask confirmation when there are
    unsaved changes.
    """
    def __init__(self, uiName, store, *args, **kwargs):
        super().__init__(uiName, store, *args, **kwargs)
        self.globalStore = store
        self.localconfig = copy.deepcopy(store['config'])
        self.ui.saveClosedEvent = self.ui.closeEvent
        self.ui.closeEvent = self.closeEvent

    def closeEvent(self, event):
        if self.localconfig != self.globalStore['config']:
            event.ignore()
            ConfirmWindow(parent=self)
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

    def forceClose(self):
        self.ui.closeEvent = self.ui.saveClosedEvent
        self.ui.close()
