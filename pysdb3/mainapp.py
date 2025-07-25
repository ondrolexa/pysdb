import sys
import os
import datetime
import sqlite3
from pathlib import Path
from lxml import etree

from PyQt5 import QtCore, QtWidgets

from .models import (
    SCHEMA,
    DEFDATA,
    sitecol,
    datacol,
    structurecol,
    unitcol,
    tagcol,
    SiteModel,
    DataModel,
    StructureModel,
    UnitModel,
    TagModel,
)
from .dialogs import (
    DialogImportSetting,
    DialogSDBInfo,
    DialogSDBReport,
    DialogSiteFilter,
    DialogDataFilter,
    DialogSelectUnit,
    DialogAddEditSite,
    DialogAddEditData,
    DialogMultiEditData,
    DialogAddEditStructure,
    DialogSaveDiscard,
    DialogAddEditUnit,
    DialogAddEditTag,
)
from .ui_pysdb3 import Ui_MainWindow

__version__ = "3.2.1"
__about__ = """<b>PySDB - structural database manager v.{}</b>
               <p>Copyright (c) 2021-2025 Ondrej Lexa</p>"""


class MainWindow(QtWidgets.QMainWindow):
    """Our application maion window."""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # connect actions
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionOpen.triggered.connect(self.openFileSDB)
        self.ui.actionNew.triggered.connect(self.newFileSDB)
        self.ui.actionInformation.triggered.connect(
            lambda: self.check_action(self.infoSDB)
        )
        self.ui.actionSave.triggered.connect(
            lambda: self.check_action(self.saveFileSDB)
        )
        self.ui.actionSave_as.triggered.connect(
            lambda: self.check_action(self.saveAsSDB)
        )
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionFrom_GPX.triggered.connect(
            lambda: self.check_action(self.importSitesFromGPX)
        )
        self.ui.actionFrom_GeoJSON.triggered.connect(
            lambda: self.check_action(self.importSitesFromGeoJSON)
        )
        self.ui.actionFrom_CSV.triggered.connect(
            lambda: self.check_action(self.importSitesFromCSV)
        )
        self.ui.actionCompact_database.triggered.connect(
            lambda: self.check_action(self.compactDatabase)
        )
        # siteview
        self.ui.pushSiteAdd.clicked.connect(lambda: self.check_action(self.addSiteDlg))
        self.ui.pushSiteEdit.clicked.connect(
            lambda: self.check_action(self.editSiteDlg)
        )
        self.ui.pushSiteRemove.clicked.connect(
            lambda: self.check_action(self.removeSiteDlg)
        )
        self.ui.pushSiteFilter.clicked.connect(
            lambda: self.check_action(self.filterSiteDlg)
        )
        self.ui.sitesView.doubleClicked.connect(self.editSiteDlg)
        # dataview
        self.ui.pushDataAdd.clicked.connect(lambda: self.check_action(self.addDataDlg))
        self.ui.pushDataEdit.clicked.connect(
            lambda: self.check_action(self.editDataDlg)
        )
        self.ui.pushDataRemove.clicked.connect(
            lambda: self.check_action(self.removeDataDlg)
        )
        self.ui.pushDataFilter.clicked.connect(
            lambda: self.check_action(self.filterDataDlg)
        )
        self.ui.dataView.doubleClicked.connect(self.editDataDlg)
        # structureview
        self.ui.pushStructuresAdd.clicked.connect(
            lambda: self.check_action(self.addStructureDlg)
        )
        self.ui.pushStructuresRemove.clicked.connect(
            lambda: self.check_action(self.removeStructureDlg)
        )
        self.ui.pushStructuresUp.clicked.connect(
            lambda: self.check_action(self.moveStructureUp)
        )
        self.ui.pushStructuresDown.clicked.connect(
            lambda: self.check_action(self.moveStructureDown)
        )
        self.ui.structuresView.doubleClicked.connect(self.editStructureDlg)
        # unitview
        self.ui.pushUnitsAdd.clicked.connect(lambda: self.check_action(self.addUnitDlg))
        self.ui.pushUnitsRemove.clicked.connect(
            lambda: self.check_action(self.removeUnitDlg)
        )
        self.ui.pushUnitsUp.clicked.connect(lambda: self.check_action(self.moveUnitUp))
        self.ui.pushUnitsDown.clicked.connect(
            lambda: self.check_action(self.moveUnitDown)
        )
        self.ui.unitsView.doubleClicked.connect(self.editUnitDlg)
        # tagview
        self.ui.pushTagsAdd.clicked.connect(lambda: self.check_action(self.addTagDlg))
        self.ui.pushTagsRemove.clicked.connect(
            lambda: self.check_action(self.removeTagDlg)
        )
        self.ui.pushTagsUp.clicked.connect(lambda: self.check_action(self.moveTagUp))
        self.ui.pushTagsDown.clicked.connect(
            lambda: self.check_action(self.moveTagDown)
        )
        self.ui.tagsView.doubleClicked.connect(self.editTagDlg)
        # docks
        self.ui.menuView.addAction(self.ui.dockUnits.toggleViewAction())
        self.ui.menuView.addAction(self.ui.dockStructures.toggleViewAction())
        self.ui.menuView.addAction(self.ui.dockTags.toggleViewAction())
        self.ui.menuView.addAction(self.ui.toolBar.toggleViewAction())

        self.connected = False
        self.changed = False

        # own sorting tracking
        self.sortorder = 0

        # load and apply settings
        self.app_settings()
        self.populate_recent()

        # get ready
        self.statusBar().showMessage("Ready", 5000)

    @property
    def changed(self):
        return self._changed

    @changed.setter
    def changed(self, val):
        self._changed = val
        title = QtWidgets.QApplication.translate(
            "MainWindow", "PySDB Structural database"
        )
        if self.connected:
            if self.recent:
                title += " - {}".format(os.path.basename(self.recent[0]))
        if val:
            title += "*"
        self.setWindowTitle(title)

    def app_settings(self, write=False):
        settings = QtCore.QSettings("LX", "pysdb")
        if write:
            settings.setValue("lastdir", str(self.lastdir))
            settings.beginWriteArray("recent")
            for ix, f in enumerate(self.recent):
                settings.setArrayIndex(ix)
                settings.setValue("sdbfile", str(f))
            settings.endArray()
        else:
            self.lastdir = Path(settings.value("lastdir", str(Path.home()), type=str))
            self.recent = []
            n = settings.beginReadArray("recent")
            for ix in range(n):
                settings.setArrayIndex(ix)
                self.recent.append(Path(settings.value("sdbfile", type=str)))
            settings.endArray()

    def populate_recent(self):
        self.ui.menuRecent_databases.clear()
        for p in self.recent:
            self.ui.menuRecent_databases.addAction(
                p.name, lambda p=p: self.openFileSDB(False, p)
            )

    def about(self):
        """Popup a box with about message."""
        QtWidgets.QMessageBox.about(self, "About PySDB", __about__.format(__version__))

    def closeEvent(self, event):
        if self.changed:
            if (
                QtWidgets.QMessageBox.question(
                    self,
                    "Question",
                    "Are you sure you want to exit the program and lost all changes?",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No,
                )
                == QtWidgets.QMessageBox.Yes
            ):
                if self.connected:
                    self.conn.rollback()
                    self.conn.close()
                self.app_settings(write=True)
                event.accept()
            else:
                event.ignore()
        else:
            self.app_settings(write=True)
            event.accept()

    def check_action(self, action):
        if self.connected:
            action()

    def addtorecent(self, p):
        if p in self.recent:
            self.recent.pop(self.recent.index(p))
        self.recent.insert(0, p)
        if len(self.recent) > 15:
            self.recent = self.recent[:15]
        self.populate_recent()

    def openFileSDB(self, checked, p=None):
        if p is None:
            file, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Open file",
                str(self.lastdir),
                "SDB database (*.sdb);;All Files (*)",
            )
            if file == "":
                return
            p = Path(file)
        if p.is_file():
            self.connectDatabase(p)
            self.lastdir = p.parent
            self.addtorecent(p)
            self.changed = False
        else:
            QtWidgets.QMessageBox.warning(
                self, "File error", "Database {} does not exists !".format(p.name)
            )
            if p in self.recent:
                self.recent.pop(self.recent.index(p))
                self.populate_recent()

    def newFileSDB(self):
        if self.connected:
            if self.changed:
                if (
                    QtWidgets.QMessageBox.question(
                        self,
                        "Question",
                        "Do you want to save all changes?",
                        QtWidgets.QMessageBox.Yes,
                        QtWidgets.QMessageBox.No,
                    )
                    == QtWidgets.QMessageBox.Yes
                ):
                    self.dbcommit()
                else:
                    self.conn.rollback()
            self.conn.close()
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "New database", ".", "SDB database (*.sdb)"
        )
        if fname:
            p = Path(fname)
            if not p.suffix:
                p = p.with_suffix(".sdb")
            self.conn = sqlite3.connect(p)
            self.conn.text_factory = str
            # Create schema of database
            for sql in SCHEMA.splitlines():
                self.conn.execute(sql)
            # Insert metadata
            self.conn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)", ("version", __version__)
            )
            self.conn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)", ("crs", "EPSG:4326")
            )
            self.conn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("created", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
            self.conn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("updated", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
            self.conn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("accessed", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
            # Insert default data from template
            for sql in DEFDATA.splitlines():
                self.conn.execute(sql)
            # commit
            self.dbcommit()
            self.connectDatabase(p)
            self.addtorecent(p)
            self.changed = False

    def importSitesFromGPX(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open GPX file", str(self.lastdir), "GPX file (*.gpx);;All Files (*)"
        )
        fname = Path(file)
        if fname.is_file():
            NSMAP = {"gpx": "http://www.topografix.com/GPX/1/1"}
            tree = etree.parse(str(fname))
            wpts = tree.findall("gpx:wpt", namespaces=NSMAP)
            sites = []
            if self.selectunitdlg.exec_():
                defunit_id = self.units.row2id[
                    self.selectunitdlg.ui.unitCombo.currentIndex()
                ]
                for elem in wpts:
                    sites.append(
                        (
                            elem.find("gpx:name", namespaces=NSMAP).text,  # name
                            float(elem.attrib["lon"]),  # x_coord
                            float(elem.attrib["lat"]),  # y_coord
                            "",  # description
                            defunit_id,
                        )
                    )  # id_units
                self.importSites(
                    sites,
                    self.selectunitdlg.ui.updateCoords.isChecked(),
                    self.selectunitdlg.ui.updateUnits.isChecked(),
                )

    def importSitesFromCSV(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open CSV file",
            str(self.lastdir),
            "CSV file (*.csv);;All Files (*)",
        )
        fname = Path(file)
        if fname.is_file():
            import csv

            with fname.open() as src:
                sample = src.read(1024)
                dialect = csv.Sniffer().sniff(sample)
                has_header = csv.Sniffer().has_header(sample)
                src.seek(0)
                # Create a new reader object using the CSV dialect
                data = list(csv.reader(src, dialect=dialect))
                if has_header:
                    columns = data[0]
                    data = data[1:]
                else:
                    columns = [f"Col {n + 1}" for n in range(len(data[0]))]
                sites = []
                propsdlg = DialogImportSetting(self.units, columns, geom=True)
                if propsdlg.exec_():
                    if propsdlg.ui.radioUnitExisting.isChecked():
                        unit_id = self.units.row2id[
                            propsdlg.ui.unitCombo.currentIndex()
                        ]
                    for row in data:
                        x = float(row[propsdlg.ui.lonComboFile.currentIndex()])
                        y = float(row[propsdlg.ui.latComboFile.currentIndex()])
                        sname = str(row[propsdlg.ui.siteComboFile.currentIndex()])
                        skip_unit = (
                            propsdlg.ui.updateCoords.isChecked()
                            and not propsdlg.ui.updateUnits.isChecked()
                        )
                        if propsdlg.ui.radioUnitFile.isChecked() and not skip_unit:
                            uname = str(row[propsdlg.ui.unitComboFile.currentIndex()])
                            res = self.conn.execute(
                                "SELECT id FROM units WHERE name=?",
                                (uname,),
                            ).fetchall()
                            if res:
                                unit_id = res[0][0]
                            else:
                                cur = self.db_addUnit([-1, uname, ""])
                                unit_id = cur.lastrowid
                                self.units.appendRow([unit_id, uname, ""])
                        sites.append(
                            (
                                sname,  # name
                                x,  # x_coord
                                y,  # y_coord
                                "",  # description
                                unit_id,  # id_units
                            )
                        )
                    self.units.updateIndex()
                    self.importSites(
                        sites,
                        propsdlg.ui.updateCoords.isChecked(),
                        propsdlg.ui.updateUnits.isChecked(),
                    )

    def importSitesFromGeoJSON(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open GeoJSON file",
            str(self.lastdir),
            "GeoJSON file (*.geojson);;All Files (*)",
        )
        fname = Path(file)
        if fname.is_file():
            import json

            with fname.open() as src:
                data = json.load(src)

            if data["type"] == "FeatureCollection":
                if len(data["features"]) > 0:
                    if data["features"][0]["geometry"]["type"] == "Point":
                        props = list(data["features"][0]["properties"].keys())
                        sites = []
                        propsdlg = DialogImportSetting(self.units, props, geom=False)
                        if propsdlg.exec_():
                            if propsdlg.ui.radioUnitExisting.isChecked():
                                unit_id = self.units.row2id[
                                    propsdlg.ui.unitCombo.currentIndex()
                                ]
                            for feature in data["features"]:
                                fp = feature["properties"]
                                if len(feature["geometry"]["coordinates"]) > 2:
                                    x, y, _ = feature["geometry"]["coordinates"]
                                else:
                                    x, y = feature["geometry"]["coordinates"]
                                sname = fp[propsdlg.ui.siteComboFile.currentText()]
                                skip_unit = (
                                    propsdlg.ui.updateCoords.isChecked()
                                    and not propsdlg.ui.updateUnits.isChecked()
                                )
                                if (
                                    propsdlg.ui.radioUnitFile.isChecked()
                                    and not skip_unit
                                ):
                                    uname = fp[propsdlg.ui.unitComboFile.currentText()]
                                    res = self.conn.execute(
                                        "SELECT id FROM units WHERE name=?",
                                        (uname,),
                                    ).fetchall()
                                    if res:
                                        unit_id = res[0][0]
                                    else:
                                        cur = self.db_addUnit([-1, uname, ""])
                                        unit_id = cur.lastrowid
                                        self.units.appendRow([unit_id, uname, ""])
                                sites.append(
                                    (
                                        sname,  # name
                                        x,  # x_coord
                                        y,  # y_coord
                                        "",  # description
                                        unit_id,  # id_units
                                    )
                                )
                            self.units.updateIndex()
                            self.importSites(
                                sites,
                                propsdlg.ui.updateCoords.isChecked(),
                                propsdlg.ui.updateUnits.isChecked(),
                            )
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "GeoJSON error",
                            "Features must be points",
                        )
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "GeoJSON error",
                        "There are no features in file",
                    )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "GeoJSON error",
                    "GeoJSON must contain FeatureCollection",
                )

    def importSites(self, data, update_coords, update_units):
        added = 0
        modified = 0
        if update_coords or update_units:
            for rec in data:
                id = self.db_getSiteID(rec[0])
                if id:
                    sindex = self.sites.index(self.sites.id2row[id], 0)
                    row = self.sites.getRow(sindex)
                    if update_coords:
                        row[sitecol["x"]] = rec[1]
                        row[sitecol["y"]] = rec[2]
                    if update_units:
                        row[sitecol["id_units"]] = rec[4]
                    self.db_updateSite(row)
                    self.sites.updateRow(sindex, row)
                    modified += 1
        else:
            for rec in data:
                id = self.db_addSite(rec)
                if id is not None:
                    self.sites.appendRow([id] + list(rec))
                    added += 1
        if added > 0:
            # self.dbcommit()
            self.changed = True
            # set focus on added item
            index = self.sortsites.mapFromSource(
                self.sites.createIndex(0, sitecol["name"])
            )
            self.siteSelection.setCurrentIndex(
                index,
                QtCore.QItemSelectionModel.ClearAndSelect
                | QtCore.QItemSelectionModel.Rows,
            )
            self.ui.sitesView.scrollTo(index, QtWidgets.QAbstractItemView.EnsureVisible)
            self.ui.sitesView.setFocus()
            self.statusBar().showMessage(f"{added} sites successfully imported.", 5000)
        elif modified > 0:
            # self.dbcommit()
            self.changed = True
            self.ui.sitesView.setFocus()
            self.statusBar().showMessage(
                f"{modified} sites successfully updated.", 5000
            )
        else:
            self.statusBar().showMessage("All sites already exists.", 5000)

    def compactDatabase(self):
        if self.changed:
            if (
                QtWidgets.QMessageBox.question(
                    self,
                    "Question",
                    "Do you want to save all changes before comapction?",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No,
                )
                == QtWidgets.QMessageBox.Yes
            ):
                self.dbcommit()
            else:
                self.conn.rollback()
        try:
            unused_units = 0
            for row in self.conn.execute(
                "SELECT units.id FROM units LEFT OUTER JOIN sites ON units.id=sites.id_units GROUP BY units.name HAVING count(sites.name)=0"
            ):
                self.conn.execute("DELETE FROM units WHERE id=?", row)
                unused_units += 1
            unused_structypes = 0
            for row in self.conn.execute(
                "SELECT structype.id FROM structype LEFT OUTER JOIN structdata ON structype.id=structdata.id_structype GROUP BY structype.structure HAVING count(structdata.id)=0"
            ):
                self.conn.execute("DELETE FROM structype WHERE id=?", row)
                unused_structypes += 1
        except Exception:
            QtWidgets.QMessageBox.critical(
                None,
                "Compacting database",
                "Error during compacting: {}".format(sys.exc_info()[1]),
                QtWidgets.QMessageBox.Ok,
            )
        else:
            if unused_units > 0 or unused_structypes > 0:
                if (
                    QtWidgets.QMessageBox.question(
                        self,
                        "Database compact",
                        "Do you want to delete {} unused units and {} unsused structure types?".format(
                            unused_units, unused_structypes
                        ),
                        QtWidgets.QMessageBox.Yes,
                        QtWidgets.QMessageBox.No,
                    )
                    == QtWidgets.QMessageBox.Yes
                ):
                    self.dbcommit()
                    self.conn.close()
                    self.connectDatabase(self.recent[0])
                else:
                    self.conn.rollback()

    def infoSDB(self):
        """Show database info and diagnostics"""
        bline = "-------------------------\n"
        info = "Database file: {}\n".format(self.recent[0])
        info += bline
        try:
            nsites = len(self.conn.execute("SELECT id FROM sites").fetchall())
        except Exception:
            info += "Error during SELECT id FROM sites: {}\n".format(sys.exc_info()[1])
        else:
            info += "Number of sites: {}\n".format(nsites)
        try:
            nunits = len(self.conn.execute("SELECT id FROM units").fetchall())
        except Exception:
            info += "Error during SELECT id FROM units: {}\n".format(sys.exc_info()[1])
        else:
            info += "Number of units: {}\n".format(nunits)
        try:
            ndata = len(self.conn.execute("SELECT id FROM structdata").fetchall())
        except Exception:
            info += "Error during SELECT id FROM structdata: {}\n".format(
                sys.exc_info()[1]
            )
        else:
            info += "Number of measurements: {}\n".format(ndata)
        info += bline
        try:
            ntype = []
            for row in self.conn.execute("SELECT id,name FROM units ORDER BY pos"):
                ntype.append(
                    (
                        row[1],
                        len(
                            self.conn.execute(
                                "SELECT id FROM sites WHERE id_units=?", (row[0],)
                            ).fetchall()
                        ),
                    )
                )
        except Exception:
            info += "Error during counting units: {}\n".format(sys.exc_info()[1])
        else:
            for row in ntype:
                info += "Unit {}: {} sites\n".format(*row)
        info += bline
        try:
            ntype = []
            for row in self.conn.execute(
                "SELECT id,structure FROM structype ORDER BY pos"
            ):
                ntype.append(
                    (
                        row[1],
                        len(
                            self.conn.execute(
                                "SELECT id FROM structdata WHERE id_structype=?",
                                (row[0],),
                            ).fetchall()
                        ),
                    )
                )
        except Exception:
            info += "Error during counting structdata: {}\n".format(sys.exc_info()[1])
        else:
            for row in ntype:
                info += "Structure type {}: {} measurements\n".format(*row)
        info += bline
        try:
            ntags = []
            for row in self.conn.execute("SELECT id,name FROM tags ORDER BY pos"):
                ntags.append(
                    (
                        row[1],
                        len(
                            self.conn.execute(
                                "SELECT id FROM tagged WHERE id_tags=?", (row[0],)
                            ).fetchall()
                        ),
                    )
                )
        except Exception:
            info += "Error during counting structdata: {}\n".format(sys.exc_info()[1])
        else:
            for row in ntags:
                info += "Tagged with {}: {} measurements\n".format(*row)
        info += bline
        try:
            res = self.conn.execute(
                "SELECT value FROM meta WHERE name='version'"
            ).fetchall()
        except Exception:
            info += (
                'Error during SELECT value FROM meta WHERE name="version": {}\n'.format(
                    sys.exc_info()[1]
                )
            )
        else:
            info += "Saved by version: {}\n".format(res[0][0])
            if len(res) > 1:
                info += "Error: More than one 'version' metavalues.\n"
        try:
            res = self.conn.execute(
                "SELECT value FROM meta WHERE name='created'"
            ).fetchall()
        except Exception:
            info += 'SELECT value FROM meta WHERE name="created": {}\n'.format(
                sys.exc_info()[1]
            )
        else:
            info += "Created: {}\n".format(res[0][0])
            if len(res) > 1:
                info += "Error: More than one 'created' metavalues.\n"
        try:
            res = self.conn.execute(
                "SELECT value FROM meta WHERE name='updated'"
            ).fetchall()
        except Exception:
            info += (
                'Error during SELECT value FROM meta WHERE name="updated": {}\n'.format(
                    sys.exc_info()[1]
                )
            )
        else:
            info += "Last updated: {}\n".format(res[0][0])
            if len(res) > 1:
                info += "Error: More than one 'updated' metavalues.\n"
        try:
            res = self.conn.execute(
                "SELECT value FROM meta WHERE name='accessed'"
            ).fetchall()
        except Exception:
            info += 'Error during SELECT value FROM meta WHERE name="accessed": {}\n'.format(
                sys.exc_info()[1]
            )
        else:
            info += "Last accessed: {}".format(res[0][0])
            if len(res) > 1:
                info += "Error: More than one 'accessed' metavalues."
        try:
            res = self.conn.execute(
                "SELECT value FROM meta WHERE name='crs'"
            ).fetchall()
        except Exception:
            crs = 'Error during SELECT value FROM meta WHERE name="crs": {}\n'.format(
                sys.exc_info()[1]
            )
        else:
            crs = res[0][0]
            if len(res) > 1:
                info += "Error: More than one 'crs' metavalues.\n"
        dlg = DialogSDBInfo(info, crs)
        if dlg.exec_():
            if crs != dlg.crs:
                self.conn.execute(
                    "UPDATE meta SET value=? WHERE name='crs'", (dlg.crs,)
                )
                self.changed = True

    def saveFileSDB(self):
        if self.changed:
            if (
                QtWidgets.QMessageBox.question(
                    self,
                    "Question",
                    "Do you want to save all current changes?",
                    QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No,
                )
                == QtWidgets.QMessageBox.Yes
            ):
                self.dbcommit()

    def saveAsSDB(self):
        self.saveFileSDB()
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "New database", ".", "SDB database (*.sdb)"
        )
        if fname:
            p = Path(fname)
            if not p.suffix:
                p = p.with_suffix(".sdb")
            nconn = sqlite3.connect(p)
            nconn.text_factory = str
            # Create schema of database
            for sql in SCHEMA.splitlines():
                nconn.execute(sql)
            # Insert metadata
            crs = self.conn.execute(
                "SELECT value FROM meta WHERE name='crs'"
            ).fetchall()[0][0]
            created = self.conn.execute(
                "SELECT value FROM meta WHERE name='created'"
            ).fetchall()[0][0]
            if not created:
                created = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            nconn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("version", __version__),
            )
            nconn.execute("INSERT INTO meta (name,value) VALUES (?,?)", ("crs", crs))
            nconn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("created", created),
            )
            nconn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("updated", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
            nconn.execute(
                "INSERT INTO meta (name,value) VALUES (?,?)",
                ("accessed", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
            )
            # read, check translate
            errors = []
            units = {}
            ins = """INSERT OR IGNORE INTO units ('pos','name','description') VALUES (?,?,?)"""
            for row in self.conn.execute("SELECT * FROM units").fetchall():
                res = nconn.execute(ins, (int(row[1]), row[2], row[3]))
                if res.rowcount > 0:
                    units[int(row[0])] = res.lastrowid
                else:
                    errors.append(f"Units record: {row}")

            tags = {}
            ins = """INSERT OR IGNORE INTO tags ('pos','name','description') VALUES (?,?,?)"""
            for row in self.conn.execute("SELECT * FROM tags").fetchall():
                res = nconn.execute(ins, (int(row[1]), row[2], row[3]))
                if res.rowcount > 0:
                    tags[int(row[0])] = res.lastrowid
                else:
                    errors.append(f"Tags record: {row}")

            structypes = {}
            ins = """INSERT OR IGNORE INTO structype ('pos','structure','description','structcode','groupcode','planar') VALUES (?,?,?,?,?,?)"""
            for row in self.conn.execute("SELECT * FROM structype").fetchall():
                res = nconn.execute(
                    ins,
                    (
                        int(row[1]),
                        row[2],
                        row[3],
                        int(row[4]),
                        int(row[5]),
                        int(row[6]),
                    ),
                )
                if res.rowcount > 0:
                    structypes[int(row[0])] = res.lastrowid
                else:
                    errors.append(f"Structype record: {row}")

            sites = {}
            ins = """INSERT OR IGNORE INTO sites ('id_units','name','x_coord','y_coord','description') VALUES (?,?,?,?,?)"""
            for row in self.conn.execute("SELECT * FROM sites").fetchall():
                if int(row[1]) in units:
                    id_unit = units[int(row[1])]
                    res = nconn.execute(
                        ins, (id_unit, row[2], float(row[3]), float(row[4]), row[5])
                    )
                    if res.rowcount > 0:
                        sites[int(row[0])] = res.lastrowid
                    else:
                        errors.append(f"Sites record: {row}")
                else:
                    errors.append(f"Sites(unit) record: {row}")

            structdata = {}
            ins = """INSERT OR IGNORE INTO structdata ('id_sites','id_structype','azimuth','inclination','description') VALUES (?,?,?,?,?)"""
            for row in self.conn.execute("SELECT * FROM structdata").fetchall():
                if int(row[1]) in sites:
                    id_site = sites[int(row[1])]
                    if int(row[2]) in structypes:
                        id_type = structypes[int(row[2])]
                        res = nconn.execute(
                            ins,
                            (id_site, id_type, float(row[3]), float(row[4]), row[5]),
                        )
                        if res.rowcount > 0:
                            structdata[int(row[0])] = res.lastrowid
                        else:
                            errors.append(f"Structdata record: {row}")
                    else:
                        errors.append(f"Structdata(structype) record: {row}")
                else:
                    errors.append(f"Structdata(site) record: {row}")

            ins = """INSERT OR IGNORE INTO tagged ('id_tags','id_structdata') VALUES (?,?)"""
            for row in self.conn.execute("SELECT * FROM tagged").fetchall():
                if int(row[1]) in tags:
                    id_tag = tags[int(row[1])]
                    if int(row[2]) in structdata:
                        id_data = structdata[int(row[2])]
                        nconn.execute(ins, (id_tag, id_data))
                    else:
                        errors.append(f"Tagged(tag) record: {row}")
                else:
                    errors.append(f"Tagged(strucdata) record: {row}")

            ins = """INSERT OR IGNORE INTO attach ('id_structdata_planar','id_structdata_linear') VALUES (?,?)"""
            for row in self.conn.execute("SELECT * FROM attach").fetchall():
                if int(row[1]) in structdata:
                    id_planar = structdata[int(row[1])]
                    if int(row[2]) in structdata:
                        id_linear = structdata[int(row[2])]
                        nconn.execute(ins, (id_planar, id_linear))
                    else:
                        errors.append(f"Attach(strucdata-planar) record: {row}")
                else:
                    errors.append(f"Attach(strucdata-linear) record: {row}")

            nconn.commit()
            nconn.close()
            self.openFileSDB(False, p)
            if errors:
                dlg = DialogSDBReport("\n".join(errors))
                dlg.exec_()

    def checkDatabase(self):
        """Check and possibly fix database"""
        ok = True
        # primary select
        sql = """SELECT
            sites.name as name,
            sites.x_coord as x,
            sites.y_coord as y,
            units.name as unit,
            structdata.azimuth as azimuth,
            structdata.inclination as inclination,
            structype.structure as structure,
            structype.planar as planar,
            structdata.description as description,
            GROUP_CONCAT(tags.name) AS tags
            FROM structdata
            INNER JOIN sites ON structdata.id_sites=sites.id
            INNER JOIN structype ON structype.id=structdata.id_structype
            INNER JOIN units ON units.id=sites.id_units
            LEFT OUTER JOIN tagged ON structdata.id=tagged.id_structdata
            LEFT OUTER JOIN tags ON tags.id=tagged.id_tags
            GROUP BY
            structdata.id
            LIMIT 1"""
        try:
            self.conn.execute(sql)
            self.conn.execute("SELECT * FROM attach LIMIT 1")
        except Exception:
            ok = False
        else:
            # Check for meta table
            mt = self.conn.execute(
                "SELECT name FROM sqlite_master WHERE name='meta'"
            ).fetchall()
            if not mt:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Database metadata table error",
                    "Metadata table does not exists !\nDefault one will be created.",
                )
                self.conn.execute(
                    "CREATE TABLE meta (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, name varchar(16) NOT NULL UNIQUE, value text)"
                )
                self.conn.execute(
                    "INSERT INTO meta (name,value) VALUES (?,?)",
                    ("version", __version__),
                )
                self.conn.execute(
                    "INSERT INTO meta (name,value) VALUES (?,?)", ("crs", "EPSG:4326")
                )
                self.conn.execute(
                    "INSERT INTO meta (name,value) VALUES (?,?)",
                    ("created", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
                )
                self.conn.execute(
                    "INSERT INTO meta (name,value) VALUES (?,?)",
                    ("updated", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
                )
                self.conn.execute(
                    "INSERT INTO meta (name,value) VALUES (?,?)",
                    ("accessed", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
                )
                self.conn.commit()
                self.changed = False
            else:
                val = self.conn.execute(
                    "SELECT value FROM meta WHERE name='version'"
                ).fetchall()
                if not val:
                    self.conn.execute(
                        "INSERT INTO meta (name,value) VALUES (?,?)",
                        ("version", __version__),
                    )
                val = self.conn.execute(
                    "SELECT value FROM meta WHERE name='crs'"
                ).fetchall()
                if not val:
                    val2 = self.conn.execute(
                        "SELECT value FROM meta WHERE name='proj4'"
                    ).fetchall()
                    if not val2:
                        self.conn.execute(
                            "INSERT INTO meta (name,value) VALUES (?,?)",
                            ("crs", "EPSG:4326"),
                        )
                    else:
                        self.conn.execute(
                            "INSERT INTO meta (name,value) VALUES (?,?)",
                            ("crs", val2[0][0]),
                        )
                val = self.conn.execute(
                    "SELECT value FROM meta WHERE name='created'"
                ).fetchall()
                if not val:
                    self.conn.execute(
                        "INSERT INTO meta (name,value) VALUES (?,?)",
                        ("created", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
                    )
                val = self.conn.execute(
                    "SELECT value FROM meta WHERE name='updated'"
                ).fetchall()
                if not val:
                    self.conn.execute(
                        "INSERT INTO meta (name,value) VALUES (?,?)",
                        ("updated", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")),
                    )
                val = self.conn.execute(
                    "SELECT value FROM meta WHERE name='accessed'"
                ).fetchall()
                if not val:
                    self.conn.execute(
                        "INSERT INTO meta (name,value) VALUES (?,?)",
                        (
                            "accessed",
                            datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                        ),
                    )
                else:
                    self.conn.execute(
                        "UPDATE meta SET value = ? WHERE name = ?",
                        (
                            datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                            "accessed",
                        ),
                    )
                self.conn.commit()
        return ok

    def connectDatabase(self, dbname):
        """Just create connection to SQLite database."""
        # connect to database
        self.conn = sqlite3.connect(str(dbname))
        self.conn.text_factory = str
        self.conn.execute("pragma encoding='UTF-8'")
        # self.conn.execute("BEGIN TRANSACTION")
        if self.checkDatabase():
            # Populate models and views from database.
            # -----------------------------------
            # read structures table
            # -----------------------------------
            tlist = []
            for row in self.conn.execute(
                "SELECT id,structure,planar,description,structcode,groupcode FROM structype ORDER BY pos"
            ):
                tlist.append(list(row))

            self.structures = StructureModel(tlist)

            # let's add view of the data source we just created:
            self.ui.structuresView.setModel(self.structures)
            self.ui.structuresView.setColumnHidden(structurecol["id"], True)
            self.ui.structuresView.setColumnHidden(structurecol["scode"], True)
            self.ui.structuresView.setColumnHidden(structurecol["gcode"], True)
            self.ui.structuresView.resizeColumnToContents(structurecol["structure"])
            self.ui.structuresView.resizeColumnToContents(structurecol["planar"])
            self.structureSelection = self.ui.structuresView.selectionModel()

            # -----------------------------------
            # read units table
            # -----------------------------------
            tlist = []
            for row in self.conn.execute(
                "SELECT id,name,description FROM units ORDER BY pos"
            ):
                tlist.append(list(row))

            self.units = UnitModel(tlist)

            # let's add view of the data source we just created:
            self.ui.unitsView.setModel(self.units)
            self.ui.unitsView.setColumnHidden(unitcol["id"], True)
            self.ui.unitsView.resizeColumnToContents(unitcol["name"])
            self.unitSelection = self.ui.unitsView.selectionModel()

            # -----------------------------------
            # read tags table
            # -----------------------------------
            tlist = []
            for row in self.conn.execute(
                "SELECT id,name,description FROM tags ORDER BY pos"
            ):
                tlist.append(
                    list(row)
                    + [
                        QtCore.Qt.Unchecked,
                    ]
                )

            self.tags = TagModel(tlist)

            # let's add view of the data source we just created:
            self.ui.tagsView.setModel(self.tags)
            self.ui.tagsView.setColumnHidden(tagcol["id"], True)
            self.ui.tagsView.setColumnHidden(tagcol["check"], True)
            self.ui.tagsView.resizeColumnToContents(tagcol["name"])
            self.tagSelection = self.ui.tagsView.selectionModel()

            # -----------------------------------
            # read sites table
            # -----------------------------------
            tlist = []
            for row in self.conn.execute(
                "SELECT id,name,x_coord,y_coord,description,id_units FROM sites ORDER BY id"
            ):
                tlist.append(list(row))

            self.sites = SiteModel(tlist)

            self.sortsites = QtCore.QSortFilterProxyModel(self)
            self.sortsites.setSourceModel(self.sites)
            self.sortsites.setDynamicSortFilter(True)

            # let's add view of the data source we just created:
            self.ui.sitesView.setModel(self.sortsites)
            self.ui.sitesView.setSelectionBehavior(
                QtWidgets.QAbstractItemView.SelectRows
            )
            # self.ui.sitesView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            # self.ui.sitesView.horizontalHeader().setStretchLastSection(True)
            # self.ui.sitesView.verticalHeader().hide()
            self.ui.sitesView.setColumnHidden(sitecol["id"], True)
            self.ui.sitesView.setColumnHidden(sitecol["x"], True)
            self.ui.sitesView.setColumnHidden(sitecol["y"], True)
            self.ui.sitesView.setColumnHidden(sitecol["desc"], True)
            self.ui.sitesView.setColumnHidden(sitecol["id_units"], True)
            # self.ui.sitesView.verticalHeader().setDefaultSectionSize(22)
            self.ui.sitesView.setSortingEnabled(True)
            self.ui.sitesView.sortByColumn(sitecol["name"], QtCore.Qt.AscendingOrder)

            # Connect siteSelection changed signal
            self.siteSelection = self.ui.sitesView.selectionModel()
            self.siteSelection.selectionChanged.connect(self.siteselChanged)
            # connect sort signal
            self.ui.sitesView.horizontalHeader().sectionClicked.connect(
                self.siteSorting
            )

            # preload dialog
            self.sitefilterdlg = DialogSiteFilter(self.units)
            self.datafilterdlg = DialogDataFilter(self.structures)
            self.selectunitdlg = DialogSelectUnit(self.units)

            # -----------------------------------
            # All done, set focus ang go...
            # -----------------------------------
            self.siteSelection.setCurrentIndex(
                self.sites.index(0, sitecol["name"]),
                QtCore.QItemSelectionModel.ClearAndSelect
                | QtCore.QItemSelectionModel.Rows,
            )
            self.siteselChanged()
            self.ui.sitesView.setFocus()

            self.connected = True
            self.changed = False
            dbversion = self.conn.execute(
                "SELECT value FROM meta WHERE name='version'"
            ).fetchall()[0][0]
            if dbversion.split(".")[0] < "3":
                QtWidgets.QMessageBox.warning(
                    self,
                    "Version check",
                    "Your database is created in older version of PySDB.\nConsider database format update.",
                )
        else:
            QtWidgets.QMessageBox.critical(
                None,
                "PySDB database",
                "File {} is not valid PySDB database.".format(dbname),
                QtWidgets.QMessageBox.Ok,
            )
            self.conn.close()

    def dbcommit(self):
        # self.conn.execute("REPLACE INTO meta (name,value) VALUES (?,?)", ("updated", datetime.datetime.now().strftime("%d.%m.%Y %H:%M")))
        self.conn.execute(
            "UPDATE meta SET value=? WHERE name=?",
            (datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), "updated"),
        )
        self.conn.commit()
        self.changed = False

    # ----------------------------------------------------------------------
    # SITE VIEW
    # ----------------------------------------------------------------------
    def addSiteDlg(self):
        """Open site dialog and retrieve data."""
        dlg = DialogAddEditSite(self.units, "Add")
        if dlg.exec_():
            id = self.db_addSite(dlg.data[1:])
            if id is not None:
                self.sites.appendRow([id] + dlg.data[1:])
                # set focus on added item
                index = self.sortsites.mapFromSource(
                    self.sites.createIndex(self.sites.rowCount() - 1, sitecol["name"])
                )
                self.siteSelection.setCurrentIndex(
                    index,
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.ui.sitesView.scrollTo(
                    index, QtWidgets.QAbstractItemView.EnsureVisible
                )
                # self.ui.sitesView.scrollToBottom()
                self.ui.sitesView.setFocus()
            else:
                self.statusBar().showMessage(
                    f"Site {dlg.data[1]} already exists.", 5000
                )

    def editSiteDlg(self, index=None):
        """Open site dialog to edit data."""
        # method is invoked by double-click (index passed) or by button action (no index passed)
        if not index:
            indexlist = self.siteSelection.selectedRows()
        else:
            indexlist = [index]
        # multiple sites selected?
        if len(indexlist) == 1:
            sindex = self.sortsites.mapToSource(indexlist[0])
            data = self.sites.getRow(sindex).copy()
            dlg = DialogAddEditSite(self.units, "Edit", data)
            if dlg.exec_():
                cur = self.db_updateSite(dlg.data)
                if cur.rowcount > 0:
                    self.sites.updateRow(sindex, dlg.data)
                    self.changed = True
                    self.statusBar().showMessage(
                        f"Site {dlg.data[sitecol['name']]} updated.", 5000
                    )
                else:
                    self.statusBar().showMessage(
                        f"Site {dlg.data[sitecol['name']]} already exists.",
                        5000,
                    )
        else:
            if self.selectunitdlg.exec_():
                newunit_id = self.units.row2id[
                    self.selectunitdlg.ui.unitCombo.currentIndex()
                ]
                for index in indexlist:
                    sindex = self.sortsites.mapToSource(index)
                    data = self.sites.getRow(sindex).copy()
                    data[sitecol["id_units"]] = newunit_id
                    if self.db_updateSite(data):
                        self.sites.updateRow(sindex, data)

    def removeSiteDlg(self):
        """Remove selected data from sites."""
        indexlist = self.siteSelection.selectedRows()
        if indexlist:
            warn_msg = "Are you sure you want to delete selected sites and all related data?\nUse Save to move data to another site."
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                warn_msg,
                QtWidgets.QMessageBox.Yes
                | QtWidgets.QMessageBox.Save
                | QtWidgets.QMessageBox.Cancel,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                # remember postion of cursor
                row = indexlist[0].row()
                # sites must be deleted from last to first in sitemodel
                sindex = [self.sortsites.mapToSource(index) for index in indexlist]
                rows = [index.row() for index in sindex]
                count = 0
                for dummy, index in sorted(zip(rows, sindex), reverse=True):
                    count += self.db_removeSite(self.sites.row2id[index.row()])
                    self.sites.removeRow(index)
                # set focus on remembered position
                if row >= self.sites.rowCount():
                    row = self.sites.rowCount() - 1
                self.siteSelection.setCurrentIndex(
                    self.sites.index(row, sitecol["name"]),
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.ui.sitesView.setFocus()
                self.statusBar().showMessage(
                    f"{len(rows)} sites and {count} data have been deleted.", 5000
                )
            if reply == QtWidgets.QMessageBox.Save:
                allsites = [item[:2] for item in self.sites._items]
                selsites = [
                    self.sites.getRow(self.sortsites.mapToSource(index))[:2]
                    for index in indexlist
                ]
                dessites = [rec for rec in allsites if rec not in selsites]
                ids, sites = zip(*dessites)
                # sort it
                sites, ids = (list(t) for t in zip(*sorted(zip(sites, ids))))
                dessite, okPressed = QtWidgets.QInputDialog.getItem(
                    self, "Select site", "Sitename:", sites, 0, False
                )
                if okPressed and dessite:
                    desid = ids[sites.index(dessite)]
                    # move data
                    for id, site in selsites:
                        for dat in self.conn.execute(
                            "SELECT id FROM structdata WHERE id_sites=?", (id,)
                        ):
                            self.conn.execute(
                                "UPDATE structdata SET id_sites=? WHERE id=?",
                                (desid, dat[0]),
                            )
                    # sites must be deleted from last to first in sitemodel
                    sindex = [self.sortsites.mapToSource(index) for index in indexlist]
                    rows = [index.row() for index in sindex]
                    count = 0
                    for dummy, index in sorted(zip(rows, sindex), reverse=True):
                        count += self.db_removeSite(self.sites.row2id[index.row()])
                        self.sites.removeRow(index)
                    # set focus on destination site
                    index = self.sortsites.mapFromSource(
                        self.sites.createIndex(
                            self.sites.id2row[desid], sitecol["name"]
                        )
                    )
                    self.siteSelection.setCurrentIndex(
                        index,
                        QtCore.QItemSelectionModel.ClearAndSelect
                        | QtCore.QItemSelectionModel.Rows,
                    )
                    self.ui.sitesView.scrollTo(
                        index, QtWidgets.QAbstractItemView.EnsureVisible
                    )
                    self.ui.sitesView.setFocus()

                    # self.siteSelection.setCurrentIndex(self.sites.index(self.sites.id2row[desid],sitecol['name']), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
                    # self.ui.sitesView.setFocus()
                    self.statusBar().showMessage(
                        f"{len(rows)} sites and {count} data have been deleted.", 5000
                    )

    def filterSiteDlg(self):
        """Filter sites"""
        self.ui.pushSiteFilter.setChecked(not self.ui.pushSiteFilter.isChecked())
        if self.sitefilterdlg.exec_():
            if self.sitefilterdlg.ui.radioUnit.isChecked():
                self.sortsites.setFilterRegExp(
                    QtCore.QRegExp(
                        "^"
                        + str(
                            self.units.row2id[
                                self.sitefilterdlg.ui.unitCombo.currentIndex()
                            ]
                        )
                        + "$"
                    )
                )
                self.sortsites.setFilterKeyColumn(sitecol["id_units"])
                self.ui.pushSiteFilter.setChecked(True)
                funame = self.sitefilterdlg.ui.unitCombo.currentText()
                self.statusBar().showMessage(f"Sites filtered to unit {funame}", 5000)
            elif self.sitefilterdlg.ui.radioName.isChecked():
                self.sortsites.setFilterWildcard(
                    "*" + self.sitefilterdlg.ui.nameEdit.text() + "*"
                )
                self.sortsites.setFilterKeyColumn(sitecol["name"])
                self.ui.pushSiteFilter.setChecked(True)
                fsname = self.sitefilterdlg.ui.nameEdit.text()
                self.statusBar().showMessage(
                    f"Sites filtered to name contains {fsname}", 5000
                )
            else:
                self.sortsites.setFilterRegExp("")
                self.ui.pushSiteFilter.setChecked(False)
                self.statusBar().showMessage("All sites shown", 5000)

    def db_getSiteID(self, name):
        """Get site id from database."""
        res = self.conn.execute("SELECT id FROM sites WHERE name=?", (name,)).fetchall()
        if res:
            return res[0][0]

    def db_addSite(self, data):
        """Add site data database."""
        res = self.conn.execute(
            "INSERT OR IGNORE INTO sites (name,x_coord,y_coord,description,id_units) VALUES (?,?,?,?,?)",
            data,
        )
        if res.rowcount > 0:
            self.changed = True
            return res.lastrowid

    def db_updateSite(self, data):
        """Update site data in database."""
        return self.conn.execute(
            "UPDATE OR IGNORE sites SET name=?, x_coord=?, y_coord=?, description=?, id_units=? WHERE id=?",
            data[1:] + data[:1],
        )

    def db_removeSite(self, id):
        """Remove site data in database."""
        count = 0
        # delete related attachments and tagged records
        for dat in self.conn.execute(
            "SELECT id FROM structdata WHERE id_sites=?", (id,)
        ):
            count += 1
            self.db_removeData(dat[0])
        # delete from site table
        self.conn.execute("DELETE FROM sites WHERE id=?", (id,))
        self.changed = True
        return count

    def siteselChanged(self, selected=None, deselected=None):
        # read selected data from structdata table
        tlist = []
        for site in self.siteSelection.selectedRows():
            for row in self.conn.execute(
                "SELECT structdata.id,structdata.id_sites,structdata.id_structype,azimuth,inclination,structype.structure,structdata.description FROM structdata Inner Join structype ON structype.id = structdata.id_structype WHERE structdata.id_sites=? ORDER BY structdata.id",
                (site.data(),),
            ):
                tags = []
                for tag in self.conn.execute(
                    "SELECT tags.name FROM tagged INNER JOIN tags ON tags.id = tagged.id_tags WHERE tagged.id_structdata = ?",
                    (row[0],),
                ):
                    tags.append(tag[0])
                nrow = list(row)
                nrow.append(",".join(tags))
                tlist.append(nrow)
        # read data
        self.data = DataModel(tlist)
        self.filterdata = QtCore.QSortFilterProxyModel(self)
        self.filterdata.setSourceModel(self.data)

        # let's add view of the data source we just created:
        self.ui.dataView.clearSpans()
        self.ui.dataView.setModel(self.filterdata)
        self.ui.dataView.setColumnHidden(datacol["id"], True)
        self.ui.dataView.setColumnHidden(datacol["id_sites"], True)
        self.ui.dataView.setColumnHidden(datacol["id_struct"], True)
        self.ui.dataView.setColumnHidden(datacol["desc"], True)
        self.ui.dataView.resizeColumnToContents(datacol["azi"])
        self.ui.dataView.resizeColumnToContents(datacol["inc"])
        self.ui.dataView.resizeColumnToContents(datacol["struct"])

        self.dataSelection = self.ui.dataView.selectionModel()
        self.dataSelection.selectionChanged.connect(self.dataselChanged)

        self.do_filterdata()
        self.show()

    def siteSorting(self, logindex):
        # cycle 4 sort types
        self.sortorder = (self.sortorder + 1) % 4
        if self.sortorder == 2:
            self.ui.sitesView.sortByColumn(sitecol["id"], QtCore.Qt.AscendingOrder)
        if self.sortorder == 3:
            self.ui.sitesView.sortByColumn(sitecol["id"], QtCore.Qt.DescendingOrder)

    # ----------------------------------------------------------------------
    # DATA VIEW
    # ----------------------------------------------------------------------

    def addDataDlg(self):
        """Open data dialog and retrieve data."""
        indexlist = self.siteSelection.selectedRows()
        if len(indexlist) != 1:
            QtWidgets.QMessageBox.warning(
                self,
                "Add data error",
                "You have no or more than one site selected !\nFor adding data select only one site.",
            )
        else:
            # prepare attach list
            attachlist = [
                [row[0], f"{row[1]}/{row[2]} - {row[3]}"]
                for row in self.conn.execute(
                    "SELECT structdata.id,azimuth, inclination, structype.structure FROM structdata INNER JOIN structype ON structype.id = structdata.id_structype WHERE structype.planar=1 AND structdata.id_sites=? ORDER BY structdata.id",
                    (indexlist[0].data(),),
                )
            ]
            self.tags.cleanState()
            dlg = DialogAddEditData(self.structures, self.tags, attachlist, "Add")
            # set dlg data
            dlg.data[datacol["id_sites"]] = indexlist[0].data()
            # set attach combo
            dlg.ui.attachCombo.setCurrentIndex(-1)
            if dlg.exec_():
                # test attachment
                if (
                    not self.structures.isplanar(dlg.ui.structureCombo.currentIndex())
                    and dlg.ui.attachCombo.currentIndex() != -1
                ):
                    attached = attachlist[dlg.ui.attachCombo.currentIndex()][0]
                else:
                    attached = None
                self.db_addData(dlg.data, attached, self.tags.getChecked())
                self.siteselChanged()
                # set focus
                self.dataSelection.setCurrentIndex(
                    self.data.index(self.data.rowCount() - 1, datacol["azi"]),
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.ui.dataView.scrollToBottom()
                self.ui.dataView.setFocus()

    def editDataDlg(self, index=None):
        """Open data dialog to edit data."""
        # method is invoked by double-click (index passed) or by button action (no index passed)
        if not index:
            indexlist = self.dataSelection.selectedRows()
        else:
            indexlist = [index]
        # multiple sites selected?
        if len(indexlist) == 1:
            data = self.data.getRow(self.filterdata.mapToSource(indexlist[0]))
            id = data[datacol["id"]]
            siteid = data[datacol["id_sites"]]
            # prepare attach list
            attachlist = [
                [row[0], f"{row[1]}/{row[2]} - {row[3]}"]
                for row in self.conn.execute(
                    "SELECT structdata.id,azimuth, inclination, structype.structure FROM structdata INNER JOIN structype ON structype.id = structdata.id_structype WHERE structype.planar=1 AND structdata.id_sites=? AND structdata.id <> ? ORDER BY structdata.id",
                    (siteid, id),
                )
            ]
            # prepare tagged
            self.tags.setState(
                [
                    row[0]
                    for row in self.conn.execute(
                        "SELECT id_tags FROM tagged WHERE id_structdata=?", (id,)
                    )
                ]
            )
            dlg = DialogAddEditData(
                self.structures, self.tags, attachlist, "Edit", data
            )
            # set attach combo
            row = self.conn.execute(
                "SELECT id_structdata_planar FROM attach WHERE id_structdata_linear = ?",
                (id,),
            ).fetchall()
            if row == []:
                dlg.ui.attachCombo.setCurrentIndex(-1)
            else:
                dlg.ui.attachCombo.setCurrentIndex(
                    [a[0] for a in attachlist].index(row[0][0])
                )
            if dlg.exec_():
                # test attachment
                if (
                    not self.structures.isplanar(dlg.ui.structureCombo.currentIndex())
                    and dlg.ui.attachCombo.currentIndex() != -1
                ):
                    attached = attachlist[dlg.ui.attachCombo.currentIndex()][0]
                else:
                    attached = None
                self.db_updateData(
                    dlg.data, attached=attached, tagged=self.tags.getChecked()
                )
                self.siteselChanged()
        else:
            # types = []
            # for index in indexlist:
            #    data = self.data.getRow(self.filterdata.mapToSource(index))
            #    types.append(self.structures.isplanar(self.structures.id2row[data[datacol['id_struct']]]))
            # if all(types) or not any(types):
            self.tags.cleanState()
            dlg = DialogMultiEditData(self.structures, self.tags)
            if dlg.exec_():
                newstruct_id = self.structures.row2id[
                    dlg.ui.structureCombo.currentIndex()
                ]
                for index in indexlist:
                    data = self.data.getRow(self.filterdata.mapToSource(index))
                    tagged = None
                    if (
                        dlg.ui.radioBoth.isChecked()
                        or dlg.ui.radioStructure.isChecked()
                    ):
                        data[datacol["id_struct"]] = newstruct_id
                    if dlg.ui.radioBoth.isChecked() or dlg.ui.radioTags.isChecked():
                        tagged = self.tags.getChecked()
                    self.db_updateData(data, tagged=tagged)
                self.siteselChanged()
            # else:
            #    QtWidgets.QMessageBox.warning(self, 'Multiedit', 'You have to select only planar or only linear structures.')

    def removeDataDlg(self):
        """Remove selected data from data."""
        indexlist = self.dataSelection.selectedRows()
        if indexlist:
            warn_msg = "Are you sure you want to delete all selected data?"
            reply = QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                warn_msg,
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                # remember postion of cursor
                row = indexlist[0].row()
                # sites must be deleted from last to first in sitemodel
                sindex = [self.filterdata.mapToSource(index) for index in indexlist]
                rows = [index.row() for index in sindex]
                for dummy, index in sorted(zip(rows, sindex), reverse=True):
                    self.db_removeData(self.data.row2id[index.row()])
                self.siteselChanged()
                # set focus on remembered position
                if row >= self.data.rowCount():
                    row = self.data.rowCount() - 1
                self.dataSelection.setCurrentIndex(
                    self.data.index(row, datacol["azi"]),
                    QtCore.QItemSelectionModel.ClearAndSelect
                    | QtCore.QItemSelectionModel.Rows,
                )
                self.ui.dataView.setFocus()

    def filterDataDlg(self):
        """Filter data"""
        self.ui.pushDataFilter.setChecked(not self.ui.pushDataFilter.isChecked())
        if self.datafilterdlg.exec_():
            self.do_filterdata()
            if self.datafilterdlg.ui.radioStructure.isChecked():
                stname = self.datafilterdlg.ui.structureCombo.currentText()
                self.statusBar().showMessage(
                    f"Data filtered to structure {stname}", 5000
                )
            elif self.datafilterdlg.ui.radioTag.isChecked():
                tgname = self.datafilterdlg.ui.nameTag.text()
                self.statusBar().showMessage(
                    f"Data filtered to tags contains {tgname}", 5000
                )
            else:
                self.statusBar().showMessage("All data shown", 5000)

    def do_filterdata(self):
        if self.datafilterdlg.ui.radioStructure.isChecked():
            self.filterdata.setFilterRegExp(
                QtCore.QRegExp(
                    "^"
                    + str(
                        self.structures.row2id[
                            self.datafilterdlg.ui.structureCombo.currentIndex()
                        ]
                    )
                    + "$"
                )
            )
            self.filterdata.setFilterKeyColumn(datacol["id_struct"])
        elif self.datafilterdlg.ui.radioTag.isChecked():
            self.filterdata.setFilterWildcard(
                "*" + self.datafilterdlg.ui.nameTag.text() + "*"
            )
            self.filterdata.setFilterKeyColumn(datacol["tags"])
        else:
            self.filterdata.setFilterRegExp("")
        if self.datafilterdlg.ui.radioNone.isChecked():
            self.ui.pushDataFilter.setChecked(False)
        else:
            self.ui.pushDataFilter.setChecked(True)

    def db_addData(self, data, attached=None, tagged=[]):
        """Add new record to database. attached is id of structure and tagged is list of tag ids."""
        id = self.conn.execute(
            "INSERT INTO structdata (id_sites, id_structype, azimuth, inclination,description) VALUES (?,?,?,?,?)",
            data[1:5] + data[6:7],
        ).lastrowid
        if attached:
            self.conn.execute(
                "INSERT INTO attach (id_structdata_planar, id_structdata_linear) VALUES (?,?)",
                (attached, id),
            )
        for idtag in tagged:
            self.conn.execute(
                "INSERT INTO tagged (id_structdata, id_tags) VALUES (?,?)", (id, idtag)
            )
        self.changed = True

    def db_updateData(self, data, attached=None, tagged=None):
        """Update data in database. attached is id of structure and tagged is list of tag ids."""
        self.conn.execute(
            "UPDATE structdata SET id_structype=?, azimuth=?, inclination=?, description=? WHERE id=?",
            data[2:5] + data[6:7] + data[0:1],
        )
        # remove existing attachments
        self.conn.execute("DELETE FROM attach WHERE id_structdata_linear=?", (data[0],))
        if attached:
            self.conn.execute(
                "INSERT INTO attach (id_structdata_planar, id_structdata_linear) VALUES (?,?)",
                (attached, data[0]),
            )
        if tagged is not None:
            # remove existing tags
            self.conn.execute("DELETE FROM tagged WHERE id_structdata=?", (data[0],))
            for idtag in tagged:
                self.conn.execute(
                    "INSERT INTO tagged (id_structdata, id_tags) VALUES (?,?)",
                    (data[0], idtag),
                )
        self.changed = True

    def db_removeData(self, id):
        """Remove data in database."""
        # delete datarecord and related attachments and tagged records
        self.conn.execute("DELETE FROM attach WHERE id_structdata_planar=?", (id,))
        self.conn.execute("DELETE FROM attach WHERE id_structdata_linear=?", (id,))
        self.conn.execute("DELETE FROM tagged WHERE id_structdata=?", (id,))
        self.conn.execute("DELETE FROM structdata WHERE id=?", (id,))
        self.changed = True

    def dataselChanged(self, selected, deselected):
        pass

    # ----------------------------------------------------------------------
    # STRUCTURE VIEW
    # ----------------------------------------------------------------------
    def addStructureDlg(self):
        """Open add structure dialog."""
        dlg = DialogAddEditStructure("Add")
        if dlg.exec_():
            cur = self.db_addStructure(dlg.data)
            if cur.rowcount > 0:
                dlg.data[structurecol["id"]] = cur.lastrowid
                self.structures.appendRow(dlg.data)
                self.statusBar().showMessage(
                    f"Structure {dlg.data[structurecol['structure']]} added.", 5000
                )
                self.ui.structuresView.scrollToBottom()
            else:
                self.statusBar().showMessage(
                    f"Structure {dlg.data[structurecol['structure']]} already exists.",
                    5000,
                )
            # self.siteSelection.setCurrentIndex(self.sites.index(self.sites.rowCount()-1,sitecol['name']), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.ui.structuresView.setFocus()

    def editStructureDlg(self, index):
        """Open edit structure dialog."""
        dlg = DialogAddEditStructure("Edit", self.structures.getRow(index).copy())
        if dlg.exec_():
            cur = self.db_updateStructure(dlg.data)
            if cur.rowcount > 0:
                self.structures.updateRow(index, dlg.data)
                self.changed = True
                self.statusBar().showMessage(
                    f"Structure {dlg.data[structurecol['structure']]} updated.", 5000
                )
            else:
                self.statusBar().showMessage(
                    f"Structure {dlg.data[structurecol['structure']]} already exists.",
                    5000,
                )

    def removeStructureDlg(self):
        """Remove selected structure from database."""
        indexlist = self.structureSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            todel = self.structures.getRow(index)
            others = [
                [row[structurecol["id"]], row[structurecol["structure"]]]
                for row in self.structures._items
                if row[structurecol["planar"]] == todel[structurecol["planar"]]
                and row[structurecol["id"]] != todel[structurecol["id"]]
            ]
            if len(others) > 0:
                dlg = DialogSaveDiscard(
                    [r[1] for r in others],
                    f"Do you want to delete structure {todel[structurecol['structure']]} and all related data?",
                    "Assign another structure to data:",
                )
                if dlg.exec_():
                    if dlg.checked():
                        # assign other structure to data
                        self.conn.execute(
                            "UPDATE structdata SET id_structype=? WHERE id_structype=?",
                            (
                                others[dlg.selected()][structurecol["id"]],
                                todel[structurecol["id"]],
                            ),
                        )
                    # delete structure and related data
                    count = self.db_removeStructure(self.structures.row2id[index.row()])
                    self.structures.removeRow(index)
                    self.siteselChanged()
                    self.statusBar().showMessage(
                        f"Structure {todel[structurecol['structure']]} and {count} data have been deleted.",
                        5000,
                    )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Delete structure",
                    "There must be at least one planar and one linear structure defined in database!",
                )

    def moveStructureUp(self):
        """Move selected structure up."""
        indexlist = self.structureSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() > 0:
                self.db_swapposStructure(
                    self.structures._items[index.row()][structurecol["id"]],
                    self.structures._items[index.row() - 1][structurecol["id"]],
                )
                cache = self.structures.getRow(index)
                self.structures.removeRow(index)
                self.structures.appendRow(cache, index, -1)
                self.ui.structuresView.selectRow(index.row() - 1)
                self.ui.structuresView.setFocus()

    def moveStructureDown(self):
        """Move selected structure up."""
        indexlist = self.structureSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() + 1 < self.structures.rowCount():
                self.db_swapposStructure(
                    self.structures._items[index.row()][structurecol["id"]],
                    self.structures._items[index.row() + 1][structurecol["id"]],
                )
                cache = self.structures.getRow(index)
                self.structures.removeRow(index)
                self.structures.appendRow(cache, index, 1)
                self.ui.structuresView.selectRow(index.row() + 1)
                self.ui.structuresView.setFocus()

    def db_addStructure(self, data):
        """Add structure to database."""
        pos = self.conn.execute("SELECT MAX(pos)+1 FROM structype").fetchall()[0][0]
        if not pos:
            pos = 1
        self.changed = True
        return self.conn.execute(
            "INSERT OR IGNORE INTO structype (pos, structure, planar, description, structcode, groupcode) VALUES (?,?,?,?,?,?)",
            (
                pos,
                data[structurecol["structure"]],
                data[structurecol["planar"]],
                data[structurecol["desc"]],
                data[structurecol["scode"]],
                data[structurecol["gcode"]],
            ),
        )

    def db_updateStructure(self, data):
        """Update structure in database."""
        return self.conn.execute(
            "UPDATE OR IGNORE structype SET structure=?, planar=?, description=?, structcode=?, groupcode=? WHERE id=?",
            (
                data[structurecol["structure"]],
                data[structurecol["planar"]],
                data[structurecol["desc"]],
                data[structurecol["scode"]],
                data[structurecol["gcode"]],
                data[structurecol["id"]],
            ),
        )

    def db_removeStructure(self, id):
        """Remove structure in database."""
        # delete related data, attachments and tagged records
        count = 0
        for dat in self.conn.execute(
            "SELECT id FROM structdata WHERE id_structype=?", (id,)
        ):
            count += 1
            self.db_removeData(dat[0])
        self.conn.execute("DELETE FROM structype WHERE id=?", (id,))
        self.changed = True
        return count

    def db_swapposStructure(self, aid, bid):
        apos = self.conn.execute(
            "SELECT pos FROM structype WHERE id=?", (aid,)
        ).fetchall()[0][0]
        bpos = self.conn.execute(
            "SELECT pos FROM structype WHERE id=?", (bid,)
        ).fetchall()[0][0]
        self.conn.execute("UPDATE structype SET pos=? WHERE id=?", (bpos, aid))
        self.conn.execute("UPDATE structype SET pos=? WHERE id=?", (apos, bid))
        self.changed = True

    # ----------------------------------------------------------------------
    # UNIT VIEW
    # ----------------------------------------------------------------------
    def addUnitDlg(self):
        """Open add unit dialog."""
        dlg = DialogAddEditUnit("Add")
        if dlg.exec_():
            cur = self.db_addUnit(dlg.data)
            if cur.rowcount > 0:
                dlg.data[unitcol["id"]] = cur.lastrowid
                self.units.appendRow(dlg.data)
                self.statusBar().showMessage(
                    "Unit %s added." % dlg.data[unitcol["name"]], 5000
                )
                self.ui.unitsView.scrollToBottom()
            else:
                self.statusBar().showMessage(
                    f"Unit {dlg.data[unitcol['name']]} already exists.", 5000
                )
            # self.siteSelection.setCurrentIndex(self.sites.index(self.sites.rowCount()-1,sitecol['name']), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.ui.unitsView.setFocus()

    def editUnitDlg(self, index):
        """Open edit unit dialog."""
        dlg = DialogAddEditUnit("Edit", self.units.getRow(index).copy())
        if dlg.exec_():
            cur = self.db_updateUnit(dlg.data)
            if cur.rowcount > 0:
                self.units.updateRow(index, dlg.data)
                self.changed = True
                self.statusBar().showMessage(
                    f"Unit {dlg.data[unitcol['name']]} updated.", 5000
                )
            else:
                self.statusBar().showMessage(
                    f"Unit {dlg.data[unitcol['name']]} already exists.", 5000
                )

    def removeUnitDlg(self):
        """Remove selected unit from database."""
        indexlist = self.unitSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            todel = self.units.getRow(index)
            others = [
                [row[unitcol["id"]], row[unitcol["name"]]]
                for row in self.units._items
                if row[unitcol["id"]] != todel[unitcol["id"]]
            ]
            if len(others) > 0:
                dlg = DialogSaveDiscard(
                    [r[1] for r in others],
                    f"Do you want to delete unit {todel[unitcol['name']]} and all related sites and data?",
                    "Assign another unit to sites:",
                )
                if dlg.exec_():
                    if dlg.checked():
                        # assign other unit to sites
                        self.conn.execute(
                            "UPDATE sites SET id_units=? WHERE id_units=?",
                            (
                                others[dlg.selected()][unitcol["id"]],
                                todel[unitcol["id"]],
                            ),
                        )
                        # change site model
                        for r in range(self.sites.rowCount()):
                            idx = self.sites.index(r, sitecol["id_units"])
                            row = self.sites.getRow(idx)
                            if row[sitecol["id_units"]] == todel[unitcol["id"]]:
                                row[sitecol["id_units"]] = others[dlg.selected()][
                                    unitcol["id"]
                                ]
                                self.sites.updateRow(idx, row)
                    # delete sites and related data
                    scount, dcount = self.db_removeUnit(self.units.row2id[index.row()])
                    self.units.removeRow(index)
                    # self.sortsites.reset()
                    self.statusBar().showMessage(
                        f"Unit {todel[unitcol['name']]}, {scount} sites and {dcount} data have been deleted.",
                        5000,
                    )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Delete unit",
                    "There must be at least one unit defined in database!",
                )

    def moveUnitUp(self):
        """Move selected unit up."""
        indexlist = self.unitSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() > 0:
                self.db_swapposUnit(
                    self.units._items[index.row()][unitcol["id"]],
                    self.units._items[index.row() - 1][unitcol["id"]],
                )
                cache = self.units.getRow(index)
                self.units.removeRow(index)
                self.units.appendRow(cache, index, -1)
                self.ui.unitsView.selectRow(index.row() - 1)
                self.ui.unitsView.setFocus()

    def moveUnitDown(self):
        """Move selected unit up."""
        indexlist = self.unitSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() + 1 < self.units.rowCount():
                self.db_swapposUnit(
                    self.units._items[index.row()][unitcol["id"]],
                    self.units._items[index.row() + 1][unitcol["id"]],
                )
                cache = self.units.getRow(index)
                self.units.removeRow(index)
                self.units.appendRow(cache, index, 1)
                self.ui.unitsView.selectRow(index.row() + 1)
                self.ui.unitsView.setFocus()

    def db_addUnit(self, data):
        """Add unit to database."""
        pos = self.conn.execute("SELECT MAX(pos)+1 FROM units").fetchall()[0][0]
        if not pos:
            pos = 1
        self.changed = True
        return self.conn.execute(
            "INSERT OR IGNORE INTO units (pos, name, description) VALUES (?,?,?)",
            (pos, data[unitcol["name"]], data[unitcol["desc"]]),
        )

    def db_updateUnit(self, data):
        """Update unit in database."""
        return self.conn.execute(
            "UPDATE OR IGNORE units SET name=?, description=? WHERE id=?",
            (data[unitcol["name"]], data[unitcol["desc"]], data[unitcol["id"]]),
        )

    def db_removeUnit(self, id):
        """Remove unit in database."""
        # delete related sites
        scount = 0
        dcount = 0
        for dat in self.conn.execute("SELECT id FROM sites WHERE id_units=?", (id,)):
            scount += 1
            dcount += self.db_removeSite(dat[0])
        self.conn.execute("DELETE FROM units WHERE id=?", (id,))
        self.changed = True
        return scount, dcount

    def db_swapposUnit(self, aid, bid):
        apos = self.conn.execute("SELECT pos FROM units WHERE id=?", (aid,)).fetchall()[
            0
        ][0]
        bpos = self.conn.execute("SELECT pos FROM units WHERE id=?", (bid,)).fetchall()[
            0
        ][0]
        self.conn.execute("UPDATE units SET pos=? WHERE id=?", (bpos, aid))
        self.conn.execute("UPDATE units SET pos=? WHERE id=?", (apos, bid))
        self.changed = True

    # ----------------------------------------------------------------------
    # TAG VIEW
    # ----------------------------------------------------------------------
    def addTagDlg(self):
        """Open add tag dialog."""
        dlg = DialogAddEditTag("Add")
        if dlg.exec_():
            cur = self.db_addTag(dlg.data)
            if cur.rowcount > 0:
                dlg.data[tagcol["id"]] = cur.lastrowid
                self.tags.appendRow(dlg.data)
                self.statusBar().showMessage(
                    f"Tag {dlg.data[tagcol['name']]} added.", 5000
                )
                self.ui.tagsView.scrollToBottom()
            else:
                self.statusBar().showMessage(
                    f"Tag {dlg.data[tagcol['name']]} already exists.", 5000
                )
            # self.siteSelection.setCurrentIndex(self.sites.index(self.sites.rowCount()-1,sitecol['name']), QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
            self.ui.tagsView.setFocus()

    def editTagDlg(self, index):
        """Open edit tag dialog."""
        dlg = DialogAddEditTag("Edit", self.tags.getRow(index))
        if dlg.exec_():
            cur = self.db_updateTag(dlg.data)
            if cur.rowcount > 0:
                self.tags.updateRow(index, dlg.data)
                self.statusBar().showMessage(
                    f"Tag {dlg.data[tagcol['name']]} added.", 5000
                )
            else:
                self.statusBar().showMessage(
                    f"Tag {dlg.data[tagcol['name']]} already exists.", 5000
                )

    def removeTagDlg(self):
        """Remove selected tag from database."""
        indexlist = self.tagSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            todel = self.tags.getRow(index)
            others = [
                [row[tagcol["id"]], row[tagcol["name"]]]
                for row in self.tags._items
                if row[tagcol["id"]] != todel[tagcol["id"]]
            ]
            dlg = DialogSaveDiscard(
                [r[1] for r in others],
                f"Do you want to delete tag {todel[tagcol['name']]}?",
                "Assign another tag to data:",
            )
            if dlg.exec_():
                if dlg.checked() and (len(others) > 0):
                    # assign other tags to data
                    self.conn.execute(
                        "UPDATE tagged SET id_tags=? WHERE id_tags=?",
                        (others[dlg.selected()][tagcol["id"]], todel[tagcol["id"]]),
                    )
                # delete tags
                self.db_removeTag(self.tags.row2id[index.row()])
                self.tags.removeRow(index)
                # self.sortsites.reset()
                self.siteselChanged()
                self.statusBar().showMessage(
                    f"Tag {todel[tagcol['name']]} have been deleted.", 5000
                )

    def moveTagUp(self):
        """Move selected tag up."""
        indexlist = self.tagSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() > 0:
                self.db_swapposTag(
                    self.tags._items[index.row()][tagcol["id"]],
                    self.tags._items[index.row() - 1][tagcol["id"]],
                )
                cache = self.tags.getRow(index)
                self.tags.removeRow(index)
                self.tags.appendRow(cache, index, -1)
                self.ui.tagsView.selectRow(index.row() - 1)
                self.ui.tagsView.setFocus()

    def moveTagDown(self):
        """Move selected tag up."""
        indexlist = self.tagSelection.selectedRows()
        if indexlist:
            index = indexlist[0]
            if index.row() + 1 < self.tags.rowCount():
                self.db_swapposTag(
                    self.tags._items[index.row()][tagcol["id"]],
                    self.tags._items[index.row() + 1][tagcol["id"]],
                )
                cache = self.tags.getRow(index)
                self.tags.removeRow(index)
                self.tags.appendRow(cache, index, 1)
                self.ui.tagsView.selectRow(index.row() + 1)
                self.ui.tagsView.setFocus()

    def db_addTag(self, data):
        """Add tag to database."""
        pos = self.conn.execute("SELECT MAX(pos)+1 FROM tags").fetchall()[0][0]
        if pos is None:
            pos = 1
        self.changed = True
        return self.conn.execute(
            "INSERT OR IGNORE INTO tags (pos, name, description) VALUES (?,?,?)",
            (pos, data[tagcol["name"]], data[tagcol["desc"]]),
        )

    def db_updateTag(self, data):
        """Update tag in database."""
        self.changed = True
        return self.conn.execute(
            "UPDATE OR IGNORE tags SET name=?, description=? WHERE id=?",
            (data[tagcol["name"]], data[tagcol["desc"]], data[tagcol["id"]]),
        )

    def db_removeTag(self, id):
        """Remove tag in database."""
        self.conn.execute("DELETE FROM tags WHERE id=?", (id,))
        self.changed = True

    def db_swapposTag(self, aid, bid):
        apos = self.conn.execute("SELECT pos FROM tags WHERE id=?", (aid,)).fetchall()[
            0
        ][0]
        bpos = self.conn.execute("SELECT pos FROM tags WHERE id=?", (bid,)).fetchall()[
            0
        ][0]
        self.conn.execute("UPDATE tags SET pos=? WHERE id=?", (bpos, aid))
        self.conn.execute("UPDATE tags SET pos=? WHERE id=?", (apos, bid))
        self.changed = True


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
