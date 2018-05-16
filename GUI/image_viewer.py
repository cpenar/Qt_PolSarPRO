#!/usr/bin/env python3
# -*- codding: utf-8 -*-

import json
from logging import error, warning, info

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from lib.gen_window import GenWindow
from lib.callback_manager import cbManager

# variable for dev phase
default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'
#default_image_path = '/tmp/huge.bmp'


class Window(GenWindow):
    def __init__(self, store, image=None):
        self.ui = QtWidgets.QDialog()
        super().__init__(__name__, store)

        # Reserved attribute names
        self.zoomRatio = None
        self.image = None
        self.pixmap = None
        self.scene = None
        self.cbm = None
        self.polygonSelection = None

        self.currentpoly = []
        self.qcolors = (
            'black', 'blue', 'red', 'cyan',
            'darkBlue', 'darkGray', 'darkGreen',
            'darkMagenta', 'darkRed', 'darkYellow', 'gray',
            'green', 'lightGray', 'magenta',   'yellow')

        self.color = 0

        # loading image
        if image is None:
            try:
                self.image = QtGui.QImage(default_image_path)
            except:
                error("Couldn't load " + default_image_path)
        else:
            self.image = image

        if self.image.isNull():
            warning("ERR: No image loaded")

        self.setViewFromImage()

        self.ui.imageView.setMouseTracking(True)
        self.ui.imageView.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        self.fitWindow()

        # signals connection
        self.ui.zoomLineEdit.editingFinished.connect(self.setZoomRatio)

        # menu actions
        self.ui.actionFit_to_window.triggered.connect(self.fitWindow)
        self.ui.actionDraw_new_class_polygon.triggered.connect(
            self.draw_new_class_polygon)
        self.ui.actionDraw_same_class_polygon.triggered.connect(
            self.draw_same_class_polygon)
        self.ui.actionRemove_last_polygon.triggered.connect(
            self.remove_last_poly)
        self.ui.actionRemove_all_selection.triggered.connect(
            self.remove_all_selection)
        self.ui.actionExtract_selection.triggered.connect(
            self.extract_selection)
        self.ui.actionRotate_Right.triggered.connect(
            self.rotateRight)
        self.ui.actionRotate_Left.triggered.connect(
            self.rotateLeft)
        self.ui.actionFlip_Vertically.triggered.connect(
            self.flipVertically)
        self.ui.actionFlip_Horizontally.triggered.connect(
            self.flipHorizontally)

        ### QEvent management ###

        # suppress Escape key closing event for Dialog window
        self.ui.savedKeyPressEvent = self.ui.keyPressEvent
        self.ui.keyPressEvent = self.dontCloseWithEscapeKey

        # Wheel event for zooming
        self.ui.imageView.wheelEvent = self.wheelEvent

    def setViewFromImage(self):
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        if self.scene is not None:
            self.scene.clear()
            self.scene.deleteLater()

        self.scene = ImageScene()
        self.ui.imageView.setScene(self.scene)
        self.scene.addPixmap(self.pixmap)

        # events connection using the cbManager
        self.scene.mouseMoveEvent, self.mouseMoveECbm = cbManager(
            self.scene.mouseMoveEvent, self.mousePosToStatusBar)
        self.scene.mousePressEvent, self.mousePressECbm = cbManager(
            self.scene.mousePressEvent)
        self.resetPolygonSelection()

    def resetPolygonSelection(self):
        self.color = 0
        self.polygonSelection = {
            'polyQsegments': [],
            'tempQsegments': [],
            'currentpoly': [],
            'classPolygons': [],
            }

    def flipVertically(self):
        self.image = self.image.mirrored(vertical=True)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

    def flipHorizontally(self):
        self.image = self.image.mirrored(horizontal=True)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)

    def rotateRight(self):
        transfo = QtGui.QTransform()
        transfo.rotate(90)
        self.image = self.image.transformed(transfo)
        self.setViewFromImage()

    def rotateLeft(self):
        transfo = QtGui.QTransform()
        transfo.rotate(-90)
        self.image = self.image.transformed(transfo)
        self.setViewFromImage()

    def wheelEvent(self, event):
        zoomFactor = 1.1
        if event.angleDelta().y() < 0:
            zoomFactor = 1.0 / zoomFactor
        self.zoomRatio = self.zoomRatio * zoomFactor
        self.ui.imageView.scale(zoomFactor, zoomFactor)
        self.ui.zoomLineEdit.setText(format(self.zoomRatio, '.2f'))

    def extract_selection(self):
        classes = self.polygonSelection['classPolygons']
        if not classes:
            error('Create polygon selection first')
            return

        training_file_path = self.config['tempDir'] + '/training.json'
        info('Saving polygon selections in ' + training_file_path)
        with open(training_file_path, 'w') as fp:
            json.dump(classes, fp, indent=4, separators=(',', 'g '))

    def remove_all_selection(self):
        pSelect = self.polygonSelection

        # removing all drawed QLines
        while pSelect['polyQsegments']:
            self.remove_last_poly()

        # reseting classPolygon
        pSelect['classPolygons'] = []

    def remove_last_poly(self):
        pSelect = self.polygonSelection
        if not pSelect['polyQsegments']:
            warning('No polygon selection to remove')
            return

        # removing drawed QLines
        lastPoly = pSelect['polyQsegments'].pop()
        while lastPoly:
            self.scene.removeItem(lastPoly.pop())

        # removing stored polygon
        if pSelect['classPolygons'][-1] == []:
            pSelect['classPolygons'].pop()
        pSelect['classPolygons'][-1].pop()

    def draw_new_class_polygon(self):
        # Disconnect drag mode
        self.ui.imageView.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.color = (self.color + 1) % len(self.qcolors)
        self.polygonSelection['classPolygons'].append([])
        self.polygonSelection['polyQsegments'].append([])
        self.mouseMoveECbm.connect(self.draw_temp_segment)
        self.mousePressECbm.connect(self.nextPolyCoord)

    def draw_same_class_polygon(self):
        pSelect = self.polygonSelection
        if not pSelect['classPolygons']:
            warning('Start creating class first')
            return False

        self.ui.imageView.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.polygonSelection['polyQsegments'].append([])
        self.mouseMoveECbm.connect(self.draw_temp_segment)
        self.mousePressECbm.connect(self.nextPolyCoord)

    def draw_temp_segment(self, event):
        pSelect = self.polygonSelection
        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Mouse not in image ? -> nothing to do
        if not (int(x) in range(self.image.width()) and
                int(y) in range(self.image.height())):
            return

        # remove previous temp segments
        while pSelect['tempQsegments']:
            self.scene.removeItem(pSelect['tempQsegments'].pop())

        if pSelect['currentpoly']:
            segment = self.draw_segment(pSelect['currentpoly'][-1], (x, y))
            pSelect['tempQsegments'].append(segment)

            segment = self.draw_segment(
                pSelect['currentpoly'][0], (x, y), Qt.white)
            pSelect['tempQsegments'].append(segment)

    def removeTempQsegments(self):
        tempQsegments = self.polygonSelection['tempQsegments']
        while tempQsegments:
            self.scene.removeItem(tempQsegments.pop())

    def nextPolyCoord(self, event):
        # Draw the polygon segments while vertices are
        # defined with mouse clicks.
        # Store the polygon when it is closed.
        pSelect = self.polygonSelection
        current = pSelect['currentpoly']
        if not event.button() in (Qt.LeftButton, Qt.RightButton):
            return

        x, y = event.lastScenePos().x(), event.lastScenePos().y()

        # Not in image ? -> nothing to do
        if not (int(x) in range(self.image.width()) and
                int(y) in range(self.image.height())):
            return

        current.append((x, y))

        if len(current) > 1:
            pSelect['polyQsegments'][-1].append(
                self.draw_segment(current[-1], current[-2]))

        # right button -> last segment
        if event.button() == Qt.RightButton:
            pSelect['classPolygons'][-1].append(current.copy())
            # draw last segment
            pSelect['polyQsegments'][-1].append(
                self.draw_segment(current[-1], current[0]))
            # reset currentpoly
            current.clear()
            # remove callbacks
            self.mouseMoveECbm.removeCallback(self.draw_temp_segment)
            self.mousePressECbm.removeCallback(self.nextPolyCoord)
            # remove tempQsegments
            self.removeTempQsegments()
            self.ui.imageView.setDragMode(
                QtWidgets.QGraphicsView.ScrollHandDrag)

    def draw_segment(self, pt1, pt2, color=None):
        x1, y1, x2, y2 = pt1[0], pt1[1], pt2[0], pt2[1]
        if color is None:
            color = getattr(Qt, self.qcolors[self.color])
        # a styled pen for an easier view not depending of zoom factor
        pen = QtGui.QPen(color, 0)
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
            self.ui.zoomLineEdit.setText(format(self.zoomRatio, '.2f'))
            return False
        if self.zoomRatio != newZoomRatio:
            self.zoomRatio = newZoomRatio
            self.ui.imageView.resetTransform()
            self.ui.imageView.scale(self.zoomRatio / 100, self.zoomRatio / 100)

    def fitWindow(self):
        widthRatio = self.ui.imageView.size().width() / self.pixmap.width()
        heightRatio = self.ui.imageView.size().height() / self.pixmap.height()

        ratio = min(widthRatio, heightRatio)
        self.ui.zoomLineEdit.setText(format(ratio*98, '.2f'))
        self.setZoomRatio()


class ImageScene(QtWidgets.QGraphicsScene):
    # doesn't do much but need it because
    # overiding Qt builtin method does not work well.

    def __init__(self, parent=None):
        super(ImageScene, self).__init__(parent)

    def mouseMoveEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mouseMoveEvent(self, *args, **kargs)

    def mousePressEvent(self, *args, **kargs):
        return QtWidgets.QGraphicsScene.mousePressEvent(self, *args, **kargs)
