#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import sys
#import os
from logging import error, warning

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem

from lib.callback_manager import cbManager

default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'


class Window():
    def __init__(self):
        # Reserved attributes name
        self.ui = None
        self.zoomRatio = None
        self.image = None
        self.pixmap = None
        self.scene = None
        self.currentpoly = []
        self.cbm = None
        self.polygonSelection = {
            'polyQsegments': [],
            'tempQsegments': [],
            'currentpoly': [],
            'polygons': [],
            }

        # .ui loader
        self.ui = uic.loadUi('image_viewer.ui')

        # suppress Escape key closing event for Dialog window
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.dontCloseWithEscapeKey

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
        self.ui.imageView.setMouseTracking(True)

        # signals connection
        self.ui.zoomLineEdit.editingFinished.connect(self.setZoomRatio)

        # menu actions
        self.ui.actionFit_to_window.triggered.connect(self.fitWindow)
        self.ui.actionDraw_polygon.triggered.connect(self.start_draw_polygon)

        # events connection using the cbManager
        self.scene.mouseMoveEvent, self.mouseMoveECbm = cbManager(
            self.scene.mouseMoveEvent, self.mousePosToStatusBar)
        self.scene.mousePressEvent, self.mousePressECbm = cbManager(
            self.scene.mousePressEvent)

        # must be after show() method
        self.fitWindow()
        # a timeout to be sure that we resize the imageView
        # after the window manager is done decorating the window
        #QtCore.QTimer.singleShot(500, self.fitWindow)

    def start_draw_polygon(self):
        self.mouseMoveECbm.connect(self.draw_temp_segment)
        self.mousePressECbm.connect(self.nextPolyCoord)
        self.polygonSelection['polyQsegments'].append([])

    def draw_temp_segment(self, event):
        pSelect = self.polygonSelection
        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Not in image ? -> nothing to do
        if not (int(x) in range(self.image.width()) and
                int(y) in range(self.image.height())):
            return

        # remove previous temp segments
        while pSelect['tempQsegments']:
            self.scene.removeItem(pSelect['tempQsegments'].pop())

        if pSelect['currentpoly']:
            pSelect['tempQsegments'].append(
                self.draw_segment(pSelect['currentpoly'][-1], (x, y)))
            pSelect['tempQsegments'].append(
                self.draw_segment(pSelect['currentpoly'][0], (x, y)))

    def nextPolyCoord(self, event):
        # Draw the polygon segments while vertices are
        # defined with mouse clicks.
        # Store the polygon when it is closed.
        pSelect = self.polygonSelection
        if not event.button() in (Qt.LeftButton, Qt.RightButton):
            return

        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Not in image ? -> nothing to do
        if not (int(x) in range(self.image.width()) and
                int(y) in range(self.image.height())):
            return

        pSelect['currentpoly'].append((x, y))

        if len(self.currentpoly) > 1:
            pSelect['polyQsegments'].append(
                self.draw_segment(self.currentpoly[-1], self.currentpoly[-2]))

            # right button -> last segment
        if event.button() == Qt.RightButton:
            pSelect['polygons'].append(self.currentpoly)
            # draw last segment
            self.draw_segment(self.currentpoly[-1], self.currentpoly[0])
            # reset currentpoly
            self.currentpoly = []
            # remove callbacks
            self.mouseMoveECbm.removeCallback(self.draw_temp_segment)
            self.mousePressECbm.removeCallback(self.nextPolyCoord)

    def draw_segment(self, pt1, pt2):
        x1, y1, x2, y2 = pt1[0], pt1[1], pt2[0], pt2[1]
        # a styled pen for an easier view not depending of zoom factor
        pen = QtGui.QPen(Qt.black, 0)
        return self.scene.addLine(QtCore.QLineF(x1, y1, x2, y2), pen=pen)

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
        self.ui.imageView.fitInView(
            self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.updateZoomRatio()

    def updateZoomRatio(self):
        width_ratio = self.ui.imageView.width() / self.pixmap.width() * 100
        height_ratio = self.ui.imageView.height() / self.pixmap.height() * 100
        self.ui.zoomLineEdit.setText(format(
            min(width_ratio, height_ratio), '.2f'))


class ImageScene(QtWidgets.QGraphicsScene):
    # doesnt do much but need it because overiding
    # Qt builtin method doest work well.

    def __init__(self, parent=None):
        super(ImageScene, self).__init__(parent)

    def mouseMoveEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mouseMoveEvent(self, *args, **kargs)

    def mousePressEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mousePressEvent(self, *args, **kargs)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
