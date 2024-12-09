"""
calc_loil.py

Determine which LWI water values should be lake instead of ocean

Uses external information about known ocean pixels for each
subgrid tile to help fill all values efficiently

For reference, LWI values:
     50: ocean
    150: Land
    200: Ice (land-ice)
    250: off-Earth (e.g. corners of full EASE2 grids)

This adds:
    175: Lake

Code assumes that data files will be:
    ./lwi_filled_<projid>/<projid><res>_<tileid>_lwi.dat
  where
    projid: e2n e2s psn pss
       res: 390
    tileid: x0y0, x0y1, ..., x3y3

dims dict holds dimensions of all these subgrids
"""

import os
import numpy as np
from scipy.ndimage import label


lake_lwil_value = 175


def xwm(m='exiting in xwm()'):
    raise SystemExit(m)


subgrid_dims = {
    # These are (ydim, xdim)
    'psn390_x0y0': (14976, 9856),
    'psn390_x0y1': (13696, 9856),
    'psn390_x1y0': (14976, 9600),
    'psn390_x1y1': (13696, 9600),

    'pss390_x0y0': (11136, 10112),
    'pss390_x0y1': (10112, 10112),
    'pss390_x1y0': (11136, 10112),
    'pss390_x1y1': (10112, 10112),
}


def get_dims(projid, tileid, res):
    # Return the shape -- (ydim, xdim) -- of this subgrid tile's data
    if res != '390':
        xwm(f'Not set up for resolution other than 390: {res}')

    if projid == 'e2n' or projid == 'e2s':
        return (11520, 11520)
    else:
        try:
            fulltileid = f'{projid}{res}_{tileid}'
            return subgrid_dims[fulltileid]
        except KeyError:
            xwm(f'No dims found for: {fulltileid}')


'''
    waterregions_fn = f'{lwil_dir}/{tile_index}_waterregions.dat'
    if not os.path.isfile(waterregions_fn):
        is_water = (lwi < 100).astype(np.uint8)
        n_is_water = np.sum(np.where(is_water > 0, 1, 0))

        water_regions, n_regions = label(is_water)

        # water_regions.tofile(waterregions_fn)
        # print(f'  Wrote: {waterregions_fn} with {n_regions} regions')
    else:
        water_regions = np.fromfile(waterregions_fn, dtype=np.int32).reshape(ydim, xdim)  # noqa
        print(f'  Read in: {waterregions_fn} with {water_regions.max()} regions')  # noqa

    # Initially set to lake if water
    is_lake = water_regions > 0
    for ocean_index in is_ocean_coords[tile_index]:
        ival, jval = ocean_index
        # ocean_region_val = water_regions[ocean_index[1], ocean_index[0]]
        ocean_region_val = water_regions[jval, ival]
        is_lake[water_regions == ocean_region_val] = 0
        print(f'  Set water_region value {ocean_region_val} ({ival}, {jval}) to ocean')  # noqa

    lwi[is_lake] = lake_lwil_value
    lwi.tofile(lwil_fn)
    print(f'  Wrote: {lwil_fn}')

'''


def decode_lwi_fn(fn):
    # Assuming this LWI file is something like:
    #  ./lwi_filled_e2n/e2n390_x0y0_lwi.dat
    # Return the components
    valid_projids = ('e2n', 'e2s', 'psn', 'pss')
    valid_ress = ('390',)
    valid_tileids = ('x0y0', 'x0y1', 'x0y2', 'x0y3',
                     'x1y0', 'x1y1', 'x1y2', 'x1y3',
                     'x2y0', 'x2y1', 'x2y2', 'x2y3',
                     'x3y0', 'x3y1', 'x3y2', 'x3y3',)

    bfn = os.path.basename(fn)
    parts = bfn.split('_')

    projid = parts[0][:3]
    res = parts[0][3:]

    tileid = parts[1]

    assert parts[2] == 'lwi.dat'
    assert projid in valid_projids
    assert res in valid_ress
    assert tileid in valid_tileids

    return projid, res, tileid


