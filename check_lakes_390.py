"""
check_lakes_390.py

Verify lakes aren't next to coean in adjacent tiles
"""

import numpy as np


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


def xwm(m='exiting in xwm()'):
    raise SystemExit(m)


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
            # xwm(f'No dims found for: {fulltileid}')
            return 0, 0


def verify_water_consistency(projid, n_tile, fn_):
    # Verify that lake and ocean are not adjacent on adjacent tiles
    # fn_ = './loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    for y in range(n_tile):
        for x in range(n_tile):
            tileid = f'x{x}y{y}'

            ydim, xdim = get_dims(projid, tileid, '390')

            data_center = np.fromfile(
                fn_.format(projid=projid, x=x, y=y),
                dtype=np.uint8).reshape(ydim, xdim)
            print(f'read data for {tileid}', flush=True)

            # Evaluate to the right
            try:
                tileid_right = f'x{x+1}y{y}'
                ydim2, xdim2 = get_dims(projid, tileid_right, '390')
                data_right = np.fromfile(
                    fn_.format(projid=projid, x=x+1, y=y),
                    dtype=np.uint8).reshape(ydim2, xdim2)
                print(f'read data for {tileid_right}', flush=True)
                right_of_center = data_center[:, -1]
                left_of_right = data_right[:, 0]

                is_okay = True
                bad_locs = \
                    ((right_of_center == 50) & (left_of_right == 175)) | \
                    ((right_of_center == 175) & (left_of_right == 50))
                n_mismatched = np.sum(np.where(bad_locs, 1, 0))
                if n_mismatched > 0:
                    where_bad = np.where(bad_locs)
                    print(f'left/right mismatch for {tileid}/{tileid_right}')
                    print(f'dims of {tileid}: {data_center.shape}')
                    print(f'dims of {tileid_right}: {data_below.shape}')
                    print(f'{where_bad}')
                    for i in zip(where_bad[0]):
                        print(f'{i}: b_of_c {right_of_center[i]}  t_of_l {left_of_right[i]}')
            except FileNotFoundError:
                pass

            # Evaluate below
            try:
                tileid_below = f'x{x}y{y+1}'
                ydim2, xdim2 = get_dims(projid, tileid_below, '390')
                data_below = np.fromfile(
                    fn_.format(projid=projid, x=x, y=y+1),
                    dtype=np.uint8).reshape(ydim2, xdim2)
                print(f'read data for {tileid_below}', flush=True)
                bottom_of_center = data_center[-1, :]
                top_of_lower = data_below[0, :]

                is_okay = True
                bad_locs = \
                    ((bottom_of_center == 50) & (top_of_lower == 175)) | \
                    ((bottom_of_center == 175) & (top_of_lower == 50))
                n_mismatched = np.sum(np.where(bad_locs, 1, 0))
                if n_mismatched > 0:
                    where_bad = np.where(bad_locs)
                    print(f'up/down mismatch for {tileid}/{tileid_below}')
                    print(f'dims of {tileid}: {data_center.shape}')
                    print(f'dims of {tileid_below}: {data_below.shape}')
                    print(f'{where_bad}')
                    for j in zip(where_bad[0]):
                        print(f'{j}: b_of_c {bottom_of_center[j]}  t_of_l {top_of_lower[j]}')
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    import sys

    projid = sys.argv[1]
    assert projid in ('e2n', 'e2s', 'psn', 'pss')

    if 'e2' in projid:
        n_tile = 4
    elif 'ps' in projid:
        n_tile = 2

    fn_ = './loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'

    verify_water_consistency(projid, n_tile, fn_)
