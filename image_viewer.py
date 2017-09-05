#!/usr/bin/env python3
# -*- codding: utf-8 -*-



# -*- coding: utf-8 -*- 

import sys 
import os 

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap

default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'

class GUI(QtWidgets.QDialog):
    def __init__(self):
        super(GUI, self).__init__()
        # .ui laoder
        uic.loadUi('image_viewer.ui', self)

        self.image = QtGui.QImage(default_image_path)
        if self.image.isNull():
            print("ERR: pas d'image chargé")

        self.pixmap = QtGui.QPixmap.fromImage(self.image)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)

        self.imageView.setScene(self.scene)

        self.show()
        # must be after show() method
        self.imageView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        # more stuff
        self.verticalLayout.resizeEvent = self.onResize

    def onResize(self, event):
        print('toto')
        print(event)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.resizeEvent = window.onResize
    sys.exit(app.exec_())
