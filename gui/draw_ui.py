# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'draw.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(594, 447)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.connectButton = QtWidgets.QToolButton(Form)
        self.connectButton.setCheckable(True)
        self.connectButton.setAutoRaise(False)
        self.connectButton.setObjectName("connectButton")
        self.verticalLayout_3.addWidget(self.connectButton)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setAcceptDrops(True)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_3.addWidget(self.graphicsView)
        self.verticalLayout_3.setStretch(0, 2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addVarButton = QtWidgets.QToolButton(Form)
        self.addVarButton.setEnabled(True)
        self.addVarButton.setMinimumSize(QtCore.QSize(25, 25))
        self.addVarButton.setObjectName("addVarButton")
        self.verticalLayout.addWidget(self.addVarButton)
        self.treeWidget = variableTreeWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.connectButton.setText(_translate("Form", "->"))
        self.addVarButton.setText(_translate("Form", "+"))
        self.treeWidget.headerItem().setText(0, _translate("Form", "Variablen"))

from gui.variabletreewidget import variableTreeWidget
