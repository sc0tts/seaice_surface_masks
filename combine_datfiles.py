"""
combine_datfiles.py

Create one large array out of MODIS grids

Usage examples:
    python combine_datfiles.py e2n |& tee out_cd_e2n
    python combine_datfiles.py e2s |& tee out_cd_e2s
    python combine_datfiles.py psn |& tee out_cd_psn
    python combine_datfiles.py pss |& tee out_cd_pss
"""

import os
import numpy as np
import netCDF4 as nc


# Set up directory and filename templates
outdir_ = './combined_lcarrs_{projid}'
fieldsdir_ = './combined_fields_{projid}'
outgpddir_ = './combined_gpds_{projid}'

modis_nc_dir = './modis_LC_Type1'
try:
    assert os.path.isdir(modis_nc_dir)
except AssertionError:
    raise SystemExit(
        f'Could not find dir with nc files of "LC Type1" fields')

modis_nc_fn_ = '{modis_nc_dir}/modis_LC_Type1_{hv_str}.nc'
modlist_fn_ =\
    './modids_{projid}/{projid}{list_res}_{tileid}_modids.txt'


def xwm(m='stopping in xwm()'):
    raise SystemExit(m)


def get_minmax(modlist):
    """Return the minimum h and v indexes of this list of tile ids"""
    hvals = [int(modval[1:3]) for modval in modlist]
    vvals = [int(modval[4:6]) for modval in modlist]
    # print('  {}'.format([pairs for pairs in zip(hvals, vvals)]))

    return min(hvals), min(vvals), max(hvals), max(vvals)


def yield_tileids(projid):
    # return the list of tileid's based on the projid
    # EASE2 are x0y0 through x3y3
    # Polar Stereo are x0y0 through x1y1
    # Polar Stereo North has x0y0_left and x0y0_right instead of x0y0
    if projid == 'psn':
        for subgrid_id in ('x0y0_left', 'x0y0_right',
                           'x0y1', 'x1y0', 'x1y1'):
            yield subgrid_id
    elif projid == 'pss':
        for subgrid_id in ('x0y0', 'x0y1', 'x1y0', 'x1y1'):
            yield subgrid_id
    elif projid == 'e2n' or projid == 'e2s':
        for y in range(4):
            for x in range(4):
                yield f'x{x}y{y}'
    else:
        xwm('projid not recognized in yield_tileids(): {projid}')


def main_cd(projid):
    """Main command line routine or combine_datfiles"""

    # Test a single combined tile
    """
    tileid = 'x1y1'
    combine_tiles(psn_tileid)
    xwm(f'stopping after creating {tileid}')
    """

    # Run through all psn tiles
    # for yval in range(4):
    #     for xval in range(4):
    #         psn_tileid = f'x{xval}y{yval}'
    #         combine_tiles(psn_tileid)

    # for psn_tileid, suffix in \
    #         (('x0y0left', ''),  ('x0y0right', ''),
    #          ('x0y1', ''),  ('x1y0', ''), ('x1y1', ''), ):

    for tileid in yield_tileids(projid):
        print(f'Combining: {tileid}')
        combine_tiles(projid, tileid)


