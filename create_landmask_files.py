"""
create_landmasks_files.py

Use the loili file from ./loili_<projid>/
to generate land mask files for various resolutions

lwil/loili/loilid encoding:
   50: Ocean
   80: Disconnected Ocean (only in loilid)
  150: Land
  175: Lake
  200: Ice, including almost --but not all! -- of Antarctica
  220: Ice shelf (added by this code for loili (not in lwil) )
  250: Off-earth

This encoding adds:
    80: Disconnected-ocean; majority-water/ocean but not orthogonally-
          connected to the global ocean
"""

import os
import sys
import numpy as np


val = {
    'ocean': 50,
    'discon': 80,
    'land': 150,
    'lake': 175,
    'ice': 200,
    'shelf': 220,
    'offearth': 250,
}


def xwm(m='exiting xwm()'):
    raise SystemExit(m)


def get_dims(gridid):
    if gridid == 'psn25':
        xdim = 304
        ydim = 448
        res = 25000
    elif gridid == 'psn12.5':
        xdim = 608
        ydim = 896
        res = 12500
    elif gridid == 'psn6.25':
        xdim = 1216
        ydim = 1792
        res = 6250
    elif gridid == 'psn3.125':
        xdim = 2432
        ydim = 3584
        res = 3125
    elif gridid == 'psn390':
        xdim = 19456
        ydim = 28672
        res = 390.625
    elif gridid == 'pss25':
        xdim = 316
        ydim = 332
        res = 25000
    elif gridid == 'pss12.5':
        xdim = 632
        ydim = 664
        res = 12500
    elif gridid == 'pss6.25':
        xdim = 1264
        ydim = 1328
        res = 6250
    elif gridid == 'pss3.125':
        xdim = 2528
        ydim = 2656
        res = 3125
    elif gridid == 'pss390':
        xdim = 20224
        ydim = 21248
        res = 390.625
    elif 'e2' in gridid:
        if '390' in gridid:
            xdim = 46080
            ydim = 46080
            res = 390.625
        elif '3.125' in gridid:
            xdim = 5760
            ydim = 5760
            res = 3125
        elif '6.25' in gridid:
            xdim = 2880
            ydim = 2880
            res = 6250
        elif '12.5' in gridid:
            xdim = 1440
            ydim = 1440
            res = 12500
        elif '25' in gridid:
            xdim = 720
            ydim = 720
            res = 25000
    else:
        xwm(f'Could not get dims for: {gridid}')

    return xdim, ydim, res


def get_loili390(gridid,
                 fn_loili_390_='./loili_{projid}//{projid}390_loili.dat'):

    # Create or read the loili390 mask
    projid = gridid[:3]
    fn_loili390 = fn_loili_390_.format(projid=projid)

    xdim390, ydim390, res390 = get_dims(f'{projid}390')

    print(f'Reading: {fn_loili390}', flush=True)
    loili390 = np.fromfile(fn_loili390, dtype=np.uint8).reshape(
        ydim390, xdim390)

    return loili390


def get_ocean_indices(gridid):
    # For a given gridid, return i,j pairs where is global ocean

    if 'psn' in gridid:
        yield 0, 0  # Upper left corner
        if gridid == 'psn25':
            yield 202, 0    # Sea of Bohai
        elif gridid == 'psn12.5':
            yield 404, 0  # Sea of Bohai
        elif gridid == 'psn6.25':
            yield 808, 0  # Sea of Bohai
        elif gridid == 'psn3.125':
            yield 1616, 0  # Sea of Bohai
    elif 'pss' in gridid:
        yield 0, 0  # Upper left corner
    elif 'e2n25' in gridid:
        yield 360, 10
        yield 430, 580  # Mediterranean Sea
    elif 'e2n12.5' in gridid:
        yield 720, 10
    elif 'e2n6.25' in gridid:
        yield 1440, 10
    elif 'e2n3.125' in gridid:
        yield 2880, 10
    elif 'e2s25' in gridid:
        yield 360, 10
    elif 'e2s12.5' in gridid:
        yield 720, 10
    elif 'e2s6.25' in gridid:
        yield 1440, 10
    elif 'e2s3.125' in gridid:
        yield 2880, 10
    else:
        print(f'No ocean indices for: {gridid}')


