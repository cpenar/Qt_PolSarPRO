#!/usr/bin/env python3
# -*- codding: utf-8 -*-



# -*- coding: utf-8 -*- 

import sys 
import os 

from PyQt5 import QtCore, QtGui, QtWidgets, uic

class MyWindow(QtWidgets.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
