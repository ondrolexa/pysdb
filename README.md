# pysdb - python structural database

GUI front-end to creat, edit and manage the field structural geology data in sqlite3 file database (SDB structural database). This database format is compatible
with [readsdb QGIS3 plugin](https://github.com/ondrolexa/readsdb) to plot data from SDB structural database on the map or stereonet. For advanced analyses and visualization, it could be used with APSG toolbox (https://github.com/ondrolexa/apsg). 

## How to install

Easiest way to install **pysdb** is to use conda package management system. Create conda environment from the included `environment.yml` file:

    conda env create -f environment.yml

or manually:

    conda create -n pysdb python=3.8 pyqt=5

Then activate the new environment:

    conda activate pysdb

and install pysdb using pip:

    pip install https://github.com/ondrolexa/pysdb/archive/master.zip

or if you downloaded pypsbuilder repository, run in unzipped folder:

    pip install .

## License

pysdb is free software: you can redistribute it and/or modify it under the terms of the MIT License. A copy of this license is provided in ``LICENSE`` file.