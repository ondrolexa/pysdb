from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets, uic

from .models import unitcol, sitecol, datacol, structurecol, tagcol

_UI_DIR = Path(__file__).parent / "ui"


class DialogAddEditSite(QtWidgets.QDialog):
    def __init__(self, model, action, data=None, parent=None):
        super(DialogAddEditSite, self).__init__(parent)
        if data is None:
            data = [-1, "", 0.0, 0.0, "", None]

        uic.loadUi(_UI_DIR / "addeditsite.ui", self)
        self.unitCombo.setModel(model)
        self.unitCombo.setModelColumn(unitcol["name"])
        # store data
        self.data = data
        # populate widgets
        if action == "Add":
            self.sitenameEdit.setText("")
            self.xcoordEdit.setText("0")
            self.ycoordEdit.setText("0")
            self.descriptionEdit.setPlainText("")
            title = "Add site"
        else:
            self.sitenameEdit.setText(data[sitecol["name"]])
            self.xcoordEdit.setText(str(data[sitecol["x"]]))
            self.ycoordEdit.setText(str(data[sitecol["y"]]))
            self.descriptionEdit.setPlainText(data[sitecol["desc"]])
            title = f"Edit site #{data[sitecol['id']]}"
        # set unit
        if data[sitecol["id_units"]]:
            self.unitCombo.setCurrentIndex(model.id2row[data[sitecol["id_units"]]])
        else:
            self.unitCombo.setCurrentIndex(0)
        # set title
        self.setWindowTitle(
            QtWidgets.QApplication.translate("DialogAddEditSite", title)
        )
        # set validation rules — stored on self to prevent garbage collection
        self.floatval = QtGui.QDoubleValidator()
        self.floatval.setLocale(
            QtCore.QLocale(
                QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates
            )
        )
        self.floatval.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        self.xcoordEdit.setValidator(self.floatval)
        self.ycoordEdit.setValidator(self.floatval)

        self.sitenameEdit.setFocus()

    def accept(self):
        # add site accept check
        if self.sitenameEdit.text():
            self.data[sitecol["name"]] = self.sitenameEdit.text()
            self.data[sitecol["x"]] = float(self.xcoordEdit.text())
            self.data[sitecol["y"]] = float(self.ycoordEdit.text())
            self.data[sitecol["desc"]] = self.descriptionEdit.toPlainText()
            self.data[sitecol["id_units"]] = self.unitCombo.model().row2id[
                self.unitCombo.currentIndex()
            ]
            QtWidgets.QDialog.accept(self)
        else:
            QtWidgets.QMessageBox.warning(
                self, "Add site error", "Sitename cannot be empty!"
            )
            self.sitenameEdit.setFocus()
            return


