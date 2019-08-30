# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pysdb3/ui/importsitescsv.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogImportSitesCSV(object):
    def setupUi(self, DialogImportSitesCSV):
        DialogImportSitesCSV.setObjectName("DialogImportSitesCSV")
        DialogImportSitesCSV.resize(273, 271)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogImportSitesCSV)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(DialogImportSitesCSV)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.siteComboCSV = QtWidgets.QComboBox(self.groupBox)
        self.siteComboCSV.setObjectName("siteComboCSV")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.siteComboCSV)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lonComboCSV = QtWidgets.QComboBox(self.groupBox)
        self.lonComboCSV.setObjectName("lonComboCSV")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lonComboCSV)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.latComboCSV = QtWidgets.QComboBox(self.groupBox)
        self.latComboCSV.setObjectName("latComboCSV")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.latComboCSV)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(DialogImportSitesCSV)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.radioUnitExisting = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioUnitExisting.setChecked(True)
        self.radioUnitExisting.setObjectName("radioUnitExisting")
        self.buttonGroup = QtWidgets.QButtonGroup(DialogImportSitesCSV)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioUnitExisting)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.radioUnitExisting)
        self.unitCombo = QtWidgets.QComboBox(self.groupBox_2)
        self.unitCombo.setObjectName("unitCombo")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.unitCombo)
        self.radioUnitCSV = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioUnitCSV.setObjectName("radioUnitCSV")
        self.buttonGroup.addButton(self.radioUnitCSV)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radioUnitCSV)
        self.unitComboCSV = QtWidgets.QComboBox(self.groupBox_2)
        self.unitComboCSV.setObjectName("unitComboCSV")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.unitComboCSV)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogImportSitesCSV)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogImportSitesCSV)
        self.buttonBox.accepted.connect(DialogImportSitesCSV.accept)
        self.buttonBox.rejected.connect(DialogImportSitesCSV.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogImportSitesCSV)

    def retranslateUi(self, DialogImportSitesCSV):
        _translate = QtCore.QCoreApplication.translate
        DialogImportSitesCSV.setWindowTitle(_translate("DialogImportSitesCSV", "Import from CSV"))
        self.groupBox.setTitle(_translate("DialogImportSitesCSV", "Site"))
        self.label.setText(_translate("DialogImportSitesCSV", "Name:"))
        self.label_2.setText(_translate("DialogImportSitesCSV", "X/Longitude:"))
        self.label_3.setText(_translate("DialogImportSitesCSV", "Y/Latitude:"))
        self.groupBox_2.setTitle(_translate("DialogImportSitesCSV", "Unit"))
        self.radioUnitExisting.setText(_translate("DialogImportSitesCSV", "Existing:"))
        self.radioUnitCSV.setText(_translate("DialogImportSitesCSV", "From CSV:"))

