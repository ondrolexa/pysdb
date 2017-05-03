from PyQt5 import QtCore, QtGui, QtWidgets

sitecol = {'id':0,'name':1,'x':2,'y':3,'desc':4,'id_units':5}
datacol = {'id':0,'id_sites':1,'id_struct':2,'azi':3,'inc':4,'struct':5,'desc':6,'tags':7}
structurecol = {'id':0,'structure':1,'planar':2,'desc':3,'scode':4,'gcode':5}
unitcol = {'id':0,'name':1,'desc':2}
tagcol = {'id':0,'name':1,'desc':2,'check':3}

class SiteModel(QtCore.QAbstractTableModel):
    # Here we define model to store sites table data
    def __init__(self, mlist, parent=None):
        super(SiteModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()
    
    def updateIndex(self):
        """ Update lookup dictionaries for id and row. """
        self.id2row = {}
        self.row2id = {}
        for idx,row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(sitecol)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
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
            return self._items[index.row()][sitecol['desc']]
        else:
            # We don't care about anything else, so make sure to return None.
            return None
    def getRow(self, index):
        """ Returns model row. """
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """ Updates model row. """
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        #self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow):
        """ Append model row. """
        self.beginInsertRows(QtCore.QModelIndex(), len(self._items), len(self._items))
        self._items.append(datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """ Remove model row. """
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == sitecol['name']:
                return 'Site'
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
        """ Update lookup dictionaries for id and row. """
        self.id2row = {}
        self.row2id = {}
        for idx,row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(structurecol)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
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
        """ Returns model row. """
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """ Updates model row. """
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        #self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """ Append model row. """
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """ Remove model row. """
        self.beginRemoveRows(QtCore.QModelIndex(), index.row(), index.row())
        del self._items[index.row()]
        self.endRemoveRows()
        self.updateIndex()

    def isplanar(self, row):
        return self._items[row][2] == 1

class UnitModel(QtCore.QAbstractTableModel):
    # Here we define model to store units table data
    def __init__(self, mlist, parent=None):
        super(UnitModel, self).__init__(parent)

        # Cache the passed data list as a class member.
        self._items = mlist
        # Create lookup dictionaries
        self.updateIndex()
    
    def updateIndex(self):
        """ Update lookup dictionaries for id and row. """
        self.id2row = {}
        self.row2id = {}
        for idx,row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]
    
    def rowCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self._items)
    
    def columnCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(unitcol)
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
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
        """ Returns model row. """
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """ Updates model row. """
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        #self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """ Append model row. """
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """ Remove model row. """
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
        """ Update lookup dictionaries for id and row. """
        self.id2row = {}
        self.row2id = {}
        for idx,row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(tagcol)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
            returning data, return None (PySide equivalent of QT's 
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._items):
            return None

        if role == QtCore.Qt.CheckStateRole and index.column() == tagcol['check']:
            # The view is asking for the actual state of checkable item.
                return self._items[index.row()][index.column()]

        elif role == QtCore.Qt.FontRole and index.column() == tagcol['check']:
             # The view is asking for the font properties.
            font = QtGui.QFont()
            if self._items[index.row()][index.column()] == QtCore.Qt.Checked:
                font.setBold(True)
            else:
                font.setBold(False)
            return font

        elif role == QtCore.Qt.DisplayRole:
            # The view is asking for the actual data, so, just return the item it's asking for.
            if index.column() == tagcol['check']:
                return self._items[index.row()][tagcol['name']]
            else:
                return self._items[index.row()][index.column()]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def flags (self, index):
        if not index.isValid():
            return None
        if index.column() == tagcol['check']:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData (self, index, value, role):
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if index.column() == tagcol['check']:
                self._items[index.row()][index.column()] = value

        self.dataChanged.emit(index, index)
        return True

    def getChecked(self):
        return [row[tagcol['id']] for row in self._items if row[tagcol['check']] == QtCore.Qt.Checked]

    def setState(self, ids):
        for row in self._items:
            if row[tagcol['id']] in ids:
                row[tagcol['check']] = QtCore.Qt.Checked
            else:
                row[tagcol['check']] = QtCore.Qt.Unchecked
    
    def getRow(self, index):
        """ Returns model row. """
        return self._items[index.row()]

    def updateRow(self, index, datarow):
        """ Updates model row. """
        self._items[index.row()] = datarow
        self.dataChanged.emit(index, index)
        #self.emit(QtCore.SIGNAL('dataChanged(QModelIndex,QModelIndex)'), index, index)

    def appendRow(self, datarow, index=None, offset=0):
        """ Append model row. """
        if index is None:
            pos = len(self._items)
        else:
            pos = index.row() + offset
        self.beginInsertRows(QtCore.QModelIndex(), pos, pos)
        self._items.insert(pos, datarow)
        self.endInsertRows()
        self.updateIndex()

    def removeRow(self, index):
        """ Remove model row. """
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
        """ Update lookup dictionaries for id and row. """
        self.id2row = {}
        self.row2id = {}
        for idx,row in enumerate(self._items):
            self.id2row[row[0]] = idx
            self.row2id[idx] = row[0]

    def rowCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self._items)

    def columnCount(self, index=QtCore.QModelIndex()):
        """ Returns the number of columns the model holds. """
        return len(datacol)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not 
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
            return self._items[index.row()][datacol['desc']]
        else:
            # We don't care about anything else, so make sure to return None.
            return None

    def getRow(self, index):
        """ Returns model row. """
        return self._items[index.row()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            if section == datacol['azi']:
                return "Azimuth"
            elif section == datacol['inc']:
                return "Inclination"
            elif section == datacol['struct']:
                return "Structure"
            elif section == datacol['tags']:
                return "Tags"
            else:
                return None

        return None