def yield_ocean_indices(projid, res, tileid):
    # Iterator yields ocean indices based on subgrid id

    if projid is None:
        xwm('This is just a placeholder in yield_ocean_indices()')

    # Derived from find_lakes_psn390.py
    elif projid == 'psn' and res == '390' and tileid == 'x0y0':
        yield 50, 50
        yield 553, 14975
        yield 556, 14975
        yield 580, 14975
        yield 680, 14975
        yield 702, 14975
        yield 710, 14975
        yield 987, 14975
        yield 3854, 14975
        yield 3874, 14975
        yield 3880, 14975
        yield 3886, 14975
        yield 3890, 14975
    elif projid == 'psn' and res == '390' and tileid == 'x0y1':
        yield 9700, 50
        yield 50, 50
        yield 290, 0
        yield 327, 0
        yield 336, 0
        # yield 555, 0
        yield 3857, 0
        yield 3862, 0
        yield 3867, 0
        yield 3898, 0
        yield 4033, 0
        yield 4028, 0
        yield 9855, 1915
        # yield 9855, 1917
        yield 9855, 1920
        yield 9855, 2167
    elif projid == 'psn' and res == '390' and tileid == 'x1y0':
        yield 50, 50
        yield 50, 14800
        yield 3000, 50
    elif projid == 'psn' and res == '390' and tileid == 'x1y1':
        yield 50, 50
        yield 6340, 0
        yield 0, 1980
        yield 0, 2010
        yield 0, 2150
        yield 0, 2290
        yield 0, 8370
        yield 0, 8394
        yield 0, 8455

    # Derived from find_lakes_pss390.py
    elif projid == 'pss' and res == '390' and tileid == 'x0y0':
        yield 9700, 50
    elif projid == 'pss' and res == '390' and tileid == 'x0y1':
        yield 9700, 10050
    elif projid == 'pss' and res == '390' and tileid == 'x1y0':
        yield 50, 50
    elif projid == 'pss' and res == '390' and tileid == 'x1y1':
        yield 50, 10050

    # These are hand-derived because no prior version of e2n390 subgrids
    elif projid == 'e2n' and res == '390' and tileid == 'x0y0':
        yield 11500, 11500
    elif projid == 'e2n' and res == '390' and tileid == 'x0y1':
        yield 11500, 50
        yield 6000, 11500
        yield 6572, 11519
    elif projid == 'e2n' and res == '390' and tileid == 'x0y2':
        yield 11500, 11500
        yield 50, 50
    elif projid == 'e2n' and res == '390' and tileid == 'x0y3':
        yield 11500, 50

    elif projid == 'e2n' and res == '390' and tileid == 'x1y0':
        yield 11500, 11500
    elif projid == 'e2n' and res == '390' and tileid == 'x1y1':
        yield 11500, 50
        yield 3000, 11500
        yield 4115, 11519
        yield 4670, 11519
        yield 5581, 11519
        yield 7540, 11519
        yield 8228, 11519
        yield 8240, 11519
        yield 8270, 11519
    elif projid == 'e2n' and res == '390' and tileid == 'x1y2':
        yield 11500, 50
        yield 4131, 0
        yield 5500, 0
        yield 5416, 0
        yield 5475, 0
        yield 5508, 0
        yield 6280, 0
        yield 6300, 0
        yield 6382, 0
        yield 6385, 0
        yield 6405, 0
        yield 6390, 0
        yield 9020, 0
        yield 9120, 0
        yield 9130, 0
        yield 0, 5000
        yield 11519, 10220
    elif projid == 'e2n' and res == '390' and tileid == 'x1y3':
        yield 50, 50
        yield 10620, 0
        yield 10626, 0
        yield 10655, 0
        yield 10726, 0
        yield 10740, 0
        yield 10800, 0
        yield 11000, 0
        yield 11519, 2400

    elif projid == 'e2n' and res == '390' and tileid == 'x2y0':
        yield 50, 11500
    elif projid == 'e2n' and res == '390' and tileid == 'x2y1':
        yield 50, 50
        yield 50, 11500
        yield 4126, 11519
        yield 4130, 11519
        yield 10000, 50
        yield 11519, 3307
        yield 11519, 3311
        yield 11519, 3313
        yield 11519, 3450
        yield 11519, 4362
    elif projid == 'e2n' and res == '390' and tileid == 'x2y2':
        yield 50, 50
        yield 6500, 11500
    elif projid == 'e2n' and res == '390' and tileid == 'x2y3':
        yield 50, 11500    # South Atlantic
        yield 50, 2900     # Mediterranean
        yield 11500, 3000  # Persian Gulf

    elif projid == 'e2n' and res == '390' and tileid == 'x3y0':
        yield 50, 11500
        yield 6129, 11519
    elif projid == 'e2n' and res == '390' and tileid == 'x3y1':
        yield 50, 50
        yield 5307, 0
        yield 6125, 0
        yield 6125, 0
        yield 6666, 0
        yield 6690, 0
        yield 6730, 0
        yield 6760, 0
        yield 6775, 0
        yield 6780, 0
        yield 6625, 11519
        yield 6730, 11519
    elif projid == 'e2n' and res == '390' and tileid == 'x3y2':
        yield 11500, 50
        yield 6340, 0
    elif projid == 'e2n' and res == '390' and tileid == 'x3y3':
        yield 8000, 50

    # These are hand-derived because no prior version of e22390 subgrids
    elif projid == 'e2s' and res == '390' and tileid == 'x0y0':
        yield 11500, 11500
        yield 3816, 11519
        yield 5185, 8438  # Amazon crossing equator
        yield 5184, 8439  # Amazon crossing equator
        yield 5183, 8440  # Amazon crossing equator
        yield 5182, 8442  # Amazon crossing equator
        yield 5178, 8447  # Amazon crossing equator
        yield 5167, 8459  # Amazon crossing equator
        yield 5130, 8505  # Amazon crossing equator
        yield 5129, 8507  # Amazon crossing equator
        yield 5127, 8509  # Amazon crossing equator
    elif projid == 'e2s' and res == '390' and tileid == 'x0y1':
        yield 11500, 50
        yield 11500, 11500
        yield 3810, 0
        yield 3820, 0
        yield 3905, 0
        yield 9935, 0
        yield 9957, 0
        yield 9965, 0
    elif projid == 'e2s' and res == '390' and tileid == 'x0y2':
        yield 11500, 11500
    elif projid == 'e2s' and res == '390' and tileid == 'x0y3':
        yield 11500, 50

    elif projid == 'e2s' and res == '390' and tileid == 'x1y0':
        yield 11500, 11500
    elif projid == 'e2s' and res == '390' and tileid == 'x1y1':
        yield 11500, 50
        yield 0, 8226
    elif projid == 'e2s' and res == '390' and tileid == 'x1y2':
        yield 50, 50
    elif projid == 'e2s' and res == '390' and tileid == 'x1y3':
        yield 50, 50

    elif projid == 'e2s' and res == '390' and tileid == 'x2y0':
        yield 50, 11500
    elif projid == 'e2s' and res == '390' and tileid == 'x2y1':
        yield 50, 50
    elif projid == 'e2s' and res == '390' and tileid == 'x2y2':
        yield 11500, 50
    elif projid == 'e2s' and res == '390' and tileid == 'x2y3':
        yield 50, 50
        yield 10440, 0

    elif projid == 'e2s' and res == '390' and tileid == 'x3y0':
        yield 50, 11500
    elif projid == 'e2s' and res == '390' and tileid == 'x3y1':
        yield 50, 50
    elif projid == 'e2s' and res == '390' and tileid == 'x3y2':
        yield 50, 50
        yield 5938, 11519
        yield 5950, 11519
        yield 8300, 11519
    elif projid == 'e2s' and res == '390' and tileid == 'x3y3':
        yield 50, 8000
        yield 7800, 10
    else:
        xwm(f'yield_ocean_indices failed for {projid} {res} {tileid}')


