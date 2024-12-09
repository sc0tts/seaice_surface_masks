README_bumodis_gen.txt

Steps taken to generate land masks from MCD12Q1 tiles

1) Download the MODIS data

See the wget script in /data/mcd12q1
  mcd12q1_wget_2020.sh}

Leaves data in, eg, /data/mcd12q1/modis_granules_2020/


2) Determine which of these tiles are NH or SH

./find_modis_tile_lists.sh

Creates:
  modis_granule_list_nh.txt (NH list)
  modis_granule_list_sh.txt (SH list)


3)  Create the .nc subsets of the original .hdf files
  ./extract_lcvar_nc.sh


4) Get the .gpd files for the MODIS tiles
  These are in:
    ./modis_gpds/

  These are copied from BitBucket, though I did create a set at some point...

  Note: all the original tiles are 2400x2400 grids


5) Determine which modis tiles (h??v??) are on the earth

  python write_valid_modid_lists.py 

  Creates:
    valid_modids_NH.txt  (NH)
    valid_modids_SH.txt  (SH)

----------------------------------------------
This completes pre-processing of MODIS files
----------------------------------------------

----------------------------------------------
The following grids are to be generated
  Grids:
    psn390m
    psn3.125km
    psn6.25km
    psn12.5km
    psn25km
    
    pss390m
    pss3.125km
    pss6.25km
    pss12.5km
    pss25km

    e2n390m
    e2n3.125km
    e2n6.25km
    e2n12.5km
    e2n25km

    e2s390m
    e2s3.125km
    e2s6.25km
    e2s12.5km
    e2s25km

13) Create the  gpd files for the tiles that will be used for the output projection

  Note: NH and SH EASE2 grids are 4x4 grid, named:  x0y0 to x3y3
        NH Polar stereo grids are 2x2 grid, named x0y0 to x1y1
           except NH x0y0 grid is split into west and east,
           as x0y0left and x0y0right because of -180 to 180 boundary
        SH Polar stereo grids are 2x2 grid, named x0y0 to x1y1

  High-resolution Grids:
    e2n390m: x0y0 to x3y3   (4x4 array of subgrids)
    e2s390m: x0y0 to x3y3   (4x4 array of subgrids)
    psn390m: x0y0 to x1y1   (2x2 array of subgrids)
    pss390m: x0y0 to x1y1   (2x2 array of subgrids)

  Create the fraction-of-25km gpd files (390.625m, 3125m, 25km) :
     python gen_e2n_gpds.py  
     python gen_e2s_gpds.py  
     python gen_psn_gpds.py  
     python gen_pss_gpds.py  

  
14) Determine which modis tiles (h??v??) contribute to which SH subsets (x?y?)
  This is done by morphing all the hemisphere modids to a low resolution grid
  -- here 3.125km -- and comparing the resulting morph to an all-255 (missing)
  value of the appropriate shape.  If all the values are "missing", then the
  modid grid does not map onto that subgrid.

  Script:
    ./determine_which_modis_tiles.sh

  Usage:
    ./determine_which_modis_tiles.sh e2n          (quick, using 25km)
    ./determine_which_modis_tiles.sh e2n 3125    (slower, using 3.125km)

       creates:
         modids_e2n/e2n25_xXyY_modids.txt    where X, Y are 0, 1, 2, or 3
         modids_e2n/e2n3125_xXyY_modids.txt  where X, Y are 0, 1, 2, or 3

    ./determine_which_modis_tiles.sh e2s          (quick, using 25km)
    ./determine_which_modis_tiles.sh e2s 3125    (slower, using 3.125km)

       creates:
         modids_e2s/e2s25_xXyY_modids.txt    where X, Y are 0, 1, 2, or 3
         modids_e2s/e2s3125_xXyY_modids.txt  where X, Y are 0, 1, 2, or 3

    ./determine_which_modis_tiles.sh psn          (quick, using 25km)
    ./determine_which_modis_tiles.sh psn 3125    (slower, using 3.125km)

       creates:
         modids_psn/psn25_xXyY_modids.txt    where X, Y are 0, 1, 2, or 3
         modids_psn/psn3125_xXyY_modids.txt  where X, Y are 0, 1, 2, or 3

    ./determine_which_modis_tiles.sh pss          (quick, using 25km)
    ./determine_which_modis_tiles.sh pss 3125    (slower, using 3.125km)

       creates:
         modids_pss/pss25_xXyY_modids.txt    where X, Y are 0, 1, 2, or 3
         modids_pss/pss3125_xXyY_modids.txt  where X, Y are 0, 1, 2, or 3


