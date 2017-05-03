# I'm using PySide, Nokia's official LGPL bindings.
# You can however easily use PyQt (Riverside Computing's GPL bindings) by commenting this and fixing the appropriate import.

import sys
import os

__version__ = '3.0.3'

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
