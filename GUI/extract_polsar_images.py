#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.store_window import StoreWindow


class Window(StoreWindow):
    def __init__(self, store, **kwargs):
        super().__init__(__name__, store)

        # Initializing Widgets Value

        if 'outputDir' in self.localconfig and self.localconfig['outputDir'] != '':
            self.ui.pushButton_OutputDir.setText(self.localconfig['outputDir'])

        self.ui.lineEdit_InitRow.setText('1')

        if ('initial_rows_number' in self.localconfig and
                self.localconfig['initial_rows_number'] is not ''):
            self.ui.lineEdit_EndRow.setText(str(self.localconfig['initial_rows_number']))

        self.ui.lineEdit_InitCol.setText('1')

        if ('initial_cols_number' in self.localconfig and
                self.localconfig['initial_cols_number'] is not ''):
            self.ui.lineEdit_EndCol.setText(str(self.localconfig['initial_cols_number']))
