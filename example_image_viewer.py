#!/usr/bin/env python3
# -*- codding: utf-8 -*-



# -*- coding: utf-8 -*- 

import sys 
import os 

from PyQt5 import QtCore, QtGui, QtWidgets

class ImageViewer(object): 
    def setupUi(self, Viewer): 
        Viewer.resize(640, 480) 
        Viewer.setWindowTitle(u"Exemples d'usage d'images")
        self.image_1 = "/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp" 
        self.image_2 = "image2.png"
        self.centralwidget = QtWidgets.QWidget(Viewer) 
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget) 
        self.verticalLayout_2 = QtWidgets.QVBoxLayout() 
        self.horizontalLayout = QtWidgets.QHBoxLayout() 

        # QLabel 
        self.label = QtWidgets.QLabel(self.centralwidget) 
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                QtWidgets.QSizePolicy.Fixed) 
        self.label.setSizePolicy(sizePolicy) 
        self.label.setPixmap(QtGui.QPixmap(self.image_1)) 
        self.label.setScaledContents(True) 
        self.horizontalLayout.addWidget(self.label) 

        self.verticalLayout = QtWidgets.QVBoxLayout() 
        self.label_cmb = QtWidgets.QComboBox(self.centralwidget) 
        self.verticalLayout.addWidget(self.label_cmb) 
        spacerItem = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, 
                QtWidgets.QSizePolicy.Fixed) 
        self.verticalLayout.addItem(spacerItem) 
        self.horizontalLayout.addLayout(self.verticalLayout) 
        self.verticalLayout_2.addLayout(self.horizontalLayout) 
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout() 

        # QPushButton 
        self.pushButton = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton.setText("PushButton") 
        icon1 = QtGui.QIcon() 
        icon1.addPixmap(QtGui.QPixmap(self.image_2),QtGui.QIcon.Normal, 
                QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1) 
        self.horizontalLayout_2.addWidget(self.pushButton) 

        self.push_cmb = QtWidgets.QComboBox(self.centralwidget) 
        self.horizontalLayout_2.addWidget(self.push_cmb) 

        # QToolButton 
        self.toolButton = QtWidgets.QToolButton(self.centralwidget) 
        self.toolButton.setText("toolButton")  
        self.toolButton.setIcon(icon1)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon) 
        self.horizontalLayout_2.addWidget(self.toolButton) 

        self.tool_cmb = QtWidgets.QComboBox(self.centralwidget) 
        self.horizontalLayout_2.addWidget(self.tool_cmb) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_2) 
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout() 

        # QRadioButton 
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget) 
        self.radioButton.setText("RadioButton") 
        self.radioButton.setIcon(icon1) 
        self.horizontalLayout_3.addWidget(self.radioButton) 

        # QCheckBox 
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget) 
        self.checkBox.setText("CheckBox") 
        self.checkBox.setIcon(icon1) 
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft) 
        self.horizontalLayout_3.addWidget(self.checkBox) 
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, 
                QtWidgets.QSizePolicy.Minimum) 
        self.horizontalLayout_3.addItem(spacerItem1) 

        # Colors comboBox 
        self.colors_cmb = QtWidgets.QComboBox(self.centralwidget) 
        self.horizontalLayout_3.addWidget(self.colors_cmb) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_3) 

        # QGraphicsView 
        self.vue = QtWidgets.QGraphicsView(self.centralwidget) 
        self.verticalLayout_2.addWidget(self.vue) 

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout() 
        self.horizontalLayout_4.setObjectName("horizontalLayout_4") 
        self.image_btn = QtWidgets.QToolButton(self.centralwidget) 
        self.image_btn.setText("Image") 
        self.image_btn.setObjectName("image_btn") 
        self.horizontalLayout_4.addWidget(self.image_btn) 
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, 
                QtWidgets.QSizePolicy.Minimum) 
        self.horizontalLayout_4.addItem(spacerItem2) 
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1) 
        Viewer.setCentralWidget(self.centralwidget) 

        self.populate_combos() 

        # Connections
        self.label_cmb.currentIndexChanged.connect(self.update_label) 
        self.push_cmb.currentIndexChanged.connect(self.update_push_button)
        self.tool_cmb.currentIndexChanged.connect(self.update_tool_button) 

    def populate_combos(self): 
        items = ["setScaledContents(True)", "setScaledContents(False)"]
        self.label_cmb.addItems(items) 
        items = ["Modifier...", "setAutoDefault()", "setDefaut()", "setFlat()"] 
        self.push_cmb.addItems(items) 

        items = ["Modifier...", "setAutoRaise()", "ToolButtonIconOnly", 
                "ToolButtonTextOnly", "ToolButtonTextBesideIcon", 
                "ToolButtonTextUnderIcon", "ToolButtonFollowStyle"] 
        self.tool_cmb.addItems(items) 

        names = ["Rouge", "Vert", "Bleu"] 
        colors = [QtGui.QColor(255, 0, 0, 255), QtGui.QColor(0, 255, 0, 255), 
                QtGui.QColor(0, 0, 255, 255)] 
        pix = QtGui.QPixmap(QtCore.QSize(30, 10))
        self.colors_cmb.setIconSize(QtCore.QSize(30, 10)) 
        for idx, name in enumerate(names):  
            pix.fill(colors[idx]) 
            icon = QtGui.QIcon(pix)
            self.colors_cmb.addItem(icon, name) 

    def update_label(self, idx): 
        self.label.setScaledContents(not self.label.hasScaledContents()) 

    def update_push_button(self, idx): 
        if not idx: 
            return 
        if idx == 1:
            self.pushButton.setAutoDefault(not self.pushButton.autoDefault()) 
        elif idx == 2: 
            self.pushButton.setDefault(not self.pushButton.isDefault()) 
        else: 
            self.pushButton.setFlat(not self.pushButton.isFlat()) 

    def update_tool_button(self, idx): 
        if not idx: 
            return 
        if idx == 1: 
            self.toolButton.setAutoRaise(not self.toolButton.autoRaise()) 
        else: 
            self.toolButton.setToolButtonStyle(idx-2) 


if __name__ == "__main__": 
    import sys 
    app = QtWidgets.QApplication(sys.argv) 
    Viewer = QtWidgets.QMainWindow() 
    ui = ImageViewer() 
    ui.setupUi(Viewer) 
    Viewer.show()
    sys.exit(app.exec_()) 
