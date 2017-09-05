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
        uic.loadUi('image_viewer.ui', self)

        self.image = QtGui.QImage(default_image_path)
        if self.image.isNull():
            print("ERR: pas d'image chargé")

        self.pixmap = QtGui.QPixmap.fromImage(self.image)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)

        self.imageView.setScene(self.scene)

        self.show()
        self.imageView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
