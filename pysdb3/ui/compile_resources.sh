#!/bin/bash
pyuic5 --from-imports -o ../ui_pysdb3.py pysdb3.ui
pyuic5 --from-imports -o ../ui_addeditdata.py addeditdata.ui
pyuic5 --from-imports -o ../ui_addeditsite.py addeditsite.ui
pyuic5 --from-imports -o ../ui_addeditstructure.py addeditstructure.ui
pyuic5 --from-imports -o ../ui_addedittag.py addedittag.ui
pyuic5 --from-imports -o ../ui_addeditunit.py addeditunit.ui
pyuic5 --from-imports -o ../ui_savediscard.py savediscard.ui
pyuic5 --from-imports -o ../ui_datafilter.py datafilter.ui
pyuic5 --from-imports -o ../ui_sitefilter.py sitefilter.ui
pyuic5 --from-imports -o ../ui_sdbinfo.py sdbinfo.ui
pyuic5 --from-imports -o ../ui_importsitesfile.py importsitesfile.ui
pyuic5 --from-imports -o ../ui_selectunit.py selectunit.ui
pyuic5 --from-imports -o ../ui_multieditdata.py multieditdata.ui
pyrcc5 -o ../pysdb3_rc.py pysdb3.qrc
