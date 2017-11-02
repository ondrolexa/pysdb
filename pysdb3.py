#!/usr/bin/env python3 

import sys
import os

from pysdb3.mainapp import *

# set things up, and run it. :)
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# set tags
        # for row in self.tagged:
        #     item = QtGui.QListWidgetItem()
        #     cb = QtGui.QCheckBox(row[1])
        #     cb.setTristate(True)
        #     cb.setCheckState(row[2])
        #     item.setSizeHint(cb.sizeHint())
        #     self.ui.taggedList.addItem(item)
        #     self.ui.taggedList.setItemWidget(item, cb)
