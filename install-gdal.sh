#!/bin/bash
gdal_version=1.11.2
mkdir /tmp/
cd /tmp/
wget http://download.osgeo.org/gdal/$gdal_version/gdal-$gdal_version.tar.gz
tar xvzf gdal-$gdal_version.tar.gz
cd gdal-$gdal_version
./configure
make
make install
cd