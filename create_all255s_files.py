"""
create_all255s_files.py

Create files on the subgrids for use in comparing to regridded fields -- made
with a missing value of 255 -- to determine if any points in the original
file get used in the reprojection.

Create uniform fields of specific shapes, then set symbolic links to these
with a more general description

The EASE2 grids are the same size for NH and SH.
The polar stereo grids are different size between NH and SH

This code will set up all-255 fields for full (390.625m),
intermediate (3906.25m) and coarse (25km) resolutions
"""

import os
import numpy as np


outdir='./uniform_fields'

# ==============================================================================
# EASE2
#   All the EASE2 subgrids are the same size, for both NH and SH
#   Entire grid goes from -9,000,000 to +9,000,000
#   Subgrids are 4,500,000 x 4,500,000 each (x0y0 through x3y3)
#   25km is 180x180
#   3125m is 1440x1440
#   390.625m is 11520x11520
# ==============================================================================

# 25km
field_180x180 = np.zeros((180, 180), dtype=np.uint8)
field_180x180[:] = 255
fn = f'all255s_180x180.dat'
field_180x180.tofile(f'{outdir}/{fn}')
for y in range(4):
    for x in range(4):
        os.system(f'ln -s {fn} {outdir}/e2n25_x{x}y{y}_255s.dat')
        os.system(f'ln -s {fn} {outdir}/e2s25_x{x}y{y}_255s.dat')

# 3125m
field_1440x1440 = np.zeros((1440, 1440), dtype=np.uint8)
field_1440x1440[:] = 255
fn = f'all255s_1440x1440.dat'
field_1440x1440.tofile(f'{outdir}/{fn}')
for y in range(4):
    for x in range(4):
        os.system(f'ln -s {fn} {outdir}/e2n3125_x{x}y{y}_255s.dat')
        os.system(f'ln -s {fn} {outdir}/e2s3125_x{x}y{y}_255s.dat')

# 390.625m
field_11520x11520 = np.zeros((11520, 11520), dtype=np.uint8)
field_11520x11520[:] = 255
fn = f'all255s_11520x11520.dat'
field_11520x11520.tofile(f'{outdir}/{fn}')
for y in range(4):
    for x in range(4):
        os.system(f'ln -s {fn} {outdir}/e2n390.625_x{x}y{y}_255s.dat')
        os.system(f'ln -s {fn} {outdir}/e2s390.625_x{x}y{y}_255s.dat')

# ==============================================================================
# PSS
# -3950000 is 158 to origin (left of center)
#  3950000 is 158 to origin (right of center)
#  4350000 is 174 to origin (above center)
# -3950000 is 158 to origin (below center)
# ==============================================================================

# 25km
# Note: PSS has two of its four quadrants the same shape, and two another shape
field_158x158 = np.zeros((158, 158), dtype=np.uint8)
field_158x174 = np.zeros((174, 158), dtype=np.uint8)

field_158x158[:] = 255
field_158x174[:] = 255

fn_158x174=f'all255s_158x174.dat'
field_158x174.tofile(f'{outdir}/{fn_158x174}')
os.system(f'ln -s {fn_158x174} {outdir}/pss25_x0y0_255s.dat')
os.system(f'ln -s {fn_158x174} {outdir}/pss25_x1y0_255s.dat')

fn_158x158=f'all255s_158x158.dat'
field_158x158.tofile(f'{outdir}/{fn_158x158}')
os.system(f'ln -s {fn_158x158} {outdir}/pss25_x0y1_255s.dat')
os.system(f'ln -s {fn_158x158} {outdir}/pss25_x1y1_255s.dat')

# ------------------------------------------------------------------------------

# 3125m
# Note: PSS has two of its four quadrants the same shape, and two another shape
field_1264x1264 = np.zeros((1264, 1264), dtype=np.uint8)
field_1264x1392 = np.zeros((1392, 1264), dtype=np.uint8)

field_1264x1264[:] = 255
field_1264x1392[:] = 255

fn_1264x1392=f'all255s_1264x1392.dat'
field_1264x1392.tofile(f'{outdir}/{fn_1264x1392}')
os.system(f'ln -s {fn_1264x1392} {outdir}/pss3125_x0y0_255s.dat')
os.system(f'ln -s {fn_1264x1392} {outdir}/pss3125_x1y0_255s.dat')

fn_1264x1264='all255s_1264x1264.dat'
field_1264x1264.tofile(f'{outdir}/{fn_1264x1264}')
os.system(f'ln -s {fn_1264x1264} {outdir}/pss3125_x0y1_255s.dat')
os.system(f'ln -s {fn_1264x1264} {outdir}/pss3125_x1y1_255s.dat')