15) Create data files for each subgrid with all corresponding original tiles

   combine_datfiles.py 

     python combine_datfiles.py psn |& tee out_cd_psn

     - links ./combined_fields_psn/combinedsinu_for_psn_x?y?_{lnd/wtr/ice}.dat
        - includes psn_x0y0_left and psn_x0y0_right

16) Generate lnd, wtr, ice .dat files

   convert_comb_to_390.sh psn   [takes about 30min]
   convert_comb_to_390.sh pss   [takes about 20min]
   convert_comb_to_390.sh e2n   [takes about an hour]
   convert_comb_to_390.sh e2s   [takes about an hour]

   Primary outputs are:
     - gpd files, including links with subgrid id, in combined_gpds_<projid>
     - lnd, wtr, ice subgrid files in <projid>390_fields

17) Generate LWI -- land water ice -- files at high resolution (390.625m)

   create_lwi390_files.py
     - requires gpd files and combined field files labeled with subgrid id
   
   python create_lwi
   create_lwi390_files.py psn |& tee out_lwi_psn 
     - uses:
        ./psn_gpds/psn390_{tileid}.gpd
        ./psn390_fields/psn390_{tileid}_{lnd,wtr,ice}.dat
     - creates:
        ./lwi_psn/psn390_{tileid}_lwi.dat


18) Generating the LOIL -- Land/Ocean/Ice/Lake -- from LWI

  Generate loil fields with:
    python calc_loil.py
  Then check lake/ocean connectivity in adjacent subgrids with:
    rm <just-modified loil files>
    python check_lakes_390.py

  ...And iterate until no left/right or up/down inconsistencies are reported

  When correct, these should run with only "read data for x?y?" as output:
    python check_lakes_390.py psn
    python check_lakes_390.py pss
    python check_lakes_390.py e2n
    python check_lakes_390.py e2s


19) Create full 390 masks with lakes indicated

  python combine_390_tiles.py psn
  python combine_390_tiles.py pss
  python combine_390_tiles.py e2n
  python combine_390_tiles.py e2s


20) Add in the ice shelf values
    - QGreenland in NH
      in /data/greendland_bedmachine (which is symlinked here)

        ./extract_hires_subsets.sh   to get psn390 and e2n390 versions of mask

        to generate subset and overlays...
        python overlay_bmg_on_390.py psn
        python overlay_bmg_on_390.py e2n

      then, in ~/bumodis_gen/
        python overwrite_with_bmgv5.py psn
           creates  ./loili_psn/psn390_loili.dat  (28672, 19456)

        python overwrite_with_bmgv5.py e2n
           creates ./loili_e2n/e2n390_loili.dat  (46080, 46080)

    - Apply Antarctic Digital Database (ADD) "seamask" to SH
        in ./add_seamask/
          (Ensure that v7.5 of the ADD SeaMask shapefile(s) are unzipped here)

          ./morph_add_seamask_pss.sh
            - Creates pss shapefile (epsg:3412)
            - Rasterizes this shapefile to netCDF:  add_seamask_pss390.625.nc
            - Extracts a raw binary file from .nc:  add_seamask_pss390.625.dat
            - Removes the out-of-bounds (lat > -60deg) values
            - Creates: pss390_add_seamask.dat

          ./morph_add_seamask_e2s.sh
            - Creates e2s shapefile (epsg:6932)
            - Rasterizes this shapefile to netCDF:  add_seamask_e2s390.625.nc
            - Extracts a raw binary file from .nc:  add_seamask_e2s390.625.dat
            - Removes the out-of-bounds (lat > -60deg) values
            - Creates: e2s390_add_seamask.dat


21) Create full-resolution masks from LOILI, adding disconnected-ocean 
    - Uses fields now in ./loili_???
    - adds disconnected-ocean value for majority-ocean grid cells not
      orthogonally connected to the global ocean

    python create_landmask_files.py <gridid> will do one grid (eg psn25)
    python create_landmask_files.py          will do all grids

    This writes:
        <gridid>_loilid.dat
      eg
        psn25_loilid.dat
        e2n3.125_loilid.dat


