"""
create_lwi390_files.py

Combine tiled land, water ice files to single lwi file
For 390.625m subgrid files

Usage:
    python create_lwi390_files.py e2n |& tee out_lwi_e2n
    python create_lwi390_files.py e2s |& tee out_lwi_e2s
    python create_lwi390_files.py psn |& tee out_lwi_psn
    python create_lwi390_files.py pss |& tee out_lwi_pss
"""

import os
import numpy as np


pss390_fields_dir = './pss390m_fields'

pss390_lwi_dir = './pss390m_lwis'
os.makedirs(pss390_lwi_dir, exist_ok=True)

pss390_prefix = 'pss390'

dims = {
    # These are (ydim, xdim)
    'pss390_x0y0': (11136, 10112),
    'pss390_x0y1': (10112, 10112),
    'pss390_x1y0': (11136, 10112),
    'pss390_x1y1': (10112, 10112),
}


def xwm(m='stopping in xwm()'):
    raise SystemExit(m)



def yield_tileids(projid):
    # Yieldthe tileids for this projid
    if projid == 'psn':
        for tileid in ('x0y0_left', 'x0y0_right',
                'x1y0', 'x0y1', 'x1y1'):
            yield tileid
    elif projid == 'pss':
        for tileid in ('x0y0', 'x1y0', 'x0y1', 'x1y1'):
            yield tileid
    elif projid == 'e2n' or projid == 'e2s':
        for y in range(4):
            for x in range(4):
                yield f'x{x}y{y}'


def create_lwi(projid, tileid, xdim, ydim,
        combo_field_dir_='./{projid}390_fields',
        lwi_fn_='./lwi_{projid}/{projid}390_{tileid}_lwi.dat'):
    # Create a land-water-ice file for this subgridid
    print(f'Creating LWI for: {projid} {tileid}  ({xdim}, {ydim})',
            flush=True)

    combo_field_dir = combo_field_dir_.format(projid=projid)
    lwi_fn = lwi_fn_.format(projid=projid,tileid=tileid)
    if not os.path.isdir(os.path.dirname(lwi_fn)):
        os.makedirs(os.path.dirname(lwi_fn), exist_ok=True)

    lnd_fn = f'{combo_field_dir}/{projid}390_{tileid}_lnd.dat'
    lnd = np.fromfile(lnd_fn, dtype=np.uint8).reshape(ydim, xdim)
    print(f'  Read land values from {lnd_fn}:', flush=True)
    # print(f'Unique land values from {lnd_fn}:')
    # print(f'{np.unique(lnd)}\n', flush=True)

    wtr_fn = f'{combo_field_dir}/{projid}390_{tileid}_wtr.dat'
    wtr = np.fromfile(wtr_fn, dtype=np.uint8).reshape(ydim, xdim)
    print(f'  Read water values from {wtr_fn}:', flush=True)
    # print(f'Unique water values from {wtr_fn}:')
    # print(f'{np.unique(wtr)}\n', flush=True)

    ice_fn = f'{combo_field_dir}/{projid}390_{tileid}_ice.dat'
    ice = np.fromfile(ice_fn, dtype=np.uint8).reshape(ydim, xdim)
    print(f'  Read ice values from {ice_fn}:', flush=True)
    # print(f'Unique ice values from {ice_fn}:')
    # print(f'{np.unique(ice)}\n', flush=True)

    lwi = np.zeros((ydim, xdim), dtype=np.uint8)

    # lwi encoding:
    #   50: water
    #  150: land
    #  200: ice
    #  255: off-earth
    lwi[wtr > 100] = 50
    lwi[(lwi == 0) & (ice > lnd)] = 200
    lwi[lwi == 0] = 150

    # Add back in the oob values
    lwi[lnd == 255] = 255

    lwi.tofile(lwi_fn)
    print(f'  Wrote LWI field to: {lwi_fn}', flush=True)
    # print(f'Wrote LWI field to: {lwi_fn} with unique values:')
    # print(f'{np.unique(lwi)}\n', flush=True)

    # Zero out arrays to save memory
    lnd = None
    wtr = None
    ice = None
    lwi = None


if __name__ == '__main__':
    import sys
    valid_projids = ('psn', 'pss', 'e2n', 'e2s')
    try:
        projid = sys.argv[1]
        assert projid in valid_projids
    except IndexError:
        print('No projid given')
        print(f'Usage:\n  python {sys.argv[0]} <projid>')
        xwm(f'  where projid is one of :{valid_projids}')

    for tileid in yield_tileids(projid):
        gpd_fn = f'./{projid}_gpds/{projid}390_{tileid}.gpd'
        if not os.path.isfile(gpd_fn):
            xwm(f'No such gpd file: {gpd_fn}')

        # Find xdim and ydim
        with open(gpd_fn, 'r') as f:
            for line in f:
                if 'Grid Width' in line:
                    width_line = line.rstrip().replace('Grid Width:', '')
                    width_line = width_line.split(';', 1)[0]
                    width_line = width_line.split('#', 1)[0]
                    width_line = width_line.replace(' ', '')
                    width = int(width_line)
                elif 'Grid Height' in line:
                    height_line = line.rstrip().replace('Grid Height:', '')
                    height_line = height_line.split(';', 1)[0]
                    height_line = height_line.split('#', 1)[0]
                    height_line = height_line.replace(' ', '')
                    height = int(height_line)

        # print(f'    width:  {width}')
        # print(f'    height: {height}')

        create_lwi(projid, tileid, width, height)

        # xwm(f'stopping after creating lwi for {projid} {tileid}')
