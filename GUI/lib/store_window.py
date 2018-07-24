#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import json
from pprint import pformat

from lib.basic_window import BasicWindow
from confirm_window import ConfirmWindow


class StoreWindow(BasicWindow):
    """
    A window that access the global store and has a local
    copy of the config part of the store.
    Manage closing events to ask confirmation when there are
    unsaved changes in the local store.
    The Global Store is NOT initialised here, it is passed as argument !
    Global Store initialisation is responsability of main.py
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

        # logging localconfig as an intermediate log level between
        # INFO (20) and DEBUG (10)
        self.logger.log(logging.STORE_INFO, 'with localconfig value :\n' + pformat(self.localconfig, indent=4))
        try:
            self.globalStore['config'].update(self.localconfig)
            # TODO: dont save to file every time,
            # only when closing PSP
            conffile = self.localconfig['conffile']
            with open(conffile, 'w') as f:
                json.dump(self.localconfig, f, indent=4)
        except Exception as e:
            self.logger.error('Error when saving configuration')
            self.logger.debug(e, exc_info=True)
        self.ui.close()

    def forceClose(self):
        self.ui.closeEvent = self.ui.saveClosedEvent
        self.ui.close()
