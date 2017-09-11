#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import sys 
import os 
from logging import critical, error, warning, info, debug

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem

from lib.callback_manager import cbManager

default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'

class Window():
    def __init__(self):
        # Reserved attributes name
        self.zoomRatio = None
        self.image = None
        self.pixmap = None
        self.scene = None
        self.ui = None
        self.currentpoly = []
        self.polygonCollection = []
        self.cbm = None

        # .ui loader
        self.ui = uic.loadUi('image_viewer.ui')

        # suppress Escape key closing event for Dialog window
        self.modify_keyPressEvent()

        # opening and showing the window
        self.ui.show()

        # loading image
        try:
            self.image = QtGui.QImage(default_image_path)
        except:
            error("Couldn't load " + default_image_path)

        if self.image.isNull():
            warning("ERR: No image loaded")

        # setting showed pixmap
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap, self.scene)

        self.scene = ImageScene()
        self.scene.addPixmap(self.pixmap)

        self.ui.imageView.setScene(self.scene)

        # signals connection
        self.ui.zoomLineEdit.editingFinished.connect(self.setZoomRatio)

        # menu actions
        self.ui.actionFit_to_window.triggered.connect(self.fitWindow)
        self.ui.actionDraw_polygon.triggered.connect(self.start_draw_polygon)

        # events connection
        self.ui.imageView.setMouseTracking(True)
        self.scene.mouseMoveEvent, self.mouseMoveEventCbm = cbManager(
                self.scene.mouseMoveEvent, self.mousePosToStatusBar)

        # must be after show() method
        self.fitWindow()

    def start_draw_polygon(self):
        self.scene.mousePressEvent = self.nextPolyCoord
        self.mouseMoveEventCbm.connect(self.draw_temp_segment)

    def draw_temp_segment(self, event):
        debug("Not implemented")
        pass
        

    def nextPolyCoord(self, event):
        # Draw the polygon segments while vertices are
        # defined with mouse clicks.
        # Store the polygon when it is closed.
        if not event.button() in (Qt.LeftButton, Qt.RightButton): return

        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Not in image ? -> nothing to do
        if not (int(x) in range(self.image.width()) and \
                int(y) in range(self.image.height())):
            return

        self.currentpoly.append((x, y))

        if len(self.currentpoly) > 1:
            self.draw_segment(self.currentpoly[-1], self.currentpoly[-2])

        # right button -> last segment
        if event.button() == Qt.RightButton:
            self.polygonCollection.append(self.currentpoly)
            # draw last segment
            self.draw_segment(self.currentpoly[-1], self.currentpoly[0])
            # reset currentpoly
            self.currentpoly = []
            # remove draw_temp_segment callback
            self.mouseMoveEventCbm.removeCallback(self.draw_temp_segment)
            # remove mousePressEvent
            self.scene.mousePressEvent = lambda *args, **kargs: None

        # refresh canvas? view ?

    def draw_segment(self, pt1, pt2, color="k"):
        x1, y1, x2, y2 = pt1[0], pt1[1], pt2[0], pt2[1]
        # a styled pen for an easier view not depending of zoom factor
        pen = QtGui.QPen(Qt.black, 0)
        return self.scene.addLine(QtCore.QLineF(x1, y1, x2, y2), pen=pen)

    def modify_keyPressEvent(self):
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.dontCloseWithEscapeKey

    def dontCloseWithEscapeKey(self, event):
        if event.key() != QtCore.Qt.Key_Escape:
            self.ui.savedKeyPressEvent(event)

    def mousePosToStatusBar(self, event):
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
            newZoomRatio = float(self.ui.zoomLineEdit.text())
        except ValueError:
            warning("Zoom ratio : only numbers allowed")
            return self.updateZoomRatio()

        if self.zoomRatio != newZoomRatio:
            self.zoomRatio = newZoomRatio
            self.ui.imageView.resetTransform()
            self.ui.imageView.scale(self.zoomRatio / 100, self.zoomRatio / 100)


    def fitWindow(self):
        self.ui.imageView.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.updateZoomRatio()

    def updateZoomRatio(self):
        width_ratio = self.ui.imageView.width() / self.pixmap.width() * 100
        height_ratio = self.ui.imageView.height() / self.pixmap.height() * 100
        self.ui.zoomLineEdit.setText(format(
            min(width_ratio, height_ratio), '.2f'))



class ImageScene(QtWidgets.QGraphicsScene):
    # doesnt do much but need it because overiding
    # Qt builtin method doest work well.

    def __init__(self,parent = None):
        super(ImageScene, self).__init__(parent)

    def mouseMoveEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mouseMoveEvent(self, *args, **kargs)

    def mousePressEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mousePressEvent(self, *args, **kargs)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
