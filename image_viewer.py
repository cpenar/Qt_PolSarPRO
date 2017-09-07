#!/usr/bin/env python3
# -*- codding: utf-8 -*-



# -*- coding: utf-8 -*- 

import sys 
import os 
from logging import critical, error, warning, info, debug

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
        self.currentpoly = []
        self.polycollection = []

        # .ui loader
        self.ui = uic.loadUi('image_viewer.ui')

        # loading image
        try:
            self.image = QtGui.QImage(default_image_path)
        except:
            error("Couldn't load " + default_image_path)

        if self.image.isNull():
            warning("ERR: pas d'image chargé")

        # setting showed pixmap
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap, self.scene)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.addPixmap(self.pixmap)

        self.ui.imageView.setScene(self.scene)

        self.ui.show()

        # suppress Escape key closing event for Dialog
        self.modify_keyPressEvent()

        # signals connection
        self.ui.zoomLineEdit.editingFinished.connect(self.setZoomRatio)

        # menu actions
        self.ui.actionFit_to_window.triggered.connect(self.fitWindow)
        self.ui.actionDraw_polygon.triggered.connect(self.start_draw_polygon)

        # events connection
        self.ui.imageView.setMouseTracking(True)
        self.scene.mouseMoveEvent = self.imageViewMouseMove

        # must be after show() method
        self.fitWindow()

    def start_draw_polygon(self):
        print('menu add poly')
        # 1. connect un event mouse click vers self.next_poly_coord
        self.scene.mousePressEvent = self.nextPolyCoord
        # 2. connect mouse motion vers self.draw_temp_segment

    def nextPolyCoord(self, event):
        print("cliecked")
        if not event.button() in (Qt.LeftButton, Qt.RightButton): return

        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Not in image ? -> nothing to do
        if not (x in range(self.image.width()) and \
                y in range(self.image.height())):
            return

        self.currentpoly.append((x, y))

        if len(self.currentpoly) > 1:
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[-2])

        # right button -> last segment
        if event.button() == Qt.RightButton():
            self.polycollection.append(self.currentpoly)
            # draw last segment
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[0])
            # reset currentpoly
            self.currentpoly = []

        # refresh canvas? view ?

    def modify_keyPressEvent(self):
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.dontCloseWithEscapeKey

    def dontCloseWithEscapeKey(self, event):
        if event.key() != QtCore.Qt.Key_Escape:
            self.ui.savedKeyPressEvent(event)

    def imageViewMouseMove(self, event):
        pos = event.lastScenePos()
        x = int(pos.x())
        y = int(pos.y())
        # are we inside the image ?
        if x in range(self.image.width()) and y in range(self.image.height()):
            value = self.image.pixel(x, y)
            rgb = str(QtGui.QColor(value).getRgb()[:-1])
            self.ui.statusBar.setText(
                    'x:' + str(x) + '  y:' + str(y) + '  value:' + rgb)

    def setZoomRatio(self):
        try:
            newZoomRatio = int(self.ui.zoomLineEdit.text())
        except ValueError:
            warning("Zoom ratio : only int value allowed")
            return self.updateZoomRatio()

        if self.zoomRatio != newZoomRatio:
            self.zoomRatio = newZoomRatio
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
