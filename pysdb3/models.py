from PyQt5 import QtCore, QtGui

sitecol = {"id": 0, "name": 1, "x": 2, "y": 3, "desc": 4, "id_units": 5}
datacol = {
    "id": 0,
    "id_sites": 1,
    "id_struct": 2,
    "azi": 3,
    "inc": 4,
    "struct": 5,
    "desc": 6,
    "tags": 7,
}
structurecol = {"id": 0, "structure": 1, "planar": 2, "desc": 3, "scode": 4, "gcode": 5}
unitcol = {"id": 0, "name": 1, "desc": 2}
tagcol = {"id": 0, "name": 1, "desc": 2, "check": 3}

SCHEMA = """pragma auto_vacuum=0;
pragma default_cache_size=2000;
pragma encoding='UTF-8';
pragma page_size=1024;
drop table if exists sites;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS "meta";
CREATE TABLE IF NOT EXISTS "meta" ("id" INTEGER NOT NULL, "name" VARCHAR(16) NOT NULL, "value" TEXT, PRIMARY KEY("id"));
DROP TABLE IF EXISTS "structype";
CREATE TABLE IF NOT EXISTS "structype" ("id" INTEGER NOT NULL, "pos" INTEGER NOT NULL DEFAULT 0, "structure" VARCHAR(16) NOT NULL, "description" TEXT, "structcode" INTEGER DEFAULT 0, "groupcode" INTEGER DEFAULT 0, "planar" INTEGER DEFAULT 1, PRIMARY KEY("id"), CONSTRAINT "_structype_structure_uc" UNIQUE("structure"));
DROP TABLE IF EXISTS "tags";
CREATE TABLE IF NOT EXISTS "tags" ("id" INTEGER NOT NULL, "pos" INTEGER NOT NULL DEFAULT 0, "name" VARCHAR(16) NOT NULL, "description" TEXT, PRIMARY KEY("id"), CONSTRAINT "_tag_name_uc" UNIQUE("name"));
DROP TABLE IF EXISTS "units";
CREATE TABLE IF NOT EXISTS "units" ("id" INTEGER NOT NULL, "pos" INTEGER NOT NULL DEFAULT 0, "name" VARCHAR(60) NOT NULL, "description" TEXT, PRIMARY KEY("id"), CONSTRAINT "_unit_name_uc" UNIQUE("name"));
DROP TABLE IF EXISTS "sites";
CREATE TABLE IF NOT EXISTS "sites" ("id" INTEGER NOT NULL, "id_units" INTEGER NOT NULL, "name" VARCHAR(16) NOT NULL, "x_coord" FLOAT DEFAULT NULL, "y_coord" FLOAT DEFAULT NULL, "description" TEXT, FOREIGN KEY("id_units") REFERENCES "units"("id"), PRIMARY KEY("id"), CONSTRAINT "_site_name_uc" UNIQUE("name"));
DROP TABLE IF EXISTS "structdata";
CREATE TABLE IF NOT EXISTS "structdata" ("id" INTEGER NOT NULL, "id_sites" INTEGER NOT NULL, "id_structype" INTEGER NOT NULL, "azimuth" FLOAT NOT NULL DEFAULT 0, "inclination" FLOAT NOT NULL DEFAULT 0, "description" TEXT, FOREIGN KEY("id_sites") REFERENCES "sites"("id"), FOREIGN KEY("id_structype") REFERENCES "structype"("id"), PRIMARY KEY("id"));
DROP TABLE IF EXISTS "tagged";
CREATE TABLE IF NOT EXISTS "tagged" ("id" INTEGER NOT NULL, "id_tags" INTEGER NOT NULL, "id_structdata" INTEGER NOT NULL, FOREIGN KEY("id_tags") REFERENCES "tags"("id"), PRIMARY KEY("id"), FOREIGN KEY("id_structdata") REFERENCES "structdata"("id"));
DROP TABLE IF EXISTS "attach";
CREATE TABLE IF NOT EXISTS "attach" ("id" INTEGER NOT NULL, "id_structdata_planar" INTEGER NOT NULL, "id_structdata_linear" INTEGER NOT NULL, FOREIGN KEY("id_structdata_planar") REFERENCES "structdata"("id"), PRIMARY KEY("id"), FOREIGN KEY("id_structdata_linear") REFERENCES "structdata"("id"));
DROP INDEX IF EXISTS "ix_sites_id_units";
CREATE INDEX IF NOT EXISTS "ix_sites_id_units" ON "sites" ("id_units");
DROP INDEX IF EXISTS "ix_structdata_id_sites";
CREATE INDEX IF NOT EXISTS "ix_structdata_id_sites" ON "structdata" ("id_sites");
DROP INDEX IF EXISTS "ix_structdata_id_structype";
CREATE INDEX IF NOT EXISTS "ix_structdata_id_structype" ON "structdata" ("id_structype");
DROP INDEX IF EXISTS "ix_tagged_id_tags";
CREATE INDEX IF NOT EXISTS "ix_tagged_id_tags" ON "tagged" ("id_tags");
DROP INDEX IF EXISTS "ix_tagged_id_structdata";
CREATE INDEX IF NOT EXISTS "ix_tagged_id_structdata" ON "tagged" ("id_structdata");
DROP INDEX IF EXISTS "ix_attach_id_structdata_linear";
CREATE INDEX IF NOT EXISTS "ix_attach_id_structdata_linear" ON "attach" ("id_structdata_linear");
DROP INDEX IF EXISTS "ix_attach_id_structdata_planar";
CREATE INDEX IF NOT EXISTS "ix_attach_id_structdata_planar" ON "attach" ("id_structdata_planar");
COMMIT;"""