# ------------------------------------------------------------------------------

# 390.625m
# Note: PSS has two of its four quadrants the same shape, and two another shape
field_10112x10112 = np.zeros((10112, 10112), dtype=np.uint8)
field_10112x11136 = np.zeros((11136, 10112), dtype=np.uint8)

field_10112x10112[:] = 255
field_10112x11136[:] = 255

fn_10112x11136='all255s_10112x11136.dat'
field_10112x11136.tofile(f'{outdir}/{fn_10112x11136}')
os.system(f'ln -s {fn_10112x11136} {outdir}/pss390.625_x0y0_255s.dat')
os.system(f'ln -s {fn_10112x11136} {outdir}/pss390.625_x1y0_255s.dat')

fn_10112x10112='all255s_10112x10112.dat'
field_10112x10112.tofile(f'{outdir}/{fn_10112x10112}')
os.system(f'ln -s {fn_10112x10112} {outdir}/pss390.625_x0y1_255s.dat')
os.system(f'ln -s {fn_10112x10112} {outdir}/pss390.625_x1y1_255s.dat')

# ==============================================================================
# PSN
# -3850000 is 154 to origin (left of center)
#  3750000 is 150 to origin (right of center)
#  5850000 is 234 to origin (above center)
# -5350000 is 214 to origin (below center)
#
#  x0y0  x1y1
#  x0y0  x1y1
# ==============================================================================

# 25km
# Note: PSN has all four quadrants different sizes
field_154x234 = np.zeros((234, 154), dtype=np.uint8)  # for x0y0
field_150x234 = np.zeros((234, 150), dtype=np.uint8)  # for x1y0
field_154x214 = np.zeros((214, 154), dtype=np.uint8)  # for x0y1
field_150x214 = np.zeros((214, 150), dtype=np.uint8)  # for x1y1

field_154x234[:] = 255
field_150x234[:] = 255
field_154x214[:] = 255
field_150x214[:] = 255

fn = 'all255s_154x234.dat'
field_154x234.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn25_x0y0_255s.dat')

fn = 'all255s_150x234.dat'
field_150x234.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn25_x1y0_255s.dat')

fn = 'all255s_154x214.dat'
field_154x214.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn25_x0y1_255s.dat')

fn = 'all255s_150x214.dat'
field_150x214.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn25_x1y1_255s.dat')

# 3125m
# Note: PSN has all four quadrants different sizes
field_1232x1872 = np.zeros((1872, 1232), dtype=np.uint8)  # for x0y0
field_1200x1872 = np.zeros((1872, 1200), dtype=np.uint8)  # for x1y0
field_1232x1712 = np.zeros((1712, 1232), dtype=np.uint8)  # for x0y1
field_1200x1712 = np.zeros((1712, 1200), dtype=np.uint8)  # for x1y1

field_1232x1872[:] = 255
field_1200x1872[:] = 255
field_1232x1712[:] = 255
field_1200x1712[:] = 255

fn = 'all255s_1232x1872.dat'
field_1232x1872.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn3125_x0y0_255s.dat')

fn = 'all255s_1200x1872.dat'
field_1200x1872.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn3125_x1y0_255s.dat')

fn = 'all255s_1232x1712.dat'
field_1232x1712.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn3125_x0y1_255s.dat')

fn = 'all255s_1200x1712.dat'
field_1200x1712.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn3125_x1y1_255s.dat')

# 390.625m
# Note: PSN has all four quadrants different sizes
field_9856x14976 = np.zeros((14976, 9856), dtype=np.uint8)  # for x0y0
field_9600x14976 = np.zeros((14976, 9600), dtype=np.uint8)  # for x1y0
field_9856x13696 = np.zeros((13696, 9856), dtype=np.uint8)  # for x0y1
field_9600x13696 = np.zeros((13696, 9600), dtype=np.uint8)  # for x1y1

field_9856x14976[:] = 255
field_9600x14976[:] = 255
field_9856x13696[:] = 255
field_9600x13696[:] = 255

fn = 'all255s_9856x14976.dat'
field_9856x14976.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn390.625_x0y0_255s.dat')

fn = 'all255s_9600x14976.dat'
field_9600x14976.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn390.625_x1y0_255s.dat')

fn = 'all255s_9856x13696.dat'
field_9856x13696.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn390.625_x0y1_255s.dat')

fn = 'all255s_9600x13696.dat'
field_9600x13696.tofile(f'{outdir}/{fn}')
os.system(f'ln -s {fn} {outdir}/psn390.625_x1y1_255s.dat')

