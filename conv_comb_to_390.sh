#!/bin/bash

# convert_comb_to_390.sh
# Based on convert_comb_to_pss390.sh

# Convert the lnd, wtr, ice grids from native multi-tile resolution to PSS tile

# Usage:
#  ./convert_comb_to_390.sh <projid>
# eg
# ./conv_comb_to_390.sh e2n
# ./conv_comb_to_390.sh e2s
# ./conv_comb_to_390.sh psn
# ./conv_comb_to_390.sh pss

projid=$1
if [ -z $projid ]; then
  echo "Usage:  ./convert_comb_to_390.sh <projid>"
  echo "  eg"
  echo "        ./convert_comb_to_390.sh e2n"
  echo "        ./convert_comb_to_390.sh e2s"
  echo "        ./convert_comb_to_390.sh psn"
  echo "        ./convert_comb_to_390.sh pss"
  exit 1
fi

hires=390

for tileid in x0y0_left x0y0_right \
  x0y0 x0y1 x0y2 x0y3 \
  x1y0 x1y1 x1y2 x1y3 \
  x2y0 x2y1 x2y2 x2y3 \
  x3y0 x3y1 x3y2 x3y3 ; do
  # The comb_id values are manually set after looking through
  # the values in: ./modids_pss/pss390_x?y?_modids.txt
  # ...or the output of combine_datfiles_pss.py (saved to com ... .out)

  combo_gpd_fn=./combined_gpds_${projid}/combinedsinu_for_${projid}_${tileid}.gpd
  if [ -f $combo_gpd_fn ]; then
    hires_subgrid_gpd=./${projid}_gpds/${projid}${hires}_${tileid}.gpd
    hires_subgrid_dir=./${projid}${hires}_fields
    mkdir -p $hires_subgrid_dir

    echo "  regridding land..."
    date
    combo_lnd_fn=./combined_fields_${projid}/combinedsinu_for_${projid}_${tileid}_lnd.dat
    hires_subgrid_lnd_fn=${hires_subgrid_dir}/${projid}${hires}_${tileid}_lnd.dat
    regrid -v -w -u -i 255 \
      $combo_gpd_fn \
      $hires_subgrid_gpd \
      $combo_lnd_fn \
      $hires_subgrid_lnd_fn

    echo "  regridding water..."
    date
    combo_wtr_fn=./combined_fields_${projid}/combinedsinu_for_${projid}_${tileid}_wtr.dat
    hires_subgrid_wtr_fn=${hires_subgrid_dir}/${projid}${hires}_${tileid}_wtr.dat
    regrid -v -w -u -i 255 \
      $combo_gpd_fn \
      $hires_subgrid_gpd \
      $combo_wtr_fn \
      $hires_subgrid_wtr_fn

    echo "  regridding ice..."
    date
    combo_ice_fn=./combined_fields_${projid}/combinedsinu_for_${projid}_${tileid}_ice.dat
    hires_subgrid_ice_fn=${hires_subgrid_dir}/${projid}${hires}_${tileid}_ice.dat
    regrid -v -w -u -i 255 \
      $combo_gpd_fn \
      $hires_subgrid_gpd \
      $combo_ice_fn \
      $hires_subgrid_ice_fn
    date

  else
    echo "Skipping not-found tileid: ${tileid}"
  fi

done
