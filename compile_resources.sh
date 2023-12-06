#!/bin/bash
pyuic5 --from-imports -o pysdb3/ui_pysdb3.py pysdb3/ui/pysdb3.ui
pyuic5 --from-imports -o pysdb3/ui_addeditdata.py pysdb3/ui/addeditdata.ui
pyuic5 --from-imports -o pysdb3/ui_addeditsite.py pysdb3/ui/addeditsite.ui
pyuic5 --from-imports -o pysdb3/ui_addeditstructure.py pysdb3/ui/addeditstructure.ui
pyuic5 --from-imports -o pysdb3/ui_addedittag.py pysdb3/ui/addedittag.ui
pyuic5 --from-imports -o pysdb3/ui_addeditunit.py pysdb3/ui/addeditunit.ui
pyuic5 --from-imports -o pysdb3/ui_savediscard.py pysdb3/ui/savediscard.ui
pyuic5 --from-imports -o pysdb3/ui_datafilter.py pysdb3/ui/datafilter.ui
pyuic5 --from-imports -o pysdb3/ui_sitefilter.py pysdb3/ui/sitefilter.ui
pyuic5 --from-imports -o pysdb3/ui_sdbinfo.py pysdb3/ui/sdbinfo.ui
pyuic5 --from-imports -o pysdb3/ui_importsitesfile.py pysdb3/ui/importsitesfile.ui
pyuic5 --from-imports -o pysdb3/ui_selectunit.py pysdb3/ui/selectunit.ui
pyuic5 --from-imports -o pysdb3/ui_multieditdata.py pysdb3/ui/multieditdata.ui
pyrcc5 -o pysdb3/pysdb3_rc.py pysdb3/ui/pysdb3.qrc
