#!/bin/bash

# extract_lcvar_nc.sh

# Recommended usage:
#  ./extract_lcvar_nc.sh |& tee extract_lcvar_nc.sh.out
# Uses:
#  modis_dir: eg /data/mcd12q1/modis_granules/2020/
# Specify the MCD12Q1 land classification type to use:
#    e.g. LC_Type1
#  scripts for NCO 'ncap':
#    is_land_LC_Type1.ncap
#    is_water_LC_Type1.ncap
#    is_ice_LC_Type1.ncap
#  output dir (probably symlinked to /data/...)
#    modis_LC_Type1/

echo "Started $0 at: $(date)"

# overwrite=FALSE
overwrite=TRUE
if [[ "$overwrite" == TRUE ]]; then
  echo " "
  echo "Overwriting output .nc files if they exist..."
  echo " "
fi

# Input
modis_dir=/data/mcd12q1/modis_granules_2020
landcover_varname=LC_Type1

is_land_ncap_input=./is_land_${landcover_varname}.ncap
is_water_ncap_input=./is_water_${landcover_varname}.ncap
is_ice_ncap_input=./is_ice_${landcover_varname}.ncap

# Output directory
lc1dir=./modis_${landcover_varname}
mkdir -p $lc1dir

# Temp files
stderr_fn=.cmd_stderr

for tilelist_fn in ./modis_granule_list_nh.txt ./modis_granule_list_sh.txt; do
  for modid in $(cat ${tilelist_fn}); do
    echo "modid: $modid"

    lc_fname=${lc1dir}/modis_${landcover_varname}_${modid}.nc

    lnd_lcperc_fname=${lc1dir}/modis_${landcover_varname}_${modid}_lnd.nc
    wtr_lcperc_fname=${lc1dir}/modis_${landcover_varname}_${modid}_wtr.nc
    ice_lcperc_fname=${lc1dir}/modis_${landcover_varname}_${modid}_ice.nc


    # Create the MODIS-tile derived nc files if they don't already exist
    # if [[ ! -f ${lc_fname}2 ]]; then
    if [[ ! -f ${lc_fname}  ||  "$overwrite" == TRUE ]] ; then
      echo "  Generating ${lc_fname}"

      mod_fn=$(ls ${modis_dir}/MCD12Q1.*.${modid}.*.hdf)
      echo "    Found modis_tile file: ${mod_fn}"

      hdf_fieldname=$(gdalinfo $mod_fn | grep $landcover_varname | grep NAME | grep -Eo 'HDF4_EOS:.*')
      # echo "hdf_fieldname: $hdf_fieldname"

      gtrans_cmd="gdal_translate -of Byte -of netCDF -co "COMPRESS=DEFLATE" ${hdf_fieldname} ${lc_fname}"
      cmd_stdout=$( ${gtrans_cmd} 2> ${stderr_fn} )

      # Ensure that the word "done" is in stdout from the gdal_translate command
      if [[ ${cmd_stdout} != *done* ]]; then
        echo "Error running gdal_translate!"
        echo " "
        echo "  command was:\n  ${gtrans_cmd}"
        echo " "
        echo "  stdout was: ${cmd_stdout}"
        echo " "
        echo "  stderr was: $(cat ${stderr_fn})"
        echo " "
      else
        echo "    Created landcover_type1 nc file:    ${lc_fname}"
      fi

      # With the lc file, create files for lnd, wtr, ice with values
      #   that range from 0-100 (plus oob)
      ncap2 -4 -L 1 -O -v -S ${is_land_ncap_input} ${lc_fname} ${lnd_lcperc_fname}
      echo "      Created percentage-land nc file:    ${lnd_lcperc_fname}"

      ncap2 -4 -L 1 -O -v -S ${is_water_ncap_input} ${lc_fname} ${wtr_lcperc_fname}
      echo "      Created percentage-water nc file:   ${wtr_lcperc_fname}"

      ncap2 -4 -L 1 -O -v -S ${is_ice_ncap_input} ${lc_fname} ${ice_lcperc_fname}
      echo "      Created percentage-ice nc file:     ${ice_lcperc_fname}"

	    echo "      Finished creating .nc files for: ${modid}"
      echo " "
    else
      echo "  Skipping ${modid} because .nc files exist"
    fi

    echo "Finished with modid: ${modid}"
  done

done

# Clean up by removing temp file(s)
rm -v ${stderr_fn}

echo "Finished at: $(date)"
