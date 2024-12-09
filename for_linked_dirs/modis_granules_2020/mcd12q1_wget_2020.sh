#!/bin/bash

wget --timestamping -m -e robots=off --cut-dirs=1 --user-agent=Mozilla/5.0 --reject="*.xml" --reject="*.jpg" --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories https://e4ftl01.cr.usgs.gov/MOTA/MCD12Q1.006/2020.01.01/


