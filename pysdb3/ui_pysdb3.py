# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pysdb3/ui/pysdb3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 580)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pysdb3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.siteFrame = QtWidgets.QFrame(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteFrame.sizePolicy().hasHeightForWidth())
        self.siteFrame.setSizePolicy(sizePolicy)
        self.siteFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.siteFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.siteFrame.setObjectName("siteFrame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.siteFrame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.sitesView = QtWidgets.QTableView(self.siteFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sitesView.sizePolicy().hasHeightForWidth())
        self.sitesView.setSizePolicy(sizePolicy)
        self.sitesView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.sitesView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.sitesView.setObjectName("sitesView")
        self.sitesView.horizontalHeader().setStretchLastSection(True)
        self.sitesView.verticalHeader().setVisible(False)
        self.sitesView.verticalHeader().setDefaultSectionSize(22)
        self.verticalLayout_7.addWidget(self.sitesView)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushSiteEdit = QtWidgets.QPushButton(self.siteFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSiteEdit.sizePolicy().hasHeightForWidth())
        self.pushSiteEdit.setSizePolicy(sizePolicy)
        self.pushSiteEdit.setObjectName("pushSiteEdit")
        self.gridLayout.addWidget(self.pushSiteEdit, 0, 0, 1, 1)
        self.pushSiteFilter = QtWidgets.QPushButton(self.siteFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSiteFilter.sizePolicy().hasHeightForWidth())
        self.pushSiteFilter.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/edit-find.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushSiteFilter.setIcon(icon1)
        self.pushSiteFilter.setCheckable(True)
        self.pushSiteFilter.setObjectName("pushSiteFilter")
        self.gridLayout.addWidget(self.pushSiteFilter, 0, 1, 1, 1)
        self.pushSiteAdd = QtWidgets.QPushButton(self.siteFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSiteAdd.sizePolicy().hasHeightForWidth())
        self.pushSiteAdd.setSizePolicy(sizePolicy)
        self.pushSiteAdd.setObjectName("pushSiteAdd")
        self.gridLayout.addWidget(self.pushSiteAdd, 1, 0, 1, 1)
        self.pushSiteRemove = QtWidgets.QPushButton(self.siteFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSiteRemove.sizePolicy().hasHeightForWidth())
        self.pushSiteRemove.setSizePolicy(sizePolicy)
        self.pushSiteRemove.setObjectName("pushSiteRemove")
        self.gridLayout.addWidget(self.pushSiteRemove, 1, 1, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout)
        self.gridLayout_3.addWidget(self.siteFrame, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.East)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_data = QtWidgets.QWidget()
        self.tab_data.setObjectName("tab_data")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_data)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.dataView = QtWidgets.QTableView(self.tab_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataView.sizePolicy().hasHeightForWidth())
        self.dataView.setSizePolicy(sizePolicy)
        self.dataView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.dataView.setObjectName("dataView")
        self.dataView.horizontalHeader().setStretchLastSection(True)
        self.dataView.verticalHeader().setVisible(False)
        self.dataView.verticalHeader().setDefaultSectionSize(22)
        self.verticalLayout_8.addWidget(self.dataView)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushDataEdit = QtWidgets.QPushButton(self.tab_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushDataEdit.sizePolicy().hasHeightForWidth())
        self.pushDataEdit.setSizePolicy(sizePolicy)
        self.pushDataEdit.setObjectName("pushDataEdit")
        self.horizontalLayout_5.addWidget(self.pushDataEdit)
        self.pushDataAdd = QtWidgets.QPushButton(self.tab_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushDataAdd.sizePolicy().hasHeightForWidth())
        self.pushDataAdd.setSizePolicy(sizePolicy)
        self.pushDataAdd.setObjectName("pushDataAdd")
        self.horizontalLayout_5.addWidget(self.pushDataAdd)
        self.pushDataRemove = QtWidgets.QPushButton(self.tab_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushDataRemove.sizePolicy().hasHeightForWidth())
        self.pushDataRemove.setSizePolicy(sizePolicy)
        self.pushDataRemove.setObjectName("pushDataRemove")
        self.horizontalLayout_5.addWidget(self.pushDataRemove)
        self.pushDataFilter = QtWidgets.QPushButton(self.tab_data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushDataFilter.sizePolicy().hasHeightForWidth())
        self.pushDataFilter.setSizePolicy(sizePolicy)
        self.pushDataFilter.setIcon(icon1)
        self.pushDataFilter.setCheckable(True)
        self.pushDataFilter.setObjectName("pushDataFilter")
        self.horizontalLayout_5.addWidget(self.pushDataFilter)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_data, "")
        self.tab_images = QtWidgets.QWidget()
        self.tab_images.setObjectName("tab_images")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_images)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.imagesWidget = QtWidgets.QListWidget(self.tab_images)
        self.imagesWidget.setObjectName("imagesWidget")
        self.verticalLayout_9.addWidget(self.imagesWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushImageAdd = QtWidgets.QPushButton(self.tab_images)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushImageAdd.sizePolicy().hasHeightForWidth())
        self.pushImageAdd.setSizePolicy(sizePolicy)
        self.pushImageAdd.setObjectName("pushImageAdd")
        self.horizontalLayout_6.addWidget(self.pushImageAdd)
        self.pushImageRemove = QtWidgets.QPushButton(self.tab_images)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushImageRemove.sizePolicy().hasHeightForWidth())
        self.pushImageRemove.setSizePolicy(sizePolicy)
        self.pushImageRemove.setObjectName("pushImageRemove")
        self.horizontalLayout_6.addWidget(self.pushImageRemove)
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_images)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_9.sizePolicy().hasHeightForWidth())
        self.pushButton_9.setSizePolicy(sizePolicy)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_6.addWidget(self.pushButton_9)
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_images)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_6.addWidget(self.pushButton_10)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab_images, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent_databases = QtWidgets.QMenu(self.menuFile)
        self.menuRecent_databases.setObjectName("menuRecent_databases")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuImport_sites = QtWidgets.QMenu(self.menuTools)
        self.menuImport_sites.setObjectName("menuImport_sites")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockStructures = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.dockStructures.sizePolicy().hasHeightForWidth())
        self.dockStructures.setSizePolicy(sizePolicy)
        self.dockStructures.setMinimumSize(QtCore.QSize(200, 158))
        self.dockStructures.setMaximumSize(QtCore.QSize(250, 524287))
        self.dockStructures.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockStructures.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockStructures.setObjectName("dockStructures")
        self.dockStructuresContents = QtWidgets.QWidget()
        self.dockStructuresContents.setObjectName("dockStructuresContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockStructuresContents)
        self.verticalLayout_4.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.structuresView = QtWidgets.QTableView(self.dockStructuresContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.structuresView.sizePolicy().hasHeightForWidth())
        self.structuresView.setSizePolicy(sizePolicy)
        self.structuresView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.structuresView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.structuresView.setObjectName("structuresView")
        self.structuresView.horizontalHeader().setVisible(False)
        self.structuresView.horizontalHeader().setStretchLastSection(True)
        self.structuresView.verticalHeader().setVisible(False)
        self.structuresView.verticalHeader().setDefaultSectionSize(18)
        self.verticalLayout.addWidget(self.structuresView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushStructuresAdd = QtWidgets.QPushButton(self.dockStructuresContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushStructuresAdd.sizePolicy().hasHeightForWidth())
        self.pushStructuresAdd.setSizePolicy(sizePolicy)
        self.pushStructuresAdd.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/list-add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushStructuresAdd.setIcon(icon2)
        self.pushStructuresAdd.setObjectName("pushStructuresAdd")
        self.horizontalLayout.addWidget(self.pushStructuresAdd)
        self.pushStructuresRemove = QtWidgets.QPushButton(self.dockStructuresContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushStructuresRemove.sizePolicy().hasHeightForWidth())
        self.pushStructuresRemove.setSizePolicy(sizePolicy)
        self.pushStructuresRemove.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/list-remove.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushStructuresRemove.setIcon(icon3)
        self.pushStructuresRemove.setObjectName("pushStructuresRemove")
        self.horizontalLayout.addWidget(self.pushStructuresRemove)
        self.pushStructuresUp = QtWidgets.QPushButton(self.dockStructuresContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushStructuresUp.sizePolicy().hasHeightForWidth())
        self.pushStructuresUp.setSizePolicy(sizePolicy)
        self.pushStructuresUp.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/go-up.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushStructuresUp.setIcon(icon4)
        self.pushStructuresUp.setObjectName("pushStructuresUp")
        self.horizontalLayout.addWidget(self.pushStructuresUp)
        self.pushStructuresDown = QtWidgets.QPushButton(self.dockStructuresContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushStructuresDown.sizePolicy().hasHeightForWidth())
        self.pushStructuresDown.setSizePolicy(sizePolicy)
        self.pushStructuresDown.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/go-down.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushStructuresDown.setIcon(icon5)
        self.pushStructuresDown.setObjectName("pushStructuresDown")
        self.horizontalLayout.addWidget(self.pushStructuresDown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.dockStructures.setWidget(self.dockStructuresContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockStructures)
        self.dockUnits = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.dockUnits.sizePolicy().hasHeightForWidth())
        self.dockUnits.setSizePolicy(sizePolicy)
        self.dockUnits.setMinimumSize(QtCore.QSize(200, 158))
        self.dockUnits.setMaximumSize(QtCore.QSize(250, 524287))
        self.dockUnits.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockUnits.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockUnits.setObjectName("dockUnits")
        self.dockUnitsContents = QtWidgets.QWidget()
        self.dockUnitsContents.setObjectName("dockUnitsContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.dockUnitsContents)
        self.verticalLayout_5.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.unitsView = QtWidgets.QTableView(self.dockUnitsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unitsView.sizePolicy().hasHeightForWidth())
        self.unitsView.setSizePolicy(sizePolicy)
        self.unitsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.unitsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.unitsView.setObjectName("unitsView")
        self.unitsView.horizontalHeader().setVisible(False)
        self.unitsView.horizontalHeader().setStretchLastSection(True)
        self.unitsView.verticalHeader().setVisible(False)
        self.unitsView.verticalHeader().setDefaultSectionSize(18)
        self.verticalLayout_2.addWidget(self.unitsView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushUnitsAdd = QtWidgets.QPushButton(self.dockUnitsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushUnitsAdd.sizePolicy().hasHeightForWidth())
        self.pushUnitsAdd.setSizePolicy(sizePolicy)
        self.pushUnitsAdd.setText("")
        self.pushUnitsAdd.setIcon(icon2)
        self.pushUnitsAdd.setObjectName("pushUnitsAdd")
        self.horizontalLayout_2.addWidget(self.pushUnitsAdd)
        self.pushUnitsRemove = QtWidgets.QPushButton(self.dockUnitsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushUnitsRemove.sizePolicy().hasHeightForWidth())
        self.pushUnitsRemove.setSizePolicy(sizePolicy)
        self.pushUnitsRemove.setText("")
        self.pushUnitsRemove.setIcon(icon3)
        self.pushUnitsRemove.setObjectName("pushUnitsRemove")
        self.horizontalLayout_2.addWidget(self.pushUnitsRemove)
        self.pushUnitsUp = QtWidgets.QPushButton(self.dockUnitsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushUnitsUp.sizePolicy().hasHeightForWidth())
        self.pushUnitsUp.setSizePolicy(sizePolicy)
        self.pushUnitsUp.setText("")
        self.pushUnitsUp.setIcon(icon4)
        self.pushUnitsUp.setObjectName("pushUnitsUp")
        self.horizontalLayout_2.addWidget(self.pushUnitsUp)
        self.pushUnitsDown = QtWidgets.QPushButton(self.dockUnitsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushUnitsDown.sizePolicy().hasHeightForWidth())
        self.pushUnitsDown.setSizePolicy(sizePolicy)
        self.pushUnitsDown.setText("")
        self.pushUnitsDown.setIcon(icon5)
        self.pushUnitsDown.setObjectName("pushUnitsDown")
        self.horizontalLayout_2.addWidget(self.pushUnitsDown)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.dockUnits.setWidget(self.dockUnitsContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockUnits)
        self.dockTags = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.dockTags.sizePolicy().hasHeightForWidth())
        self.dockTags.setSizePolicy(sizePolicy)
        self.dockTags.setMinimumSize(QtCore.QSize(200, 158))
        self.dockTags.setMaximumSize(QtCore.QSize(250, 524287))
        self.dockTags.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.dockTags.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockTags.setObjectName("dockTags")
        self.dockTagsContents = QtWidgets.QWidget()
        self.dockTagsContents.setObjectName("dockTagsContents")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dockTagsContents)
        self.verticalLayout_6.setContentsMargins(-1, -1, 9, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tagsView = QtWidgets.QTableView(self.dockTagsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsView.sizePolicy().hasHeightForWidth())
        self.tagsView.setSizePolicy(sizePolicy)
        self.tagsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tagsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tagsView.setObjectName("tagsView")
        self.tagsView.horizontalHeader().setVisible(False)
        self.tagsView.horizontalHeader().setStretchLastSection(True)
        self.tagsView.verticalHeader().setVisible(False)
        self.tagsView.verticalHeader().setDefaultSectionSize(18)
        self.verticalLayout_3.addWidget(self.tagsView)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushTagsAdd = QtWidgets.QPushButton(self.dockTagsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushTagsAdd.sizePolicy().hasHeightForWidth())
        self.pushTagsAdd.setSizePolicy(sizePolicy)
        self.pushTagsAdd.setText("")
        self.pushTagsAdd.setIcon(icon2)
        self.pushTagsAdd.setObjectName("pushTagsAdd")
        self.horizontalLayout_3.addWidget(self.pushTagsAdd)
        self.pushTagsRemove = QtWidgets.QPushButton(self.dockTagsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushTagsRemove.sizePolicy().hasHeightForWidth())
        self.pushTagsRemove.setSizePolicy(sizePolicy)
        self.pushTagsRemove.setText("")
        self.pushTagsRemove.setIcon(icon3)
        self.pushTagsRemove.setObjectName("pushTagsRemove")
        self.horizontalLayout_3.addWidget(self.pushTagsRemove)
        self.pushTagsUp = QtWidgets.QPushButton(self.dockTagsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushTagsUp.sizePolicy().hasHeightForWidth())
        self.pushTagsUp.setSizePolicy(sizePolicy)
        self.pushTagsUp.setText("")
        self.pushTagsUp.setIcon(icon4)
        self.pushTagsUp.setObjectName("pushTagsUp")
        self.horizontalLayout_3.addWidget(self.pushTagsUp)
        self.pushTagsDown = QtWidgets.QPushButton(self.dockTagsContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushTagsDown.sizePolicy().hasHeightForWidth())
        self.pushTagsDown.setSizePolicy(sizePolicy)
        self.pushTagsDown.setText("")
        self.pushTagsDown.setIcon(icon5)
        self.pushTagsDown.setObjectName("pushTagsDown")
        self.horizontalLayout_3.addWidget(self.pushTagsDown)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_6.addLayout(self.verticalLayout_3)
        self.dockTags.setWidget(self.dockTagsContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockTags)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/document-new.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon6)
        self.actionNew.setIconVisibleInMenu(True)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/document-open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon7)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/document-save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon8)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/document-save-as.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_as.setIcon(icon9)
        self.actionSave_as.setIconVisibleInMenu(True)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_template = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/text-x-generic-template.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_template.setIcon(icon10)
        self.actionSave_template.setIconVisibleInMenu(True)
        self.actionSave_template.setObjectName("actionSave_template")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionInformation = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/dialog-information.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionInformation.setIcon(icon11)
        self.actionInformation.setIconVisibleInMenu(True)
        self.actionInformation.setObjectName("actionInformation")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/system-log-out.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon12)
        self.actionQuit.setIconVisibleInMenu(True)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAa = QtWidgets.QAction(MainWindow)
        self.actionAa.setObjectName("actionAa")
        self.actionFrom_GPX = QtWidgets.QAction(MainWindow)
        self.actionFrom_GPX.setObjectName("actionFrom_GPX")
        self.actionFrom_CSV = QtWidgets.QAction(MainWindow)
        self.actionFrom_CSV.setObjectName("actionFrom_CSV")
        self.actionFlush_images = QtWidgets.QAction(MainWindow)
        self.actionFlush_images.setObjectName("actionFlush_images")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuRecent_databases.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionSave_template)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionInformation)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuImport_sites.addAction(self.actionFrom_GPX)
        self.menuImport_sites.addAction(self.actionFrom_CSV)
        self.menuTools.addAction(self.menuImport_sites.menuAction())
        self.menuTools.addAction(self.actionFlush_images)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionInformation)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PySDB Structural database"))
        self.pushSiteEdit.setText(_translate("MainWindow", "Edit"))
        self.pushSiteFilter.setText(_translate("MainWindow", "Filter"))
        self.pushSiteAdd.setText(_translate("MainWindow", "Add"))
        self.pushSiteRemove.setText(_translate("MainWindow", "Remove"))
        self.pushDataEdit.setText(_translate("MainWindow", "Edit"))
        self.pushDataAdd.setText(_translate("MainWindow", "Add"))
        self.pushDataRemove.setText(_translate("MainWindow", "Remove"))
        self.pushDataFilter.setText(_translate("MainWindow", "Filter"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), _translate("MainWindow", "Data"))
        self.pushImageAdd.setText(_translate("MainWindow", "Add"))
        self.pushImageRemove.setText(_translate("MainWindow", "Remove"))
        self.pushButton_9.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_10.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_images), _translate("MainWindow", "Images"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuRecent_databases.setTitle(_translate("MainWindow", "Recent databases"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuImport_sites.setTitle(_translate("MainWindow", "Import sites"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.dockStructures.setWindowTitle(_translate("MainWindow", "Structures"))
        self.dockUnits.setWindowTitle(_translate("MainWindow", "Units"))
        self.dockTags.setWindowTitle(_translate("MainWindow", "Tags"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Toolbar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setToolTip(_translate("MainWindow", "Create new PySDB database"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open database"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open existing PySDB database"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save PySDB database"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionSave_template.setText(_translate("MainWindow", "Save template"))
        self.actionSave_template.setToolTip(_translate("MainWindow", "Save PySDB database template without data"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        self.actionInformation.setText(_translate("MainWindow", "Information"))
        self.actionInformation.setToolTip(_translate("MainWindow", "Information about PySDB database"))
        self.actionInformation.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit PySDB"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAa.setText(_translate("MainWindow", "aa"))
        self.actionFrom_GPX.setText(_translate("MainWindow", "From GPX"))
        self.actionFrom_CSV.setText(_translate("MainWindow", "From CSV"))
        self.actionFlush_images.setText(_translate("MainWindow", "Flush images"))

from . import pysdb3_rc
