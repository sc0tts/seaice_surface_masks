"""
combine_390_tiles.py

Combine the loil 390 tiles into a single file
"""

import sys
import numpy as np

projid = sys.argv[1]
if projid == 'e2n' or projid == 'e2s':
    xdim = 11520 * 4
    ydim = 11520 * 4
elif projid == 'psn':
    xdim = 304 * 64
    ydim = 448 * 64
elif projid == 'pss':
    xdim = 316 * 64
    ydim = 332 * 64

if xdim == 11520 * 4:
    # x0y0:  9856 14976
    # x0y1:  9856 13696
    # x1y0:  9600 14976
    # x1y1:  9600 13696

    all_grids = np.zeros((ydim, xdim), dtype=np.uint8)
    for x in range(4):
        ioff = x * 11520
        for y in range(4):
            joff = y * 11520

            ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
            indata = np.fromfile(ifn, dtype=np.uint8).reshape(11520, 11520)
            print(f'Read data from: {ifn}', flush=True)
            all_grids[joff:joff+11520, ioff:ioff+11520] = indata[:, :]
    ofn = f'./loil_filled_{projid}/{projid}390_loil.dat'
    all_grids.tofile(ofn)
    print(f'Wrote: {ofn}  {all_grids.shape}')
elif xdim == 304 * 64:
    # PSN
    all_grids = np.zeros((ydim, xdim), dtype=np.uint8)

    x = 0
    y = 0
    ioff = 0
    joff = 0
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(14976, 9856)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+14976, ioff:ioff+9856] = indata[:, :]

    x = 1
    y = 0
    ioff = 9856
    joff = 0
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(14976, 9600)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+14976, ioff:ioff+9600] = indata[:, :]

    x = 0
    y = 1
    ioff = 0
    joff = 14976
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(13696, 9856)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+13696, ioff:ioff+9856] = indata[:, :]

    x = 1
    y = 1
    ioff = 9856
    joff = 14976
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(13696, 9600)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+13696, ioff:ioff+9600] = indata[:, :]

    ofn = f'./loil_filled_{projid}/{projid}390_loil.dat'
    all_grids.tofile(ofn)
    print(f'Wrote: {ofn}  {all_grids.shape}')
elif xdim == 316 * 64:
    # PSS
    all_grids = np.zeros((ydim, xdim), dtype=np.uint8)

    x = 0
    y = 0
    ioff = 0
    joff = 0
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(11136, 10112)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+11136, ioff:ioff+10112] = indata[:, :]

    x = 1
    y = 0
    ioff = 10112
    joff = 0
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(11136, 10112)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+11136, ioff:ioff+10112] = indata[:, :]

    x = 0
    y = 1
    ioff = 0
    joff = 11136
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(10112, 10112)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+10112, ioff:ioff+10112] = indata[:, :]

    x = 1
    y = 1
    ioff = 10112
    joff = 11136
    ifn = f'./loil_filled_{projid}/{projid}390_x{x}y{y}_loil.dat'
    indata = np.fromfile(ifn, dtype=np.uint8).reshape(10112, 10112)
    print(f'Read data from: {ifn}', flush=True)
    all_grids[joff:joff+10112, ioff:ioff+10112] = indata[:, :]

    ofn = f'./loil_filled_{projid}/{projid}390_loil.dat'
    all_grids.tofile(ofn)
    print(f'Wrote: {ofn}  {all_grids.shape}')
