"""
overwrite_with_bmgv5.py

Use Greenland BedMachine data -- currently v5 -- to override
most of the BU-MODIS data around Greenland

Usage:
    python overwrite_with_bmgv5.py <projid>
  eg
      python overwrite_with_bmgv5.py psn
    or
      python overwrite_with_bmgv5.py e2n
"""

import os
import numpy as np


def overwrite_full(
        projid,
        bmg_fn, xdim_s, ydim_s, ioff, joff,
        loil_fn, xdim_f, ydim_f,
        loili_fn,
        dont_replace_where=10):
    outdir = os.path.dirname(loili_fn)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    print(f'Reading bmg_data from: {bmg_fn}', flush=True)
    bmg_data = np.fromfile(bmg_fn, dtype=np.uint8).reshape(
        ydim_s, xdim_s)
    print(f'Reading mask_data from: {loil_fn}', flush=True)
    mask_data = np.fromfile(loil_fn, dtype=np.uint8).reshape(
        ydim_f, xdim_f)
    print(f'Read: {loil_fn}', flush=True)

    subset = mask_data[joff:joff + ydim_s, ioff:ioff + xdim_s]

    dont_replace = bmg_data != dont_replace_where

    subset[dont_replace] = bmg_data[dont_replace]

    mask_data.tofile(loili_fn)
    print(f'Wrote: {loili_fn}  {mask_data.shape}', flush=True)


if __name__ == '__main__':
    import sys

    valid_projids = ('psn', 'e2n')
    try:
        projid = sys.argv[1]
        assert projid in valid_projids
    except IndexError:
        raise SystemExit(
            'Usage:\n  python overwrite_with_bmgv5.py <projid>')
    except AssertionError:
        raise SystemExit(
            f'  projid ({projid}) not in: {valid_projids}')

    if projid == 'psn':
        bmg_fn = \
            './greenland_bedmachine/psn390_bmgmask_v5_keep10_4032x7040.dat'
        xdim_s = 4032
        ydim_s = 7040
        ioff = 8192
        joff = 16640
        loil_fn = './loil_filled_psn/psn390_loil.dat'
        xdim_f = 19456
        ydim_f = 28672
        loili_fn = './loili_psn/psn390_loili.dat'
    elif projid == 'e2n':
        bmg_fn = \
            './greenland_bedmachine/e2n390_bmgmask_v5_keep10_5760x5248.dat'
        xdim_s = 5760
        ydim_s = 5248
        ioff = 16832
        joff = 24000
        loil_fn = './loil_filled_e2n/e2n390_loil.dat'
        xdim_f = 46080
        ydim_f = 46080
        loili_fn = './loili_e2n/e2n390_loili.dat'
    else:
        raise SystemExit(f' No BedMachine Greenland file for: {projid}')

    try:
        assert os.path.isfile(bmg_fn)
    except AssertionError:
        raise SystemExit(f'No such bmg_fn for {projid}\n  {bmg_fn}')

    overwrite_full(
        projid,
        bmg_fn, xdim_s, ydim_s, ioff, joff,
        loil_fn, xdim_f, ydim_f,
        loili_fn,)