def find_discon_ocean(data, gridid, oceanval=50, disconval=80):
    # Find where oceanvals are not connected to other oceanvals
    from scipy.ndimage import label

    is_ocean = data == oceanval
    ocean_regions, n_ocean_regions = label(is_ocean)

    is_discon_ocean = is_ocean
    for i_ocean, j_ocean in get_ocean_indices(gridid):
        is_discon_ocean[ocean_regions == ocean_regions[j_ocean, i_ocean]] = False

    data[is_discon_ocean] = disconval

    return data


def create_landmask_from_loili(gridid, loili390):
    # Combine the loili grid cells
    # then find disconnected ocean
    projid = gridid[:3]
    xdim390, ydim390, res390 = get_dims(f'{projid}390')
    xdim, ydim, res = get_dims(gridid)

    # Values are ocean, land, lake, ice, iceshelf
    n = {}
    for key in val.keys():
        n[key] = np.zeros((ydim, xdim), dtype=np.int16)

    factor = int(res // res390)
    print(f'  For {gridid}, factor: {factor}')

    for joff in range(factor):
        if joff % 5 == 0:
            print(f'joff is {joff} of {factor - 1}')
        for ioff in range(factor):
            subset = loili390[joff::factor, ioff::factor]
            for key in val.keys():
                has_value = subset == val[key]
                n[key][has_value] += 1
    """ For debugging
    for key in val.keys():
        ofn = f'n_{key}.dat'
        n[key].tofile(ofn)
        print(f'  Wrote: {ofn}', flush=True)
    """

    loilid = np.zeros((ydim, xdim), dtype=np.uint8)
    loilid[:] = 255  # Initialize all to missing

    # Logic is:
    # Water = Lake + Ocean  <-- wins tiebreaker
    # Solid = Land + Ice + Shelf
    # Water wins tiebreaker over Solid
    # Ocean wins tiebreaker over Lake
    # Shelf wins tiebreaker over ice or land
    # Ice wins tiebreaker over land

    n_water = n['ocean'] + n['lake']
    n_solid = n['land'] + n['ice'] + n['shelf']

    is_water = (n_water >= n_solid) & (n_water > 0)
    is_solid = (~is_water) & (n_solid > 0)

    is_ocean = is_water & (n['ocean'] >= n['lake'])
    is_lake = is_water & (~is_ocean)

    is_ice = is_solid & (n['ice'] >= (n['land'] + n['shelf']))
    is_shelf = is_solid & (n['shelf'] >= (n['land'] + n['ice']))
    is_land = is_solid & (~is_ice) & (~is_shelf)

    loilid[is_ocean] = val['ocean']
    loilid[is_lake] = val['lake']

    loilid[is_land] = val['land']
    loilid[is_ice] = val['ice']
    loilid[is_shelf] = val['shelf']

    # Add off-earth value
    is_offearth = (loilid == 255) & (n['offearth'] > 0)
    loilid[is_offearth] = val['offearth']

    # Check to ensure that all locations have values
    where_unassigned = np.where(loilid == 255)
    n_unassigned = len(where_unassigned[0])
    if n_unassigned > 0:
        print(f'n_unassigned: {n_unassigned}')
        xwm(f'Should not have unassigned vals: {n_unassigned}')

    loilid = find_discon_ocean(
        loilid, gridid, oceanval=val['ocean'], disconval=val['discon'])

    ofn = f'{gridid}_loilid.dat'
    loilid.tofile(ofn)
    print(f'Wrote: {ofn}  {loilid.dtype}  {loilid.shape}', flush=True)
    print(f'Unique values of loilid: {np.unique(loilid)}')


if __name__ == '__main__':
    all_gridids = (
        'psn25', 'psn12.5', 'psn6.25', 'psn3.125',
        'pss25', 'pss12.5', 'pss6.25', 'pss3.125',
        'e2n25', 'e2n12.5', 'e2n6.25', 'e2n3.125',
        'e2s25', 'e2s12.5', 'e2s6.25', 'e2s3.125',)

    try:
        gridid = sys.argv[1]
        assert gridid in all_gridids
        gridids = [gridid,]
    except IndexError:
        gridids = all_gridids
        print(f'Running for all pss grids: {gridids}')
    except AssertionError:
        xwm(f'gridid {gridid} not recognized as one of {all_gridids}')

    for gridid in gridids:
        loili390 = get_loili390(gridid)
        create_landmask_from_loili(gridid, loili390)
