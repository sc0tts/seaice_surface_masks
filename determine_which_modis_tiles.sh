#!/bin/bash

# determine_which_modis_tiles.sh

# Figure out which MODIS tiles map to which destination tile

# Usage:
#  ./determine_which_modis_tiles.sh e2n 25 |& tee out_e2n25; vi out_e2n25
#  ./determine_which_modis_tiles.sh e2s 25 |& tee out_e2s25; vi out_e2s25

# or

#  ./determine_which_modis_tiles.sh e2n 3125 |& tee out_e2n3125; vi out_e2n3125
#  ./determine_which_modis_tiles.sh e2s 3125 |& tee out_e2s3125; vi out_e2s3125

# or

#  ./determine_which_modis_tiles.sh psn 25 |& tee out_psn25; vi out_psn25
#  ./determine_which_modis_tiles.sh psn 3125 |& tee out_psn3125; vi out_psn3125

#  ./determine_which_modis_tiles.sh pss 25 |& tee out_pss25; vi out_pss25
#  ./determine_which_modis_tiles.sh pss 3125 |& tee out_pss3125; vi out_pss3125


# For sanity, use a somewhat low resolution tile -- say, 3906.25m --
# and see if a grid of pure 100s maps to the subtile, e.g. x0y1

# Because a no-value value of 255 is used, if a remapped subgrid
# is identical to a subgrid of all 255s, then the original tile
# did *not* map to that subgrid

# Get the output grid from the command line
projid="$1"
if [[ -z $projid ]]; then
  echo " "
  echo "No projid provided"
  echo "Usage:"
  echo "    ./determine_which_modis_tiles.sh <projid>"
  echo "  eg:"
  echo "    ./determine_which_modis_tiles.sh e2n"
  echo " "
  exit
else
  echo " "
  echo "Creating lists of modis tiles in each output tile for:"
  echo "  $projid"
  echo " "
fi
outdir=./modids_${projid}

# Determine which list of files to use
if [[ "$projid" == *psn* || "$projid" == *e2n* ]]; then
  modid_file_list_fn=./valid_modids_NH.txt
  v_first=0
  v_last=8
elif [[ "$projid" == *pss* || "$projid" == *e2s* ]]; then
  modid_file_list_fn=./valid_modids_SH.txt
  v_first=9
  v_last=17
else
  echo "projid not recognized: $projid"
  exit
fi

# solid_file=./uniform_fields/hundreds_2400.dat  # changing name
# modis comparison field is 2400x2400 raw binary bytes of all 100
# Note: 2,400 x 2400 = 5,760,000
modis500m_100s_fn=./uniform_fields/ub100_5760000.dat  # 2400x2400 ubytes

# modid_gpd_dir=./mod500m_gpds  # Note: this is from a bitbucket repository!
#modid_gpd_dir=./modis_gpds  # Note: only valid?
modid_gpd_dir=./modis_500m_gpds  # Note: this is from a bitbucket repository!

if [ -z $2 ] ; then
  lowres_res=25
  echo "Using default resolution: ${lowres_res}"
else
  lowres_res=$2
  echo "Using arg 2 resolution: ${lowres_res}"
fi

lowres_gridid=${projid}${lowres_res}
lowres_dir=${projid}_gpds

if [ ! -d ${outdir} ]; then
  mkdir -p ${outdir}
  echo "Created modid output directory: ${outdir}"
fi

echo "Checking for mapped-files from: ${modid_file_list_fn}"
valid_modids=`cat ${modid_file_list_fn}`
#echo ${valid_modids}


# Loop over all large tiles

if [[ "$projid" == *psn* || "$projid" == *pss* ]]; then
  max_subset_num=1
elif [[ "$projid" == *e2n* || "$projid" == *e2s* ]]; then
  max_subset_num=3
else
  echo "projid not recognized: $projid"
  exit
fi

