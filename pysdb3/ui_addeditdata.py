# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pysdb3/ui/addeditdata.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAddEditData(object):
    def setupUi(self, DialogAddEditData):
        DialogAddEditData.setObjectName("DialogAddEditData")
        DialogAddEditData.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogAddEditData.resize(350, 340)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(DialogAddEditData)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(DialogAddEditData)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.azimuthEdit = QtWidgets.QLineEdit(DialogAddEditData)
        self.azimuthEdit.setObjectName("azimuthEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.azimuthEdit)
        self.label_2 = QtWidgets.QLabel(DialogAddEditData)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.inclinationEdit = QtWidgets.QLineEdit(DialogAddEditData)
        self.inclinationEdit.setObjectName("inclinationEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inclinationEdit)
        self.label_4 = QtWidgets.QLabel(DialogAddEditData)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.structureCombo = QtWidgets.QComboBox(DialogAddEditData)
        self.structureCombo.setMinimumSize(QtCore.QSize(100, 0))
        self.structureCombo.setObjectName("structureCombo")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.structureCombo)
        self.attachLabel = QtWidgets.QLabel(DialogAddEditData)
        self.attachLabel.setObjectName("attachLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.attachLabel)
        self.attachCombo = QtWidgets.QComboBox(DialogAddEditData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachCombo.sizePolicy().hasHeightForWidth())
        self.attachCombo.setSizePolicy(sizePolicy)
        self.attachCombo.setMinimumSize(QtCore.QSize(100, 0))
        self.attachCombo.setEditable(False)
        self.attachCombo.setObjectName("attachCombo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.attachCombo)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.attachErrorLabel = QtWidgets.QLabel(DialogAddEditData)
        self.attachErrorLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.attachErrorLabel.setObjectName("attachErrorLabel")
        self.verticalLayout_2.addWidget(self.attachErrorLabel)
        self.attachLayout = QtWidgets.QHBoxLayout()
        self.attachLayout.setObjectName("attachLayout")
        self.pushFit = QtWidgets.QPushButton(DialogAddEditData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFit.sizePolicy().hasHeightForWidth())
        self.pushFit.setSizePolicy(sizePolicy)
        self.pushFit.setObjectName("pushFit")
        self.attachLayout.addWidget(self.pushFit)
        self.pushAttach = QtWidgets.QPushButton(DialogAddEditData)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushAttach.sizePolicy().hasHeightForWidth())
        self.pushAttach.setSizePolicy(sizePolicy)
        self.pushAttach.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushAttach.setObjectName("pushAttach")
        self.attachLayout.addWidget(self.pushAttach)
        self.verticalLayout_2.addLayout(self.attachLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.taggedView = QtWidgets.QTableView(DialogAddEditData)
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
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(DialogAddEditData)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.descriptionEdit = QtWidgets.QPlainTextEdit(DialogAddEditData)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.verticalLayout.addWidget(self.descriptionEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAddEditData)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.buttonBox.raise_()
        self.label.setBuddy(self.azimuthEdit)
        self.label_2.setBuddy(self.inclinationEdit)
        self.label_4.setBuddy(self.structureCombo)
        self.label_5.setBuddy(self.descriptionEdit)

        self.retranslateUi(DialogAddEditData)
        self.buttonBox.accepted.connect(DialogAddEditData.accept)
        self.buttonBox.rejected.connect(DialogAddEditData.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAddEditData)
        DialogAddEditData.setTabOrder(self.azimuthEdit, self.inclinationEdit)
        DialogAddEditData.setTabOrder(self.inclinationEdit, self.structureCombo)
        DialogAddEditData.setTabOrder(self.structureCombo, self.buttonBox)
        DialogAddEditData.setTabOrder(self.buttonBox, self.descriptionEdit)

    def retranslateUi(self, DialogAddEditData):
        _translate = QtCore.QCoreApplication.translate
        DialogAddEditData.setWindowTitle(_translate("DialogAddEditData", "Add site"))
        self.label.setText(_translate("DialogAddEditData", "&Azimuth:"))
        self.label_2.setText(_translate("DialogAddEditData", "&Inclination:"))
        self.label_4.setText(_translate("DialogAddEditData", "&Structure:"))
        self.attachLabel.setText(_translate("DialogAddEditData", "Attached:"))
        self.attachErrorLabel.setText(_translate("DialogAddEditData", "Fit error:"))
        self.pushFit.setText(_translate("DialogAddEditData", "Fit"))
        self.pushAttach.setText(_translate("DialogAddEditData", "Detach"))
        self.label_5.setText(_translate("DialogAddEditData", "&Description:"))
