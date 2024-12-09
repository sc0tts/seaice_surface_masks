"""
write_valid_modid_lists.py

Print a list of the valid MODIS sinusoidal tile IDs for
Northern and/or Southern Hemispheres

Note: NASA's "tilemap3" routine was used to query for valid values

For reference:
    NH   SH   Horizontal range
     0   17:       h14-h21
     1   16:       h11-h24
     2   15:       h09-h26
     3   14:       h06-h29
     4   13:       h03-h32
     5   12:       h02-h33
     6   11:       h01-h34
     7   10:       h00-h35
     8    9:       h00-h35

"""


def get_valid_modids(list_nh=False, list_sh=False):  # noqa
    """Returns a list of all the sinusoidal MODIS tile IDS that map to Earth"""
    valid_list = []

    """ NH is vvals 0-8 """
    if list_nh:
        vval = 0
        for hval in range(14, 21 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 1
        for hval in range(11, 24 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 2
        for hval in range(9, 26 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 3
        for hval in range(6, 29 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 4
        for hval in range(3, 32 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 5
        for hval in range(2, 33 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 6
        for hval in range(1, 34 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 7
        for hval in range(0, 35 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 8
        for hval in range(0, 35 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

    # ----- And now, in reverse order for the Southern Hemisphere ----- #
    """ SH is vvals 9-17 """

    if list_sh:
        vval = 9
        for hval in range(0, 35 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 10
        for hval in range(0, 35 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 11
        for hval in range(1, 34 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 12
        for hval in range(2, 33 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 13
        for hval in range(3, 32 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 14
        for hval in range(6, 29 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 15
        for hval in range(9, 26 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 16
        for hval in range(11, 24 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

        vval = 17
        for hval in range(14, 21 + 1):
            valid_list.append('h{:02d}v{:02d}'.format(hval, vval))

    return valid_list


def main_wvm():
    """Command line defaults for write_valid_modids.py """
    valid_modids = get_valid_modids(list_nh=True)
    # print(valid_modids)
    print(f'Number of valid ids (NH): {len(valid_modids)}')

    ofn = 'valid_modids_NH.txt'
    with open(ofn, 'w') as f:
        for modid in valid_modids:
            f.write(modid + '\n')
    print(f'  Wrote NH valid modids to: {ofn}')

    valid_modids = get_valid_modids(list_sh=True)
    # print(valid_modids)
    print(f'Number of valid ids (SH): {len(valid_modids)}')

    ofn = 'valid_modids_SH.txt'
    with open(ofn, 'w') as f:
        for modid in valid_modids:
            f.write(modid + '\n')
    print(f'  Wrote SH valid modids to: {ofn}')


if __name__ == '__main__':
    main_wvm()
