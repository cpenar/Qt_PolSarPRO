#!/usr/bin/env python3
# -*- codding: utf-8 -*-



# -*- coding: utf-8 -*- 

import sys 
import os 
from logging import warning

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'

class GUI(QtWidgets.QDialog):
    def __init__(self):
        super(GUI, self).__init__()
        # Reserved attributes name
        self.zoomRatio = None
        self.image = None
        self.pixmap = None
        self.scene = None
        self.ui = None

        # .ui loader
        self.ui = uic.loadUi('image_viewer.ui')

        # loading image
        self.image = QtGui.QImage(default_image_path)
        if self.image.isNull():
            print("ERR: pas d'image chargé")

        # setting showed pixmap
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap, self.scene)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)

        self.ui.imageView.setScene(self.scene)

        self.ui.show()
        # must be after show() method
        self.fitWindow()

        # signals connection
        self.ui.fitImageButton.clicked.connect(self.fitWindow)
        self.ui.zoomLineEdit.editingFinished.connect(self.setZoomRatio)

        # events connection
        self.ui.imageView.setMouseTracking(True)
        self.scene.mouseMoveEvent = self.imageViewMouseMove

    def imageViewMouseMove(self, event):
        x = str(int(event.lastScenePos().x()))
        y = str(int(event.lastScenePos().y()))
        self.ui.statusBar.setText('x:' + x + '  y:' + y)

    def setZoomRatio(self):
        try:
            newZoomRatio = int(self.ui.zoomLineEdit.text())
        except ValueError:
            warning("Zoom ratio : only int value allowed")
            return self.updateZoomRatio()

        if self.zoomRatio != newZoomRatio:
            self.zoomRatio = newZoomRatio
            #redraw with new ratio
            #width = int(self.pixmap.width() * self.zoomRatio / 100)
            #height = int(self.pixmap.height() * self.zoomRatio / 100)
            #self.scene.setSceneRect(0, 0, width, height)
            self.ui.imageView.resetTransform()
            self.ui.imageView.scale(self.zoomRatio / 100, self.zoomRatio / 100)

    def fitWindow(self):
        self.ui.imageView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.updateZoomRatio()

    def updateZoomRatio(self):
        width_ratio = int(self.ui.imageView.width() / self.pixmap.width() * 100)
        height_ratio = int(self.ui.imageView.height() / self.pixmap.height() * 100)
        self.ui.zoomLineEdit.setText(str(min(width_ratio, height_ratio)))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