# Replace {..} loop with explicit numbering
# for y in {0..1}; do
#   for x in {0..1}; do
y=0
while [ $y -le $max_subset_num ]; do
  x=0
  while [ $x -le $max_subset_num ]; do
    # psn_id=${gridid}_x${x}y${y}
    subgrid_id=${projid}${lowres_res}_x${x}y${y}




    # Ensure that output file doesn't overwrite existing, but does exist
    if [[ "$projid" == *psn* && "$subgrid_id" == *x0y0* ]]; then
      # Note: need a "left" and a "right" for psn x0y0 because it wraps the
      # sinusoidal left/right edges

      out_fn_left=${outdir}/${subgrid_id}_left_modids.txt
      if [ -f ${out_fn_left} ]; then
        rm ${out_fn_left}
      fi
      touch ${out_fn_left}

      out_fn_right=${outdir}/${subgrid_id}_right_modids.txt
      if [ -f ${out_fn_right} ]; then
        rm ${out_fn_right}
      fi
      touch ${out_fn_right}

      echo "Writing list of mapped tiles for ${subgrid_id} to:"
      echo "  ${out_fn_left}"
      echo "  ${out_fn_right}"

    else
      # Not psn, so just one output file
      out_fn=${outdir}/${subgrid_id}_modids.txt
      if [ -f ${out_fn} ]; then
        echo "File exists: ${out_fn}"
        echo "...but thats okay; removing instead!"
        rm -v ${out_fn}
      fi

      # Write list of tiles to outputfile, ensure its existence
      touch ${out_fn}
      echo "Writing list of mapped tiles for ${subgrid_id} to ${out_fn}"

    fi

    compare_fn=./uniform_fields/${subgrid_id}_255s.dat
    if [ ! -f $compare_fn ]; then
      echo "compare_fn does not exist: $compare_fn"
      exit
    fi

    # Loop over all valid modis tiles

    # Note: only doing files from one hemisphere,
    # because others map, but are not "on the earth" part of the projection

    # for v in {00..08}; do  
    vv=$v_first
    while [ $vv -le $v_last ]; do
      printf -v v "%02d" $vv

      # Note: can use {..} notation for h because it doesn't change
      for h in {00..35}; do
        modid=h${h}v${v}
        # echo "  modid: $modid"

        if [[ ${valid_modids} == *"${modid}"* ]]; then
          #echo "$modid is on-the-Earth"

          # Create a morphed field
          modid_gpd=${modid_gpd_dir}/sinus_${modid}_500m.gpd

          lowres_subgrid_gpd=${lowres_dir}/${subgrid_id}.gpd
          
          test_fn=is_ontile_test.dat
          
          # echo "${subgrid_id}: regridding ${modis500m_100s_fn} to ${test_fn}..."
          # regrid -w -u -i 255 ${modid_gpd} ${lowres_subgrid_gpd} ${modis500m_100s_fn} ${test_fn}

          # Remove the output file so that we're sure it came from
          # this regrid operation
          if [ -f $test_fn ]; then
            rm $test_fn
          fi

          cmd="regrid -w -u -i 255 ${modid_gpd} ${lowres_subgrid_gpd} ${modis500m_100s_fn} ${test_fn}"
          # echo "  $cmd"
          output=$($cmd)
          # echo $output

          # echo "Comparing ${test_fn} and ${compare_fn}..."
          if [ ! -f $test_fn ]; then
            echo "  Failed to write: $test_fn"
            echo "  Quitting"
            exit 1
          # else
          #   echo "  Wrote test_fn: $(ls ${test_fn})"
          fi

          if [ ! -f $compare_fn ]; then
            echo "  No comparison file: $compare_fn"
            echo "  Quitting"
            exit 1
          # else
          #   echo "  Comparing to:  ${compare_fn}"
          fi

          if [[ $(cmp ${test_fn} ${compare_fn}) != "" ]]; then
            # The regridded field does not have all missing values, so
            # it maps to this subgrid
            if [[ "$projid" == *psn* && "$subgrid_id" == *x0y0* ]]; then
              # Need to separate psn x0y0 into left and right
              if [ $h -le 17 ]; then
                echo "${modid}" >> ${out_fn_left}
                echo "${subgrid_id}: ${modid}  YES (added ${modid} to ${out_fn_left}"
              else
                echo "${modid}" >> ${out_fn_right}
                echo "${subgrid_id}: ${modid}  YES (added ${modid} to ${out_fn_right}"
              fi
            else
              # This is *not* psn x0y0
              echo "${modid}" >> ${out_fn}
              echo "${subgrid_id}: ${modid}  YES (added ${modid} to ${out_fn}"
            fi
          else
            echo "${subgrid_id}: ${modid}  NO (does not map to subgrid)"
          fi

          # Clean up by removing test file
          # rm -v ${test_fn}
          rm ${test_fn}

        else
          echo "${subgrid_id}: ${modid}  Off-Earth"
        fi

      done
      vv=$(( $vv + 1 ))

    done

  x=$(( $x + 1 ))
  done

  y=$(( $y + 1 ))
done

echo "Finished running $0"
