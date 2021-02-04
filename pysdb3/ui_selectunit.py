# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pysdb3/ui/selectunit.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogSelectUnit(object):
    def setupUi(self, DialogSelectUnit):
        DialogSelectUnit.setObjectName("DialogSelectUnit")
        DialogSelectUnit.resize(207, 97)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogSelectUnit)
        self.verticalLayout.setObjectName("verticalLayout")
        self.unitCombo = QtWidgets.QComboBox(DialogSelectUnit)
        self.unitCombo.setObjectName("unitCombo")
        self.verticalLayout.addWidget(self.unitCombo)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogSelectUnit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogSelectUnit)
        self.buttonBox.accepted.connect(DialogSelectUnit.accept)
        self.buttonBox.rejected.connect(DialogSelectUnit.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogSelectUnit)

    def retranslateUi(self, DialogSelectUnit):
        _translate = QtCore.QCoreApplication.translate
        DialogSelectUnit.setWindowTitle(_translate("DialogSelectUnit", "Select unit"))
