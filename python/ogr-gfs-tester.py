#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jürgen Weichand'
from osgeo import gdal
from osgeo import ogr
import urllib

import logging
import sys
import os
import json
import shutil

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

if len(sys.argv) != 3:
    print "usage: python ogr-gml-tester.py <gml-file> <gfs-file>"
    sys.exit(1)

# Delete existing Testfiles
gmlfilename = sys.argv[1]
customgfs = sys.argv[2]

gmlresolved = gmlfilename.replace(".gml", ".resolved.gml")
gfsfilename = gmlfilename.replace("gml", "gfs")
if os.path.isfile(gmlresolved):
    os.remove(gmlresolved)
if os.path.isfile(gfsfilename):
    os.remove(gfsfilename)
shutil.copyfile(customgfs, gfsfilename)

# GdalConfigOptions
CPL_DEBUG = "CPL_DEBUG"
CPL_LOG = "CPL_LOG"
GDAL_HTTP_TIMEOUT = "GDAL_HTTP_TIMEOUT"
GML_SKIP_RESOLVE_ELEMS = "GML_SKIP_RESOLVE_ELEMS"
GML_ATTRIBUTES_TO_OGR_FIELDS = "GML_ATTRIBUTES_TO_OGR_FIELDS"
GML_GFS_TEMPLATE = "GML_GFS_TEMPLATE"

gdal.SetConfigOption(CPL_DEBUG, "ON")
gdal.SetConfigOption(CPL_LOG, "/tmp/gdal.log")
gdal.SetConfigOption(GDAL_HTTP_TIMEOUT, "3")
gdal.SetConfigOption(GML_SKIP_RESOLVE_ELEMS, "NONE")
gdal.SetConfigOption(GML_ATTRIBUTES_TO_OGR_FIELDS, "NO")
#gdal.SetConfigOption(GML_GFS_TEMPLATE, customgfs)

root.debug("GdalConfigOptions")
root.debug(CPL_DEBUG + "=" + gdal.GetConfigOption(CPL_DEBUG))
root.debug(CPL_LOG + "=" + gdal.GetConfigOption(CPL_LOG))
root.debug(GDAL_HTTP_TIMEOUT + "=" + gdal.GetConfigOption(GDAL_HTTP_TIMEOUT))
root.debug(GML_SKIP_RESOLVE_ELEMS + "=" + gdal.GetConfigOption(GML_SKIP_RESOLVE_ELEMS))
root.debug(GML_ATTRIBUTES_TO_OGR_FIELDS + "=" + gdal.GetConfigOption(GML_ATTRIBUTES_TO_OGR_FIELDS))
#root.debug(GML_GFS_TEMPLATE + "=" + gdal.GetConfigOption(GML_GFS_TEMPLATE))
root.debug("")

ogrdriver = ogr.GetDriverByName("GML")
root.debug("OGR-Driver: " + ogrdriver.GetName())
root.debug("Opening " + gmlfilename)

ogrdatasource = ogrdriver.Open(gmlfilename, 0)
root.debug("... done")
root.debug("")

if ogrdatasource is None:
    root.debug("OGR-Datasource is None")
else:
    for i in range(0, 1):
        root.debug("Layer(" + str(i) + ") " + ogrdatasource.GetLayerByIndex(i).GetName())
        ogrlayer = ogrdatasource.GetLayerByIndex(i)
        ogrfeature = ogrlayer.GetNextFeature()
        print(json.dumps(json.loads(ogrfeature.ExportToJson()), indent=4, sort_keys=True))