class DialogAddEditData(QtWidgets.QDialog):
    # datacol = {'id':0,'id_sites':1,'id_struct':2,'azi':3,'inc':4,'struct':5,'desc':6,'tags':7}
    def __init__(
        self,
        model,
        tags,
        attached,
        action,
        data=None,
        parent=None,
    ):
        if data is None:
            data = [-1, -1, None, "", "", "", "", ""]
        super(DialogAddEditData, self).__init__(parent)
        uic.loadUi(_UI_DIR / "addeditdata.ui", self)
        self.structureCombo.setModel(model)
        self.structureCombo.setModelColumn(structurecol["structure"])
        # store data
        self.data = data
        # populate widgets
        if action == "Add":
            self.azimuthEdit.setText("")
            self.inclinationEdit.setText("")
            self.descriptionEdit.setPlainText("")
            title = "Add data"
        else:
            self.azimuthEdit.setText(str(data[datacol["azi"]]))
            self.inclinationEdit.setText(str(data[datacol["inc"]]))
            self.descriptionEdit.setPlainText(data[datacol["desc"]])
            title = f"Edit record #{data[datacol['id']]}"
        # let's add view of the data source we just created:
        self.taggedView.setModel(tags)
        self.taggedView.setColumnHidden(tagcol["id"], True)
        self.taggedView.setColumnHidden(tagcol["name"], True)
        self.taggedView.setColumnHidden(tagcol["desc"], True)
        self.taggedView.resizeColumnToContents(tagcol["check"])
        # set structure
        if data[datacol["id_struct"]]:
            self.structureCombo.setCurrentIndex(
                model.id2row[data[datacol["id_struct"]]]
            )
        # set attach visibility
        self.structure_changed(self.structureCombo.currentIndex())
        # populate attachCombo
        self.attachCombo.addItems([item[1] for item in attached])
        # connect signals
        self.structureCombo.activated.connect(self.structure_changed)
        self.pushAttach.clicked.connect(self.clear_attach)
        self.pushFit.clicked.connect(self.fit_lineplane)

        # set title
        self.setWindowTitle(
            QtWidgets.QApplication.translate("DialogAddEditData", title)
        )
        # set validation rules
        self.azival = QtGui.QDoubleValidator(0.0, 360.0, 1000)
        self.azival.setLocale(
            QtCore.QLocale(
                QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates
            )
        )
        self.azival.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        self.incval = QtGui.QDoubleValidator(0.0, 90.0, 1000)
        self.incval.setLocale(
            QtCore.QLocale(
                QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates
            )
        )
        self.incval.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        self.azimuthEdit.setValidator(self.azival)
        self.inclinationEdit.setValidator(self.incval)

        self.azimuthEdit.selectAll()
        self.azimuthEdit.setFocus()

    def clear_attach(self):
        self.attachCombo.setCurrentIndex(-1)

    def fit_lineplane(self):
        pass

    def structure_changed(self, row):
        if self.structureCombo.model().isplanar(row):
            self.attachLabel.hide()
            self.attachCombo.hide()
            self.pushAttach.hide()
            self.pushFit.hide()
            self.attachErrorLabel.hide()
        else:
            self.attachLabel.show()
            self.attachCombo.show()
            self.pushAttach.show()
            self.pushFit.show()
            self.attachErrorLabel.show()

    def accept(self):
        # add data accept check
        self.data[datacol["id_struct"]] = self.structureCombo.model().row2id[
            self.structureCombo.currentIndex()
        ]
        if (
            self.azival.validate(self.azimuthEdit.text(), 0)[0]
            == QtGui.QValidator.State.Acceptable
        ):
            self.data[datacol["azi"]] = float(self.azimuthEdit.text())
        else:
            QtWidgets.QMessageBox.warning(
                self, "Add site error", "Azimuth must be number between 0-360."
            )
            self.azimuthEdit.setFocus()
            return
        if (
            self.incval.validate(self.inclinationEdit.text(), 0)[0]
            == QtGui.QValidator.State.Acceptable
        ):
            self.data[datacol["inc"]] = float(self.inclinationEdit.text())
        else:
            QtWidgets.QMessageBox.warning(
                self, "Add site error", "Inclinations must be number between 0-90."
            )
            self.inclinationEdit.setFocus()
            return
        self.data[datacol["desc"]] = self.descriptionEdit.toPlainText()
        QtWidgets.QDialog.accept(self)


class DialogAddEditStructure(QtWidgets.QDialog):
    # structurecol = {'id':0,'structure':1,'planar':2,'desc':3,'scode':4,'gcode':5}
    def __init__(self, action, data=None, parent=None):
        super(DialogAddEditStructure, self).__init__(parent)
        if data is None:
            data = [-1, "", 1, "", 0, 0]

        uic.loadUi(_UI_DIR / "addeditstructure.ui", self)
        # store data
        self.data = list(data)
        # populate widgets
        if action == "Add":
            self.structnameEdit.setText("")
            self.scodeEdit.setText("0")
            self.gcodeEdit.setText("0")
            self.descriptionEdit.setPlainText("")
            self.radioPlanar.setChecked(True)
            title = "Add structure"
        else:
            self.structnameEdit.setText(data[structurecol["structure"]])
            self.scodeEdit.setText(str(data[structurecol["scode"]]))
            self.gcodeEdit.setText(str(data[structurecol["gcode"]]))
            self.descriptionEdit.setPlainText(data[structurecol["desc"]])
            if data[structurecol["planar"]]:
                self.radioPlanar.setChecked(True)
            else:
                self.radioLinear.setChecked(True)
            title = f"Edit structure #{data[structurecol['id']]}"
        # set title
        self.setWindowTitle(
            QtWidgets.QApplication.translate("DialogAddEditStructure", title)
        )
        # set validation rules — stored on self to prevent garbage collection
        self.intval = QtGui.QIntValidator()
        self.scodeEdit.setValidator(self.intval)
        self.gcodeEdit.setValidator(self.intval)

        self.structnameEdit.setFocus()

    def accept(self):
        # add structure accept check
        if self.structnameEdit.text():
            self.data[structurecol["structure"]] = self.structnameEdit.text()
            self.data[structurecol["scode"]] = int(self.scodeEdit.text())
            self.data[structurecol["gcode"]] = int(self.gcodeEdit.text())
            self.data[structurecol["desc"]] = self.descriptionEdit.toPlainText()
            if self.radioPlanar.isChecked():
                self.data[structurecol["planar"]] = 1
            else:
                self.data[structurecol["planar"]] = 0
            QtWidgets.QDialog.accept(self)
        else:
            QtWidgets.QMessageBox.warning(
                self, "Add structure error", "Structure cannot be empty!"
            )
            self.structnameEdit.setFocus()
            return