DEFDATA = """INSERT INTO structype VALUES (1, 1,'S', 'Default planar feature', 35, 13, 1);
INSERT INTO structype VALUES (2, 2, 'L', 'Default linear feature', 78, 13, 0);
INSERT INTO units VALUES (1, 1, 'Default', 'Default unit');"""


class SiteModel(QtCore.QAbstractTableModel):
    # Here we define model to store sites table data
    def __init__(self, mlist, parent=None):
        super(SiteModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()

    def updateIndex(self):
        """Update lookup dictionaries for id and row."""
        self.id2row = {}
        self.row2id = {}
        for idx, row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """Returns the number of rows the model holds."""
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """Returns the number of columns the model holds."""
        return len(sitecol)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            return self._items[index.row()][index.column()]
        elif role == QtCore.Qt.ToolTipRole:
            # The view is asking for tooltip data, so, we just return description.
            return self._items[index.row()][sitecol["desc"]]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def getRow(self, index):
        """Returns model row."""
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """Updates model row."""
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        # self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow):
        """Append model row."""
        self.beginInsertRows(QtCore.QModelIndex(), len(self._items), len(self._items))
        self._items.append(datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """Remove model row."""
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set the headers to be displayed."""
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == sitecol["name"]:
                return "Site"
            else:
                return None

        return None


class StructureModel(QtCore.QAbstractTableModel):
    # Here we define model to store structures table data
    def __init__(self, mlist, parent=None):
        super(StructureModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()

    def updateIndex(self):
        """Update lookup dictionaries for id and row."""
        self.id2row = {}
        self.row2id = {}
        for idx, row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """Returns the number of rows the model holds."""
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """Returns the number of columns the model holds."""
        return len(structurecol)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            return self._items[index.row()][index.column()]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def getRow(self, index):
        """Returns model row."""
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """Updates model row."""
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        # self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """Append model row."""
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """Remove model row."""
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()

    def isplanar(self, row):
        return self._items[row][structurecol["planar"]] == 1


class UnitModel(QtCore.QAbstractTableModel):
    # Here we define model to store units table data
    def __init__(self, mlist, parent=None):
        super(UnitModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()

    def updateIndex(self):
        """Update lookup dictionaries for id and row."""
        self.id2row = {}
        self.row2id = {}
        for idx, row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """Returns the number of rows the model holds."""
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """Returns the number of columns the model holds."""
        return len(unitcol)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            return self._items[index.row()][index.column()]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def getRow(self, index):
        """Returns model row."""
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """Updates model row."""
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        # self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """Append model row."""
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """Remove model row."""
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()


class TagModel(QtCore.QAbstractTableModel):
    # Here we define model to store tags table data
    def __init__(self, mlist, parent=None):
        super(TagModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()

    def updateIndex(self):
        """Update lookup dictionaries for id and row."""
        self.id2row = {}
        self.row2id = {}
        for idx, row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """Returns the number of rows the model holds."""
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """Returns the number of columns the model holds."""
        return len(tagcol)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.CheckStateRole and index.column() == tagcol["check"]:
            # The view is asking for the actual state of checkable item.
            return self._items[index.row()][index.column()]

        elif role == QtCore.Qt.FontRole and index.column() == tagcol["check"]:
            # The view is asking for the font properties.
            font = QtGui.QFont()
            if self._items[index.row()][index.column()] == QtCore.Qt.Checked:
                font.setBold(True)
            else:
                font.setBold(False)
            return font

        elif role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            if index.column() == tagcol["check"]:
                return self._items[index.row()][tagcol["name"]]
            else:
                return self._items[index.row()][index.column()]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column() == tagcol["check"]:
            return (
                QtCore.Qt.ItemIsEnabled
                | QtCore.Qt.ItemIsUserCheckable
                | QtCore.Qt.ItemIsSelectable
            )
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if index.column() == tagcol["check"]:
                self._items[index.row()][index.column()] = value

        self.dataChanged.emit(index, index)
        return True

    def getChecked(self):
        return [
            row[tagcol["id"]]
            for row in self._items
            if row[tagcol["check"]] == QtCore.Qt.Checked
        ]

    def cleanState(self):
        for row in self._items:
            row[tagcol["check"]] = QtCore.Qt.Unchecked

    def setState(self, ids):
        for row in self._items:
            if row[tagcol["id"]] in ids:
                row[tagcol["check"]] = QtCore.Qt.Checked
            else:
                row[tagcol["check"]] = QtCore.Qt.Unchecked

    def getRow(self, index):
        """Returns model row."""
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """Updates model row."""
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        # self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """Append model row."""
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """Remove model row."""
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()


class DataModel(QtCore.QAbstractTableModel):
    # Here we define model to store data table
    def __init__(self, mlist, parent=None):
        super(DataModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()

    def updateIndex(self):
        """Update lookup dictionaries for id and row."""
        self.id2row = {}
        self.row2id = {}
        for idx, row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """Returns the number of rows the model holds."""
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """Returns the number of columns the model holds."""
        return len(datacol)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """Depending on the index and role given, return data. If not
        returning data, return None (PySide equivalent of QT's
        "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            return self._items[index.row()][index.column()]
        elif role == QtCore.Qt.ToolTipRole:
            # The view is asking for tooltip data, so, we just return description.
            return self._items[index.row()][datacol["desc"]]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def getRow(self, index):
        """Returns model row."""
        return self._items[index.row()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Set the headers to be displayed."""
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == datacol["azi"]:
                return "Azimuth"
            elif section == datacol["inc"]:
                return "Inclination"
            elif section == datacol["struct"]:
                return "Structure"
            elif section == datacol["tags"]:
                return "Tags"
            else:
                return None

        return None
