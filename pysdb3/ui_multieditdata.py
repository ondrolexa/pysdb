# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pysdb3/ui/multieditdata.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogMultiEditData(object):
    def setupUi(self, DialogMultiEditData):
        DialogMultiEditData.setObjectName("DialogMultiEditData")
        DialogMultiEditData.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogMultiEditData.resize(350, 213)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(DialogMultiEditData)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.structureCombo = QtWidgets.QComboBox(DialogMultiEditData)
        self.structureCombo.setMinimumSize(QtCore.QSize(100, 0))
        self.structureCombo.setObjectName("structureCombo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.structureCombo)
        self.label_4 = QtWidgets.QLabel(DialogMultiEditData)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.groupBox = QtWidgets.QGroupBox(DialogMultiEditData)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioBoth = QtWidgets.QRadioButton(self.groupBox)
        self.radioBoth.setChecked(True)
        self.radioBoth.setObjectName("radioBoth")
        self.verticalLayout.addWidget(self.radioBoth)
        self.radioStructure = QtWidgets.QRadioButton(self.groupBox)
        self.radioStructure.setObjectName("radioStructure")
        self.verticalLayout.addWidget(self.radioStructure)
        self.radioTags = QtWidgets.QRadioButton(self.groupBox)
        self.radioTags.setObjectName("radioTags")
        self.verticalLayout.addWidget(self.radioTags)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.taggedView = QtWidgets.QTableView(DialogMultiEditData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.taggedView.sizePolicy().hasHeightForWidth())
        self.taggedView.setSizePolicy(sizePolicy)
        self.taggedView.setMaximumSize(QtCore.QSize(150, 16777215))
        self.taggedView.setShowGrid(False)
        self.taggedView.setObjectName("taggedView")
        self.taggedView.horizontalHeader().setVisible(False)
        self.taggedView.horizontalHeader().setStretchLastSection(True)
        self.taggedView.verticalHeader().setVisible(False)
        self.taggedView.verticalHeader().setDefaultSectionSize(18)
        self.horizontalLayout.addWidget(self.taggedView)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogMultiEditData)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.label_4.setBuddy(self.structureCombo)

        self.retranslateUi(DialogMultiEditData)
        self.buttonBox.accepted.connect(DialogMultiEditData.accept)
        self.buttonBox.rejected.connect(DialogMultiEditData.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogMultiEditData)
        DialogMultiEditData.setTabOrder(self.structureCombo, self.buttonBox)

    def retranslateUi(self, DialogMultiEditData):
        _translate = QtCore.QCoreApplication.translate
        DialogMultiEditData.setWindowTitle(_translate("DialogMultiEditData", "Add site"))
        self.label_4.setText(_translate("DialogMultiEditData", "&Structure:"))
        self.groupBox.setTitle(_translate("DialogMultiEditData", "Use"))
        self.radioBoth.setText(_translate("DialogMultiEditData", "Both structure and tags"))
        self.radioStructure.setText(_translate("DialogMultiEditData", "Only structure"))
        self.radioTags.setText(_translate("DialogMultiEditData", "Only tags"))