class _NameDescEntityDialog(QtWidgets.QDialog):
    """Base for dialogs that consist of a name field, a description field, and a data list.

    Subclasses must define class attributes _col (column dict) and _entity (str),
    and a property _name_edit returning the name QLineEdit.
    """

    _col = None
    _entity = ""

    @property
    def _name_edit(self):
        raise NotImplementedError

    def accept(self):
        name_edit = self._name_edit
        if name_edit.text():
            self.data[self._col["name"]] = name_edit.text()
            self.data[self._col["desc"]] = self.descriptionEdit.toPlainText()
            QtWidgets.QDialog.accept(self)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                f"Add {self._entity} error",
                f"{self._entity.capitalize()} name cannot be empty!",
            )
            name_edit.setFocus()


class DialogAddEditUnit(_NameDescEntityDialog):
    # unitcol = {'id':0,'name':1,'desc':2}
    _col = unitcol
    _entity = "unit"

    @property
    def _name_edit(self):
        return self.unitnameEdit

    def __init__(self, action, data=None, parent=None):
        super(DialogAddEditUnit, self).__init__(parent)
        if data is None:
            data = [-1, "", ""]

        uic.loadUi(_UI_DIR / "addeditunit.ui", self)
        # store data
        self.data = list(data)
        # populate widgets
        if action == "Add":
            self.unitnameEdit.setText("")
            self.descriptionEdit.setPlainText("")
            title = "Add unit"
        else:
            self.unitnameEdit.setText(data[unitcol["name"]])
            self.descriptionEdit.setPlainText(data[unitcol["desc"]])
            title = f"Edit unit #{data[unitcol['id']]}"
        # set title
        self.setWindowTitle(
            QtWidgets.QApplication.translate("DialogAddEditUnit", title)
        )
        self.unitnameEdit.setFocus()


class DialogAddEditTag(_NameDescEntityDialog):
    # tagcol = {'id':0,'name':1,'desc':2,'check':3}
    _col = tagcol
    _entity = "tag"

    @property
    def _name_edit(self):
        return self.tagnameEdit

    def __init__(self, action, data=None, parent=None):
        super(DialogAddEditTag, self).__init__(parent)
        if data is None:
            data = [-1, "", "", QtCore.Qt.CheckState.Unchecked]

        uic.loadUi(_UI_DIR / "addedittag.ui", self)
        # store data
        self.data = list(data)
        # populate widgets
        if action == "Add":
            self.tagnameEdit.setText("")
            self.descriptionEdit.setPlainText("")
            title = "Add tag"
        else:
            self.tagnameEdit.setText(data[tagcol["name"]])
            self.descriptionEdit.setPlainText(data[tagcol["desc"]])
            title = f"Edit tag #{data[tagcol['id']]}"
        # set title
        self.setWindowTitle(QtWidgets.QApplication.translate("DialogAddEditTag", title))
        self.tagnameEdit.setFocus()


class DialogSDBInfo(QtWidgets.QDialog):
    def __init__(self, info, crs, parent=None):
        super(DialogSDBInfo, self).__init__(parent)

        uic.loadUi(_UI_DIR / "sdbinfo.ui", self)
        self.crs = crs
        # populate widgets
        self.infoEdit.setPlainText(info)
        self.crsEdit.setPlainText(crs)
        self.crsEdit.setFocus()

    def accept(self):
        # add structure accept check
        if self.crsEdit.toPlainText():
            self.crs = self.crsEdit.toPlainText().replace("\n", " ").replace("\r", "")
            QtWidgets.QDialog.accept(self)
        else:
            QtWidgets.QMessageBox.warning(
                self, "Database info error", "CRS cannot be empty!"
            )
            self.crsEdit.setFocus()
            return