def combine_tiles(projid, tileid, list_res=3125):
    """Combine for this d2n tile id"""
    print(f'In combine_tiles() projid: {projid}')
    print(f'In combine_tiles() tileid: {tileid}')

    modlist_fn = modlist_fn_.format(
            projid=projid,
            list_res=list_res,
            tileid=tileid)
    try:
        assert os.path.isfile(modlist_fn)
    except AssertionError:
        xwm(f'  No such modlist_fn: {modlist_fn}')

    with open(modlist_fn, 'r') as f:
        modlines = f.readlines()
    modlist = []
    for modline in modlines:
        modlist.append(modline.rstrip())

    print(f'modlist:\n{modlist}')

    minh, minv, maxh, maxv = get_minmax(modlist)
    print(f'  ({minh}, {minv}) - ({maxh}, {maxv})')

    xdim = (maxh - minh + 1) * 2400
    ydim = (maxv - minv + 1) * 2400

    meters_per_sinutile = 20015109.3541 / 18
    xorigin = (minh - 18) * meters_per_sinutile
    yorigin = (9 - minv) * meters_per_sinutile

    print('  xorigin ({}):  {:.4f}'.format(minh, xorigin))
    print('  yorigin ({}):  {:.4f}'.format(minv, yorigin))
    print('  dims; {}, {}'.format(xdim, ydim))

    outgpddir = outgpddir_.format(projid=projid)
    os.makedirs(outgpddir, exist_ok=True)

    combined_hv_string = f'h{minh:02d}v{minv:02d}_h{maxh:02d}v{maxv:02d}'
    gpdfname = f'{outgpddir}/combined_{combined_hv_string}.gpd'  # noqa

    with open(gpdfname, 'w') as outfile:
        outfile.write(f'; grid parameter definition file for combined MODIS tile {combined_hv_string}\n')  # noqa
        outfile.write('Map Projection:            Sinusoidal\n')
        outfile.write('Map Reference Latitude:    0\n')
        outfile.write('Map Reference Longitude:   0\n')
        outfile.write('Map Equatorial Radius:     6371007.181\n')
        outfile.write(f'Map Origin X:     {xorigin:.4f}\n')
        outfile.write(f'Map Origin Y:     {yorigin:.4f}\n')
        outfile.write('Grid Map Origin Column:   -0.5\n')
        outfile.write('Grid Map Origin Row:      -0.5\n')
        outfile.write('Grid Map Units per Cell:   463.31271653\n')
        outfile.write(f'Grid Width:                {xdim}\n')
        outfile.write(f'Grid Height:               {ydim}\n')

    print('Wrote combined .gpd file to: {}'.format(gpdfname))

    # Link this to the subgrid id
    subgrid_gpdfname = f'{outgpddir}/combinedsinu_for_{projid}_{tileid}.gpd'
    link_cmd = f'ln -sf {os.path.basename(gpdfname)} {subgrid_gpdfname}'
    print(f'Linking this gpdfilename to: {subgrid_gpdfname}')
    os.system(link_cmd)

    # Set up the combined-array.
    # Initialize all the values to "water"
    # because if there were land or ice in
    # the MCD12Q1 field, it would exist and overwrite this value
    array = np.zeros((ydim, xdim), dtype=np.uint8)
    array[:, :] = 17
    print(f'Initialized combined array of shape {array.shape} to water')

    for modid in modlist:
        hval = int(modid[1:3])
        vval = int(modid[4:6])

        xoff = (hval - minh) * 2400
        yoff = (vval - minv) * 2400

        # print(f'  for {modid}: xoff = {xoff}  yoff = {yoff}')

        modis_nc_fn = modis_nc_fn_.format(
                modis_nc_dir=modis_nc_dir,
                hv_str=modid)

        if os.path.isfile(modis_nc_fn):
            # The .nc file for this tile exists

            ncfid = nc.Dataset(modis_nc_fn, 'r')
            # Read data from this nc file without dtype conversion
            ncfid.set_auto_maskandscale(False)
            print('  Opened: {}'.format(modis_nc_fn), flush=True)
            gridvals = ncfid.variables['Band1']
        else:
            # No .nc file, so there is no MCD12Q1 file for this MODIS tile
            # Assume "all water" for these values
            print(f'  No file: {modis_nc_fn}, assuming all water', flush=True)
            gridvals = np.zeros((2400, 2400), dtype=np.uint8)
            gridvals[:] = 17

        array[yoff:yoff+2400, xoff:xoff+2400] = np.flipud(gridvals[:, :])
        ncfid = None
        if gridvals is not None:
            gridvals = None

    # Create the land, water, ice files
    print('shape of array: {}'.format(array.shape))

    outdir = outdir_.format(projid=projid)
    os.makedirs(outdir, exist_ok=True)

    """
    combined_fn = \
        '{}/combined_h{:02d}v{:02d}_h{:02d}v{:02d}.dat'.format(
           outdir, minh, minv, maxh, maxv)
    """
    combined_fn = f'{outdir}/combined_{combined_hv_string}.dat'
    array.tofile(combined_fn)
    print('')
    print(f'Wrote combined file: {combined_fn}', flush=True)

    subgrid_combined_fn = f'{outdir}/combinedsinu_for_{projid}_{tileid}.dat'
    link_cmd = f'ln -sf {os.path.basename(combined_fn)} {subgrid_combined_fn}'
    print(f'Linking this combined file to: {subgrid_combined_fn}')
    os.system(link_cmd)

    fieldsdir = fieldsdir_.format(projid=projid)
    os.makedirs(fieldsdir, exist_ok=True)

    lnd_fn = f'{fieldsdir}/combined_h{minh:02d}v{minv:02d}_h{maxh:02d}v{maxv:02d}_lnd.dat'  # noqa
    wtr_fn = f'{fieldsdir}/combined_h{minh:02d}v{minv:02d}_h{maxh:02d}v{maxv:02d}_wtr.dat'  # noqa
    ice_fn = f'{fieldsdir}/combined_h{minh:02d}v{minv:02d}_h{maxh:02d}v{maxv:02d}_ice.dat'  # noqa

    array_lnd = array.copy()
    array_lnd[array == 15] = 0
    array_lnd[array == 17] = 0
    array_lnd[array_lnd != 0] = 200
    # Add fill value for out of bounds
    array_lnd[array == 255] = 255
    array_lnd.tofile(lnd_fn)
    print('Wrote lnd field to: {}'.format(lnd_fn), flush=True)
    array_lnd = None  # Save memory by deleting this variable after use

    array_wtr = array.copy()
    array_wtr[array != 17] = 0
    array_wtr[array_wtr == 17] = 200
    # Add fill value for out of bounds
    array_wtr[array == 255] = 255
    array_wtr.tofile(wtr_fn)
    print('Wrote wtr field to: {}'.format(wtr_fn), flush=True)
    array_wtr = None  # Save memory by deleting this variable after use

    array_ice = array.copy()
    array_ice[array != 15] = 0
    array_ice[array_ice == 15] = 200
    # Add fill value for out of bounds
    array_ice[array == 255] = 255
    array_ice.tofile(ice_fn)
    print('Wrote ice field to: {}'.format(ice_fn), flush=True)
    array_ice = None  # Save memory by deleting this variable after use
    print('', flush=True)

    # Link these combined files to subgrid names
    subgrid_combined_lnd_fn = f'{fieldsdir}/combinedsinu_for_{projid}_{tileid}_lnd.dat'
    link_cmd = f'ln -sf {os.path.basename(lnd_fn)} {subgrid_combined_lnd_fn}'
    print(f'Linking this combined file to: {subgrid_combined_lnd_fn}')
    os.system(link_cmd)

    subgrid_combined_wtr_fn = f'{fieldsdir}/combinedsinu_for_{projid}_{tileid}_wtr.dat'
    link_cmd = f'ln -sf {os.path.basename(wtr_fn)} {subgrid_combined_wtr_fn}'
    print(f'Linking this combined file to: {subgrid_combined_wtr_fn}')
    os.system(link_cmd)

    subgrid_combined_ice_fn = f'{fieldsdir}/combinedsinu_for_{projid}_{tileid}_ice.dat'
    link_cmd = f'ln -sf {os.path.basename(ice_fn)} {subgrid_combined_ice_fn}'
    print(f'Linking this combined file to: {subgrid_combined_ice_fn}')
    os.system(link_cmd)


if __name__ == '__main__':
    import sys

    valid_projids = ('e2n', 'e2s', 'psn', 'pss')

    try:
        projid = sys.argv[1]
        assert projid in valid_projids
    except IndexError:
        xwm(f'''
        Usage: python {sys.argv[0]} <projid>
           where projid is one of: {valid_projids}''')
    except AssertionError:
        xwm(f'projid ({projid}) not one of: {valid_projids}')

    print(f'Calling main_cd() with projid: {projid}')
    main_cd(projid)
