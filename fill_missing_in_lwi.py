"""
fill_missing_in_lwi.py

Fill in missing data with plurality of orthogonally adjacent pixels

Output directory is assumed to be:  ./lwi_filled_{projid} and is
calculated with dirname.replace('lwi_', 'lwi_filled_')

Usage:
    python fill_missing_in_lwi.py <lwi_fn> <xdim> <ydim> [<out_dir>]
  eg
    python fill_missing_in_lwi.py ./lwi_psn/psn390_x0y0_lwi.dat 9856 14976

Output:
  eg
    ./lwi_filled_psn/psn390_x0y0_lwi.dat
"""

import os
import sys
import numpy as np
from scipy.ndimage import label, shift


def xwm(m='exiting in xwm()'):
    raise SystemExit(m)


def fill_missing(data, tiebreakers=False):
    # Fill in missing data with plurality of surrounding points
    # Note: this works well for scattered points, but is slow for
    # the block of missing data near the poles of most hi-res
    # reprojected grids.  But...it works well enough and only has
    # to be run once
    """ np.roll() method
    left = np.roll(data, (0, -1))
    right = np.roll(data, (0, 1))
    up = np.roll(data, (-1, 0))
    down = np.roll(data, (1, 0))
    """
    left = shift(data, (0, -1), order=0, mode='nearest')
    right = shift(data, (0, 1), order=0, mode='nearest')
    up = shift(data, (-1, 0), order=0, mode='nearest')
    down = shift(data, (1, 0), order=0, mode='nearest')

    near_n_lnd = np.zeros((ydim, xdim), dtype=np.int16)
    near_n_wtr = np.zeros((ydim, xdim), dtype=np.int16)
    near_n_ice = np.zeros((ydim, xdim), dtype=np.int16)

    near_n_lnd[left == 150] += 1
    near_n_wtr[left == 50] += 1
    near_n_ice[left == 200] += 1

    near_n_lnd[right == 150] += 1
    near_n_wtr[right == 50] += 1
    near_n_ice[right == 200] += 1

    near_n_lnd[up == 150] += 1
    near_n_wtr[up == 50] += 1
    near_n_ice[up == 200] += 1

    near_n_lnd[down == 150] += 1
    near_n_wtr[down == 50] += 1
    near_n_ice[down == 200] += 1

    if not tiebreakers:
        # Use plurality to determine lnd/wtr/ice
        is_lnd = ((near_n_lnd > (near_n_wtr + near_n_ice)) & (data == 255))
        is_wtr = ((near_n_wtr > (near_n_lnd + near_n_ice)) & (data == 255))
        is_ice = ((near_n_ice > (near_n_lnd + near_n_wtr)) & (data == 255))
    else:
        # Make a decision...not just plurality
        # This occurs when equal number of, say land and ice or land and water
        # Because wtr is set after ice which is set after land, the order
        # of precedence is wtr > ice > lnd
        # Note: this only seems to occur in psn390_x0y0
        is_lnd = (data == 255) & (near_n_lnd >= 2)
        is_ice = (data == 255) & (near_n_ice >= 2)
        is_wtr = (data == 255) & (near_n_wtr >= 2)

    """
    where_missing = np.where(data == 255)
    for i, j in zip(where_missing[1], where_missing[0]):
        print(f'({i:5d}, {j:5d}): d {data[j, i]:3d}  l {left[j, i]:3d}  r{right[j, i]:3d}  u {up[j, i]:3d}  d {down[j, i]:3d}  nl {near_n_lnd[j, i]:1d}  nw {near_n_wtr[j, i]:1d}  ni {near_n_ice[j, i]:1d}  isl {str(is_lnd[j, i]):5s}  isw {str(is_wtr[j, i]):5s}  isi {str(is_ice[j, i]):5s}')
    """

    data[is_lnd] = 150
    data[is_wtr] = 50
    data[is_ice] = 200

    return data


def read_from_lwi_file(ifn, xdim, ydim):
    # Read LWI data
    data = np.fromfile(ifn, dtype=np.uint8).reshape(ydim, xdim)
    print(f'Read data from: {ifn}', flush=True)

    return data


def wrap_fill_call(data):
    # So that this could be called from other than main()

    last_n_missing = -1
    n_missing = np.sum(np.where(data == 255, 1, 0))
    while (n_missing != last_n_missing) and (n_missing > 0):
        data = fill_missing(data, tiebreakers=False)
        last_n_missing = n_missing
        n_missing = np.sum(np.where(data == 255, 1, 0))
        print(f'After filling, n_missing: {n_missing}', flush=True)
    
    if n_missing > 0:
        print(f'  Still {n_missing} unassigned pixels:')
        data = fill_missing(data, tiebreakers=True)
        n_missing = np.sum(np.where(data == 255, 1, 0))
        if n_missing > 0:
            where_missing = np.where(data == 255)
            for i, j in zip(where_missing[1], where_missing[0]):
                print(f'    Missing: ({i:5d}, {j:5d})')
        else:
            print(f'Filled those values using tiebreaker rules')
    else:
        print(f'  All missing data filled with adjacent values')

    return data


def determine_missing_vs_oob(ifn, data):
    # Change off-earth "missing" values from 255 to 250
    if 'psn' in ifn or 'pss' in ifn:
        # There are no off-grid pixels in the polar stereo grids
        return data

    ydim, xdim = data.shape

    tiles_with_nw_oob = ('x0y0', 'x1y0', 'x0y1') 
    tiles_with_ne_oob = ('x2y0', 'x3y0', 'x3y1')
    tiles_with_sw_oob = ('x0y2', 'x0y3', 'x1y3')
    tiles_with_se_oob = ('x3y2', 'x2y3', 'x3y3')

    oob_index = None
    ifn_parts = os.path.basename(ifn).split('_')
    for part in ifn_parts:
        print(f'{ifn}: {part}')
        if part in tiles_with_nw_oob:
            oob_index = [0, 0]
        elif part in tiles_with_ne_oob:
            oob_index = [0, xdim - 1]
        elif part in tiles_with_sw_oob:
            oob_index = [ydim - 1, 0]
        elif part in tiles_with_se_oob:
            oob_index = [ydim - 1, xdim - 1]

    if oob_index is not None:
        is_missing = data == 255
        missing_regions, n_regions = label(is_missing)

        # if only one missing region, all the missing values are oob
        if n_regions == 1:
            data[data == 255] = 250
            print('All missing data were off-earth')
        else:
            print(f'number of missing regions: {n_regions}')
            j_oob, i_oob = oob_index
            oob_region = missing_regions[j_oob, i_oob]
            print(f'oob_region: {oob_region}')
            data[missing_regions == oob_region] = 250

    return data


if __name__ == '__main__':
    # Yes, there's so many ways to error check this....

    ifn = sys.argv[1]
    ofn = ifn.replace('lwi_', 'lwi_filled_')
    try:
        assert ifn != ofn
        os.makedirs(os.path.dirname(ofn), exist_ok=True)
    except AssertionError:
        raise SystemExit(f'Could not generate differing output filename: {ifn}')

    xdim = int(sys.argv[2])
    ydim = int(sys.argv[3])

    data = read_from_lwi_file(ifn, xdim, ydim)
    data = determine_missing_vs_oob(ifn, data)
    data = wrap_fill_call(data)
    data.tofile(ofn)
    print(f'Wrote: {ofn}')