class DialogSDBReport(QtWidgets.QDialog):
    def __init__(self, info, parent=None):
        super(DialogSDBReport, self).__init__(parent)

        uic.loadUi(_UI_DIR / "sdbreport.ui", self)
        # populate widgets
        self.reportEdit.setPlainText(info)
        self.reportEdit.setFocus()

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogSaveDiscard(QtWidgets.QDialog):
    # structurecol = {'id':0,'structure':1,'planar':2,'desc':3,'scode':4,'gcode':5}
    def __init__(self, items, message, label, parent=None):
        super(DialogSaveDiscard, self).__init__(parent)

        uic.loadUi(_UI_DIR / "savediscard.ui", self)
        self.messageLabel.setText(message)
        self.checkBox.setText(label)
        self.checkBox.setChecked(False)
        self.comboBox.clear()
        self.comboBox.addItems(items)
        self.setWindowTitle(
            QtWidgets.QApplication.translate("DialogSaveDiscard", "Delete structure")
        )

    def checked(self):
        return self.checkBox.isChecked()

    def selected(self):
        return self.comboBox.currentIndex()

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogSiteFilter(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super(DialogSiteFilter, self).__init__(parent)

        uic.loadUi(_UI_DIR / "sitefilter.ui", self)
        # set unit combo
        self.unitCombo.setModel(model)
        self.unitCombo.setModelColumn(1)
        self.unitCombo.activated.connect(self.unit_sel)
        self.nameEdit.textChanged.connect(self.name_sel)

    def unit_sel(self, index):
        self.radioUnit.setChecked(True)

    def name_sel(self, index):
        self.radioName.setChecked(True)

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogDataFilter(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super(DialogDataFilter, self).__init__(parent)

        uic.loadUi(_UI_DIR / "datafilter.ui", self)
        # set unit combo
        self.structureCombo.setModel(model)
        self.structureCombo.setModelColumn(1)
        self.structureCombo.activated.connect(self.struct_sel)
        self.nameTag.textChanged.connect(self.tag_sel)

    def struct_sel(self, index):
        self.radioStructure.setChecked(True)

    def tag_sel(self, index):
        self.radioTag.setChecked(True)

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogSelectUnit(QtWidgets.QDialog):
    def __init__(self, model, parent=None):
        super(DialogSelectUnit, self).__init__(parent)

        uic.loadUi(_UI_DIR / "selectunit.ui", self)
        # set unit combo
        self.unitCombo.setModel(model)
        self.unitCombo.setModelColumn(1)

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogMultiEditData(QtWidgets.QDialog):
    # datacol = {'id':0,'id_sites':1,'id_struct':2,'azi':3,'inc':4,'struct':5,'desc':6,'tags':7}
    def __init__(self, model, tags, parent=None):
        super(DialogMultiEditData, self).__init__(parent)
        uic.loadUi(_UI_DIR / "multieditdata.ui", self)
        self.structureCombo.setModel(model)
        self.structureCombo.setModelColumn(structurecol["structure"])
        # let's add view of the data source we just created:
        self.taggedView.setModel(tags)
        self.taggedView.setColumnHidden(tagcol["id"], True)
        self.taggedView.setColumnHidden(tagcol["name"], True)
        self.taggedView.setColumnHidden(tagcol["desc"], True)
        self.taggedView.resizeColumnToContents(tagcol["check"])
        # set title
        # self.setWindowTitle(QtWidgets.QApplication.translate("DialogAddEditData", title))
        self.structureCombo.setFocus()

    def accept(self):
        QtWidgets.QDialog.accept(self)


class DialogImportSetting(QtWidgets.QDialog):
    def __init__(self, model, properties, geom=True, parent=None):
        super(DialogImportSetting, self).__init__(parent)

        uic.loadUi(_UI_DIR / "importsitesfile.ui", self)
        # set combos
        lprops = [p.lower() for p in properties]
        self.siteComboFile.addItems(properties)
        cands = [e for e in lprops if e.startswith("name") | e.startswith("site")]
        if cands:
            self.siteComboFile.setCurrentIndex(lprops.index(cands[0]))
        if geom:
            self.lonComboFile.addItems(properties)
            cands = [e for e in lprops if e.startswith("lon") | e.startswith("x")]
            if cands:
                self.lonComboFile.setCurrentIndex(lprops.index(cands[0]))
            self.latComboFile.addItems(properties)
            cands = [e for e in lprops if e.startswith("lat") | e.startswith("y")]
            if cands:
                self.latComboFile.setCurrentIndex(lprops.index(cands[0]))
        else:
            self.lonComboFile.setEnabled(False)
            self.latComboFile.setEnabled(False)
        self.unitComboFile.addItems(properties)
        cands = [e for e in lprops if e.startswith("unit") | e.startswith("domain")]
        if cands:
            self.unitComboFile.setCurrentIndex(lprops.index(cands[0]))
        self.unitCombo.setModel(model)
        self.unitCombo.setModelColumn(1)

    def accept(self):
        QtWidgets.QDialog.accept(self)
