"""
gen_e2s_gpds.py

Create a mapx .gpd file for each EASE2 SH tile
"""

import os
import numpy as np

e2_gpd_dir = './e2s_gpds'


def yield_e2s_tileids():
    """Return a sequence of the tile IDs for EASE2 SH"""
    for xstr in ('x0', 'x1', 'x2', 'x3'):
        for ystr in ('y0', 'y1', 'y2', 'y3'):
            yield '{}{}'.format(xstr, ystr)


if not os.path.isdir(e2_gpd_dir):
    print('Creating the gpd directory: {}'.format(e2_gpd_dir))
    os.makedirs(e2_gpd_dir)


for e2s_id in yield_e2s_tileids():
    xval = int(e2s_id[1:2])
    yval = int(e2s_id[3:])

    # Write the 390.625m subgrid gpds
    res = 390
    e2s_fn = os.path.join(
        e2_gpd_dir,
        f'e2s{res}_x{xval}y{yval}.gpd')
    with open(e2s_fn, 'w') as gpdfile:
        gpdfile.write('# Mapx for EASE2 SH 390.625 grid tile\n')
        gpdfile.write('# Tile id: {}\n'.format(e2s_id))
        gpdfile.write('# This resolution can be integer-nested to generate\n')
        gpdfile.write('#   multiples of 25km maps\n')
        gpdfile.write('Map Projection:           Azimuthal Equal-Area (ellipsoid)\n')
        gpdfile.write('Map Reference Latitude:   -90.0\n')
        gpdfile.write('Map Reference Longitude:  0.0\n')
        gpdfile.write('Map Rotation           :  0.0\n')
        gpdfile.write('Map Equatorial Radius:    6378137.0      ; WGS84\n')
        gpdfile.write('Map Eccentricity:         0.081819190843 ; WGS84\n')
        map_origin_x = -9000000. + xval * 4500000.
        gpdfile.write('Map Origin X:             {}; meters\n'.format(
            map_origin_x))
        map_origin_y = 9000000. - yval * 4500000.
        gpdfile.write('Map Origin Y:             {}; meters\n'.format(
            map_origin_y))
        gpdfile.write('Grid Map Origin Column:   -0.5\n')
        gpdfile.write('Grid Map Origin Row:      -0.5\n')
        gpdfile.write('Grid Map Units per Cell:  390.625;  meters\n')
        gpdfile.write('Grid Width:               11520\n')
        gpdfile.write('Grid Height:              11520\n')

    # Write the 3125m subgrid gpds
    res = 3125
    e2s_fn = os.path.join(
        e2_gpd_dir,
        f'e2s{res}_x{xval}y{yval}.gpd')
    with open(e2s_fn, 'w') as gpdfile:
        gpdfile.write('# Mapx for EASE2 SH 3125 grid tile\n')
        gpdfile.write('# Tile id: {}\n'.format(e2s_id))
        gpdfile.write('# This resolution can be integer-nested to generate\n')
        gpdfile.write('#   multiples of 25km maps\n')
        gpdfile.write('Map Projection:           Azimuthal Equal-Area (ellipsoid)\n')
        gpdfile.write('Map Reference Latitude:   -90.0\n')
        gpdfile.write('Map Reference Longitude:  0.0\n')
        gpdfile.write('Map Rotation           :  0.0\n')
        gpdfile.write('Map Equatorial Radius:    6378137.0      ; WGS84\n')
        gpdfile.write('Map Eccentricity:         0.081819190843 ; WGS84\n')
        map_origin_x = -9000000. + xval * 4500000.
        gpdfile.write('Map Origin X:             {}; meters\n'.format(
            map_origin_x))
        map_origin_y = 9000000. - yval * 4500000.
        gpdfile.write('Map Origin Y:             {}; meters\n'.format(
            map_origin_y))
        gpdfile.write('Grid Map Origin Column:   -0.5\n')
        gpdfile.write('Grid Map Origin Row:      -0.5\n')
        gpdfile.write('Grid Map Units per Cell:  3125;  meters\n')
        gpdfile.write('Grid Width:               1440\n')
        gpdfile.write('Grid Height:              1440\n')

    # Write the 25m subgrid gpds
    res = 25
    e2s_fn = os.path.join(
        e2_gpd_dir,
        f'e2s{res}_x{xval}y{yval}.gpd')
    with open(e2s_fn, 'w') as gpdfile:
        gpdfile.write('# Mapx for EASE2 SH 25 grid tile\n')
        gpdfile.write('# Tile id: {}\n'.format(e2s_id))
        gpdfile.write('# This resolution can be integer-nested to generate\n')
        gpdfile.write('#   multiples of 25km maps\n')
        gpdfile.write('Map Projection:           Azimuthal Equal-Area (ellipsoid)\n')
        gpdfile.write('Map Reference Latitude:   -90.0\n')
        gpdfile.write('Map Reference Longitude:  0.0\n')
        gpdfile.write('Map Rotation           :  0.0\n')
        gpdfile.write('Map Equatorial Radius:    6378137.0      ; WGS84\n')
        gpdfile.write('Map Eccentricity:         0.081819190843 ; WGS84\n')
        map_origin_x = -9000000. + xval * 4500000.
        gpdfile.write('Map Origin X:             {}; meters\n'.format(
            map_origin_x))
        map_origin_y = 9000000. - yval * 4500000.
        gpdfile.write('Map Origin Y:             {}; meters\n'.format(
            map_origin_y))
        gpdfile.write('Grid Map Origin Column:   -0.5\n')
        gpdfile.write('Grid Map Origin Row:      -0.5\n')
        gpdfile.write('Grid Map Units per Cell:  25000;  meters\n')
        gpdfile.write('Grid Width:               180\n')
        gpdfile.write('Grid Height:              180\n')