"""
gen_pss_gpds.py

Create a mapx .gpd file for each EASE2 NH tile

GETRID OF MENDIONS OF E2 and E2N
"""

import os
import numpy as np

ps_gpd_dir = './pss_gpds'


def yield_ps_tileids():
    """Return a sequence of the tile IDs for EASE2 NH"""
    for xstr in ('x0', 'x1'):
        for ystr in ('y0', 'y1'):
            yield '{}{}'.format(xstr, ystr)


if not os.path.isdir(ps_gpd_dir):
    print('Creating the gpd directory: {}'.format(ps_gpd_dir))
    os.makedirs(ps_gpd_dir)


def write_pss_common_gpd_lines(f):
    # Write pss common lines
    f.write('# This resolution can be integer-nested to generate\n')
    f.write('#   multiples of 25km maps\n')
    f.write('Map Projection:           Polar_Stereographic_Ellipsoid\n')
    f.write('Map Reference Latitude:         -90.0\n')
    f.write('Map Reference Longitude:          0.0\n')
    f.write('Map Second Reference Latitude:  -70.0\n')
    f.write('Map Eccentricity:                 0.081816153 ; pss\n')
    f.write('Map Equatorial Radius:         6378.273       ; pss\n')


for ps_id in yield_ps_tileids():
    xval = int(ps_id[1:2])
    yval = int(ps_id[3:])

    # Write the 390.625m subgrid gpds
    res = '390'
    ps_fn = os.path.join(
            ps_gpd_dir,
            f'pss{res}_x{xval}y{yval}.gpd')
    with open(ps_fn, 'w') as gpdfile:
        gpdfile.write('# 390.625m Northern Hemisphere Polar Stereo grid parameter definition\n')
        gpdfile.write('# Tile id: {} (of 4)\n'.format(ps_id))
        write_pss_common_gpd_lines(gpdfile)
        gpdfile.write('Map Scale:                        0.390625    ; grid res (km)\n')
        scale = 64
        left_idx = 158 * scale
        if xval == 0:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; left\n')
            gpdfile.write(f'Grid Map Origin Column:       {left_idx - 0.5:5.1f}\n')
        elif xval == 1:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; right\n')
            gpdfile.write(f'Grid Map Origin Column:          -0.5\n')
        if yval == 0:
            top_idx = 174 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; top\n')
            gpdfile.write(f'Grid Map Origin Row:          {top_idx - 0.5:5.1f}\n')
        elif yval == 1:
            top_idx = 158 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; bottom\n')
            gpdfile.write(f'Grid Map Origin Row:             -0.5\n')
    print(f'Wrote: {ps_fn}')

    # Write the 3125m subgrid gpds
    res = '3125'
    ps_fn = os.path.join(
            ps_gpd_dir,
            f'pss{res}_x{xval}y{yval}.gpd')
    with open(ps_fn, 'w') as gpdfile:
        gpdfile.write('# 3125m Northern Hemisphere Polar Stereo grid parameter definition\n')
        gpdfile.write('# Tile id: {} (of 4)\n'.format(ps_id))
        write_pss_common_gpd_lines(gpdfile)
        gpdfile.write('Map Scale:                        3.125       ; grid res (km)\n')
        scale = 8
        left_idx = 158 * scale
        if xval == 0:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; left\n')
            gpdfile.write(f'Grid Map Origin Column:        {left_idx - 0.5:5.1f}\n')
        elif xval == 1:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; right\n')
            gpdfile.write(f'Grid Map Origin Column:          -0.5\n')
        if yval == 0:
            top_idx = 174 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; top\n')
            gpdfile.write(f'Grid Map Origin Row:           {top_idx - 0.5:5.1f}\n')
        elif yval == 1:
            top_idx = 158 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; bottom\n')
            gpdfile.write(f'Grid Map Origin Row:             -0.5\n')
    print(f'Wrote: {ps_fn}')

    # Write the 25km subgrid gpds
    res = '25'
    ps_fn = os.path.join(
            ps_gpd_dir,
            f'pss{res}_x{xval}y{yval}.gpd')
    with open(ps_fn, 'w') as gpdfile:
        gpdfile.write('# 25km Northern Hemisphere Polar Stereo grid parameter definition\n')
        gpdfile.write('# Tile id: {} (of 4)\n'.format(ps_id))
        write_pss_common_gpd_lines(gpdfile)
        gpdfile.write('Map Scale:                       25.0         ; grid res (km)\n')
        scale = 1
        left_idx = 158 * scale
        if xval == 0:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; left\n')
            gpdfile.write(f'Grid Map Origin Column:         {left_idx - 0.5:5.1f}\n')
        elif xval == 1:
            gpdfile.write(f'Grid Width:                   {left_idx:5d}           ; right\n')
            gpdfile.write(f'Grid Map Origin Column:          -0.5\n')
        if yval == 0:
            top_idx = 174 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; top\n')
            gpdfile.write(f'Grid Map Origin Row:            {top_idx - 0.5:5.1f}\n')
        elif yval == 1:
            top_idx = 158 * scale
            gpdfile.write(f'Grid Height:                  {top_idx:5d}           ; bottom\n')
            gpdfile.write(f'Grid Map Origin Row:             -0.5\n')
    print(f'Wrote: {ps_fn}')
