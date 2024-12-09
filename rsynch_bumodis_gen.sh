#!/bin/bash

# rsynch_bumodis_gen.sh
#
# synchronize the generalized BUMODIS land mask code onto easystore

#<<DATADIR
# This is the "data directory" section...
rs_srcdir=/home/scotts/bumodis_gen
rs_dstdir=/media/scotts/easystore/bumodis_gen

rsync -av --exclude="./.*" ${rs_srcdir} ${rs_dstdir}
