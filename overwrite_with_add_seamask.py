"""
overwrite_with_add_seamask.py

Use Antarctid Digital Database -- currently v5 -- to add ice shelves
around Antarctica.  The ADD fields is ice+land, so wherever there
is add_seamask, but BU-MODIS-derived mask has ocean, we will label
as ice shelf (value 220).

Usage:
    python overwrite_with_add_seamask.py <projid>
  eg
      python overwrite_with_add_seamask.py pss
    or
      python overwrite_with_add_seamask.py e2s
"""

import os
import numpy as np


def overwrite_full(
        projid,
        add_fn, xdim_s, ydim_s, ioff, joff,
        loil_fn, xdim_f, ydim_f,
        loili_fn,):
    outdir = os.path.dirname(loili_fn)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    print(f'Reading: {add_fn}', flush=True)
    add_data = np.fromfile(add_fn, dtype=np.uint8).reshape(
        ydim_s, xdim_s)
    print(f'Reading: {loil_fn}', flush=True)
    mask_data = np.fromfile(loil_fn, dtype=np.uint8).reshape(
        ydim_f, xdim_f)
    print(f'Read: {loil_fn}', flush=True)

    subset = mask_data[joff:joff + ydim_s, ioff:ioff + xdim_s]

    replace_loc = (add_data == 100) & (subset == 50)

    subset[replace_loc] = 220

    print(f'Writing: {loili_fn}', flush=True)
    mask_data.tofile(loili_fn)
    print(f'Wrote: {loili_fn}  {mask_data.shape}')


if __name__ == '__main__':
    import sys

    valid_projids = ('pss', 'e2s')
    try:
        projid = sys.argv[1]
        assert projid in valid_projids
    except IndexError:
        raise SystemExit(
            'Usage:\n  python overwrite_with_bmgv5.py <projid>')
    except AssertionError:
        raise SystemExit(
            f'  projid ({projid}) not in: {valid_projids}')

    if projid == 'pss':
        add_fn = \
            './add_seamask/pss390_add_seamask.dat'
        # './add_seamask/pss390_landice_mask.dat'
        xdim_s = 20224
        ydim_s = 21248
        ioff = 0
        joff = 0
        loil_fn = './loil_filled_pss/pss390_loil.dat'
        xdim_f = 20224
        ydim_f = 21248
        loili_fn = './loili_pss/pss390_loili.dat'
    elif projid == 'e2s':
        add_fn = \
            './add_seamask/e2s390_add_seamask_17920x17920_off_14080.dat'
        #    './add_seamask/add_seamask_e2s390_17920x17920_off_14080.dat'
        xdim_s = 17920
        ydim_s = 17920
        ioff = 14080
        joff = 14080
        loil_fn = './loil_filled_e2s/e2s390_loil.dat'
        xdim_f = 46080
        ydim_f = 46080
        loili_fn = './loili_e2s/e2s390_loili.dat'
    else:
        raise SystemExit(f' No BedMachine Greenland file for: {projid}')

    try:
        assert os.path.isfile(add_fn)
    except AssertionError:
        raise SystemExit(f'No such add_fn for {projid}\n  {add_fn}')

    overwrite_full(
        projid,
        add_fn, xdim_s, ydim_s, ioff, joff,
        loil_fn, xdim_f, ydim_f,
        loili_fn,)
