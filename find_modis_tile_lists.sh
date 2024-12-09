#!/bin/bash

# find all the MODIS tiles with values in the NH and SH

# Note: this takes advantage of extended-grep to extract matches
#       to h??v?? where ? are digits
#   and
#       sort uses columns 5 and 6 from "word" 1 (the h??v?? string)
#
# Note: the SH requires matching v09 and v1?, which are done as
#       separate matchgroups (abc)|(def)
# Outputs:
#     modis_granule_list_nh.txt
#     modis_granule_list_sh.txt

modis_dir=/data/mcd12q1/modis_granules_2020
echo "Extracting modis granules from: ${modis_dir}"

modis_list_fn_nh=modis_granule_list_nh.txt
modis_list_fn_sh=modis_granule_list_sh.txt

# Create NH list
# Note: The sort arguments cause this to sort by the v?? numbers
ls ${modis_dir}/MCD12Q1.*.hdf | grep -Eo 'h[0-9][0-9]v0[0-8]' | sort -k 1.5,1.6 > ${modis_list_fn_nh}
echo "Wrote list of NH modis tiles to: {modis_list_fn_nh}"

# Create SH list
# Note: The sort arguments cause this to sort by the v?? numbers
ls ${modis_dir}/MCD12Q1.*.hdf | grep -Eo '(h[0-9][0-9]v09)|(h[0-9][0-9]v1[0-9])' | sort -k 1.5,1.6 > ${modis_list_fn_sh}
echo "Wrote list of SH modis tiles to: {modis_list_fn_sh}"
