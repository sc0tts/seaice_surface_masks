#!/bin/bash

# find_unique_vals_in_tiles.sh

# Determine whether LWI tiles have missing values (255) or not


for fn in lwi_filled*/*_lwi.dat ; do
  echo $fn
  unique_bytes.py $fn
  echo " "
done

<<OUTPUT

lwi_e2n/e2n390_x0y0_lwi.dat
Unique values in: lwi_e2n/e2n390_x0y0_lwi.dat
[ 50 255]
 
lwi_e2n/e2n390_x0y1_lwi.dat
Unique values in: lwi_e2n/e2n390_x0y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x0y2_lwi.dat
Unique values in: lwi_e2n/e2n390_x0y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x0y3_lwi.dat
Unique values in: lwi_e2n/e2n390_x0y3_lwi.dat
[ 50 150 255]
 
lwi_e2n/e2n390_x1y0_lwi.dat
Unique values in: lwi_e2n/e2n390_x1y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x1y1_lwi.dat
Unique values in: lwi_e2n/e2n390_x1y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x1y2_lwi.dat
Unique values in: lwi_e2n/e2n390_x1y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x1y3_lwi.dat
Unique values in: lwi_e2n/e2n390_x1y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x2y0_lwi.dat
Unique values in: lwi_e2n/e2n390_x2y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x2y1_lwi.dat
Unique values in: lwi_e2n/e2n390_x2y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x2y2_lwi.dat
Unique values in: lwi_e2n/e2n390_x2y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x2y3_lwi.dat
Unique values in: lwi_e2n/e2n390_x2y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x3y0_lwi.dat
Unique values in: lwi_e2n/e2n390_x3y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x3y1_lwi.dat
Unique values in: lwi_e2n/e2n390_x3y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x3y2_lwi.dat
Unique values in: lwi_e2n/e2n390_x3y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2n/e2n390_x3y3_lwi.dat
Unique values in: lwi_e2n/e2n390_x3y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x0y0_lwi.dat
Unique values in: lwi_e2s/e2s390_x0y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x0y1_lwi.dat
Unique values in: lwi_e2s/e2s390_x0y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x0y2_lwi.dat
Unique values in: lwi_e2s/e2s390_x0y2_lwi.dat
[ 50 150 255]
 
lwi_e2s/e2s390_x0y3_lwi.dat
Unique values in: lwi_e2s/e2s390_x0y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x1y0_lwi.dat
Unique values in: lwi_e2s/e2s390_x1y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x1y1_lwi.dat
Unique values in: lwi_e2s/e2s390_x1y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x1y2_lwi.dat
Unique values in: lwi_e2s/e2s390_x1y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x1y3_lwi.dat
Unique values in: lwi_e2s/e2s390_x1y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x2y0_lwi.dat
Unique values in: lwi_e2s/e2s390_x2y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x2y1_lwi.dat
Unique values in: lwi_e2s/e2s390_x2y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x2y2_lwi.dat
Unique values in: lwi_e2s/e2s390_x2y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x2y3_lwi.dat
Unique values in: lwi_e2s/e2s390_x2y3_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x3y0_lwi.dat
Unique values in: lwi_e2s/e2s390_x3y0_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x3y1_lwi.dat
Unique values in: lwi_e2s/e2s390_x3y1_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x3y2_lwi.dat
Unique values in: lwi_e2s/e2s390_x3y2_lwi.dat
[ 50 150 200 255]
 
lwi_e2s/e2s390_x3y3_lwi.dat
Unique values in: lwi_e2s/e2s390_x3y3_lwi.dat
[ 50 150 200 255]
 
lwi_psn/psn390_x0y0_lwi.dat
Unique values in: lwi_psn/psn390_x0y0_lwi.dat
[ 50 150 200 255]
 
lwi_psn/psn390_x0y1_lwi.dat
Unique values in: lwi_psn/psn390_x0y1_lwi.dat
[ 50 150 200]
 
lwi_psn/psn390_x1y0_lwi.dat
Unique values in: lwi_psn/psn390_x1y0_lwi.dat
[ 50 150 200]
 
lwi_psn/psn390_x1y1_lwi.dat
Unique values in: lwi_psn/psn390_x1y1_lwi.dat
[ 50 150 200]
 
lwi_pss/pss390_x0y0_lwi.dat
Unique values in: lwi_pss/pss390_x0y0_lwi.dat
[ 50 150 200 255]
 
lwi_pss/pss390_x0y1_lwi.dat
Unique values in: lwi_pss/pss390_x0y1_lwi.dat
[ 50 150 200 255]
 
lwi_pss/pss390_x1y0_lwi.dat
Unique values in: lwi_pss/pss390_x1y0_lwi.dat
[ 50 150 200 255]
 
lwi_pss/pss390_x1y1_lwi.dat
Unique values in: lwi_pss/pss390_x1y1_lwi.dat
[ 50 150 200 255]
 
OUTPUT