def add_lake_values(data, projid, res, tileid, dims):
    # Determine where lake should replace ocean
    # Lake value: 175
    is_water = data == 50
    water_regions, n_water_regions = label(is_water)

    # Default to setting all water to lake, then add back ocean values
    data[is_water] = 175

    # while i_ocean, j_ocean in yield_ocean_indices():

    for i_ocean, j_ocean in yield_ocean_indices(projid, res, tileid):
        ocean_index = water_regions[j_ocean, i_ocean]
        print(f'Setting water region index {ocean_index} back to ocean')
        try:
            assert ocean_index != 0
        except AssertionError:
            print(f'ocean index: ({i_ocean}, {j_ocean})')
            print(f'water_regions at ocean_index: {water_regions[j_ocean, i_ocean]}')  # noqa
            xwm(f'ocean index does not appear to be water: {projid} {res} {tileid}')  # noqa
        data[water_regions == ocean_index] = 50

    return data


def calc_loil(ifn, overwrite=False):
    # Calculate LOIL from this LWI file
    ofn = ifn.replace('lwi', 'loil')
    if not overwrite and os.path.isfile(ofn):
        print(f'Skipping because ofn exists: {ofn}')
        return

    projid, res, tileid = decode_lwi_fn(ifn)
    dims = get_dims(projid, tileid, res)
    print(f'{projid} {res} {tileid} {dims} from {ifn}')

    data = np.fromfile(ifn, dtype=np.uint8).reshape(dims)

    # This was just a quick check of the loop, and verifying
    # that the fill_missing routine worked
    # assert np.all(data != 255)
    data = add_lake_values(data, projid, res, tileid, dims)

    ofn = ifn.replace('lwi', 'loil')
    os.makedirs(os.path.dirname(ofn), exist_ok=True)
    data.tofile(ofn)
    print(f'Wrote: {ofn}')
    print('')


if __name__ == '__main__':
    import glob
    import sys

    try:
        projid = sys.argv[1]
        fn_list = \
            fn_list = sorted(glob.glob(f'./lwi_filled_{projid}/{projid}390_x?y?_lwi.dat'))  # noqa
    except IndexError:
        print(f'No projid provided, looking for all matching files')
        fn_list = sorted(glob.glob('./lwi_filled_???/???390_x?y?_lwi.dat'))

    for fn in fn_list:
        calc_loil(fn)
        # xwm(f'stopping after processing: {fn}')
