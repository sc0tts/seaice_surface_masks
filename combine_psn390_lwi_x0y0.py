"""
combine_psn390_lwi_x0y0.py

Combine the left and right x0y0 lwi grids into one

Usage:
    python combine_psn390_lwi_x0y0.py \
            ./lwi_psn/psn390_x0y0_left_lwi.dat \
            ./lwi_psn/psn390_x0y0_right_lwi.dat \
            ./lwi_psn/psn390_x0y0_lwi.dat \
            9856 \
            14976
"""

import sys
import numpy as np

# Yes, there's so many ways to error check this....
fn1 = sys.argv[1]
fn2 = sys.argv[2]
ofn = sys.argv[3]
xdim = int(sys.argv[4])
ydim = int(sys.argv[5])

data1 = np.fromfile(fn1, dtype=np.uint8).reshape(ydim, xdim)
data2 = np.fromfile(fn2, dtype=np.uint8).reshape(ydim, xdim)

in_both = (data1 != 255) & (data2 != 255)
n_in_both = np.sum(np.where(in_both, 1, 0))
if n_in_both != 0:
    print(f'Number of pixels with data in both file: {n_in_both}')
    print('That is unexpected...')

data1[data2 != 255] = data2[data2 != 255]

data1.tofile(ofn)
print(f'Wrote: {ofn}  ({xdim}, {ydim})')
