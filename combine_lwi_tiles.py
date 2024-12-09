"""
combine_tile_lwil_pss390.py

Combine all 5 pss390 lwil tiles into one file
"""

import os
import numpy as np

# ofn = 'pss390_all_lwil.dat'

info = {
    'psn': {
        'xdim': 19456,
        'ydim': 28672,
        'tiles': {
            'x0y0_left': {
                'xdim': 9856,
                'ydim': 14976,
                'xoff': 0,
                'yoff': 0},
            'x0y0_right': {
                'xdim': 9856,
                'ydim': 14976,
                'xoff': 0,
                'yoff': 0},
            'x1y0': {
                'xdim': 9600,
                'ydim': 14976,
                'xoff': 9856,
                'yoff': 0},
            'x0y1': {
                'xdim': 9856,
                'ydim': 13696,
                'xoff': 0,
                'yoff': 14976},
            'x1y1': {
                'xdim': 9600,
                'ydim': 13696,
                'xoff': 9856,
                'yoff': 14976}}},
    'pss': {
        'xdim': 20224,
        'ydim': 21248,
        'tiles': {
            'x0y0': {
                'xdim': 10112,
                'ydim': 11136,
                'xoff': 0,
                'yoff': 0},
            'x1y0': {
                'xdim': 10112,
                'ydim': 11136,
                'xoff': 10112,
                'yoff': 0},
            'x0y1': {
                'xdim': 10112,
                'ydim': 10112,
                'xoff': 11136,
                'yoff': 11136},
            'x1y1': {
                'xdim': 10112,
                'ydim': 10112,
                'xoff': 10112,
                'yoff': 11136}}},
    'e2n': {
        'xdim': 46080,
        'ydim': 46080,
        'tiles': {
            'x0y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 0},
            'x1y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 0},
            'x2y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 0},
            'x3y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 0},
            'x0y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 11520},
            'x1y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 11520},
            'x2y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 11520},
            'x3y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 11520},
            'x0y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 23040},
            'x1y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 23040},
            'x2y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 23040},
            'x3y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 23040},
            'x0y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 34560},
            'x1y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 34560},
            'x2y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 34560},
            'x3y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 34560}}},
    'e2s': {
        'xdim': 46080,
        'ydim': 46080,
        'tiles': {
            'x0y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 0},
            'x1y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 0},
            'x2y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 0},
            'x3y0': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 0},
            'x0y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 11520},
            'x1y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 11520},
            'x2y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 11520},
            'x3y1': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 11520},
            'x0y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 23040},
            'x1y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 23040},
            'x2y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 23040},
            'x3y2': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 23040},
            'x0y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 0,
                'yoff': 34560},
            'x1y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 11520,
                'yoff': 34560},
            'x2y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 23040,
                'yoff': 34560},
            'x3y3': {
                'xdim': 11520,
                'ydim': 11520,
                'xoff': 34560,
                'yoff': 34560}}},
}
"""
lwil = np.ones((21248, 20224), dtype=np.uint8)

dims = {
    # These are (ydim, xdim)
    'pss390_x0y0': (11136, 10112),
    'pss390_x0y1': (10112, 10112),
    'pss390_x1y0': (11136, 10112),
    'pss390_x1y1': (10112, 10112),
}

offsets = {
    # These are (yoff, ioff)
    'pss390_x0y0': (0, 0),
    'pss390_x0y1': (11136, 0),
    'pss390_x1y0': (0, 10112),
    'pss390_x1y1': (11136, 10112),
}

for pss390_tileid in (
        'pss390_x0y0', 'pss390_x0y1', 'pss390_x1y0', 'pss390_x1y1',):

    ydim, xdim = dims[pss390_tileid]
    yoff, xoff = offsets[pss390_tileid]

    ifn = f'./pss390m_lwil/{pss390_tileid}_lwil.dat'
    print(f'Reading: {ifn}', flush=True)

    lwil[yoff:yoff+ydim, xoff:xoff+xdim] = np.fromfile(ifn, dtype=np.uint8).reshape(ydim, xdim)  # noqa

lwil.tofile(ofn)
print(f'Wrote: {ofn}')

"""
def combine_lwis(projid, res=390, ifn_='./lwi_{projid}/{projid}{res}_{tileid}_lwi.dat', ofn_='./lwi_all/{projid}{res}_lwi.dat'):
    # Combine all the grids for this projid
    ofn = ofn_.format(projid=projid, res=res)
    os.makedirs(os.path.dirname(ofn), exist_ok=True)

    info_dict = info[projid]
    all_xdim = info_dict['xdim']
    all_ydim = info_dict['ydim']
    all_lwi = np.zeros((all_ydim, all_xdim), dtype=np.uint8)

    for tileid in info_dict['tiles'].keys():
        xdim = info_dict['tiles'][tileid]['xdim']
        ydim = info_dict['tiles'][tileid]['ydim']
        xoff = info_dict['tiles'][tileid]['xoff']
        yoff = info_dict['tiles'][tileid]['yoff']

        ifn = ifn_.format(projid=projid, res=res, tileid=tileid)
        if not os.path.isfile(ifn):
            xwm(f'Not a file: {ifn}')
        lwi = np.fromfile(ifn, dtype=np.uint8).reshape(ydim, xdim)
        print(f'Read lwi tile {tileid} from: {ifn}', flush=True)

        lwi_subset = all_lwi[yoff:yoff+ydim, xoff:xoff+xdim]
        not_missing = lwi != 255
        n_not_missing = np.sum(np.where(not_missing, 1, 0))
        lwi_subset[not_missing] = lwi[not_missing]
        print(f'Added {n_not_missing} values to lwi {res} grid')

        lwi = None

    all_lwi.tofile(ofn)
    print(f'Wrote: {ofn}  ({all_xdim}, {all_ydim})')

    # This causes my laptop to hang
    # n_missing = np.sum(np.where(all_lwi == 0, 1, 0))
    # print(f'   with {n_missing} unassigned pixels')


if __name__ == '__main__':
    import sys
    valid_projids = ('e2n', 'e2s', 'psn', 'pss')

    try:
        projid = sys.argv[1]
        assert projid in valid_projids
    except IndexError:
        print('No projid given')
        print('Usage:')
        print('  python combine_lwi_tiles.py <projid>')
        print('  eg')
        print('  python combine_lwi_tiles.py psn')
        print(f' where projid is one of: {valid_projids}')
        xwm('')

    combine_lwis(projid)
