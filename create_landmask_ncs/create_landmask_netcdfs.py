"""
create_landmask_netcdfs.py

Create netCDF versions of the land masks, one file per grid
"""

import os
import numpy as np
import xarray as xr


landmask_fns = {
    # Our masks calculated from BU-MODIS, ADD, BMG
    'psn25': '/home/scotts/bumodis_gen//loilid_files/psn25_loilid.dat',
    'psn12.5': '/home/scotts/bumodis_gen//loilid_files/psn12.5_loilid.dat',
    'psn6.25': '/home/scotts/bumodis_gen//loilid_files/psn6.25_loilid.dat',
    'psn3.125': '/home/scotts/bumodis_gen//loilid_files/psn3.125_loilid.dat',

    'pss25': '/home/scotts/bumodis_gen//loilid_files/pss25_loilid.dat',
    'pss12.5': '/home/scotts/bumodis_gen//loilid_files/pss12.5_loilid.dat',
    'pss6.25': '/home/scotts/bumodis_gen//loilid_files/pss6.25_loilid.dat',
    'pss3.125': '/home/scotts/bumodis_gen//loilid_files/pss3.125_loilid.dat',

    'e2n25': '/home/scotts/bumodis_gen//loilid_files/e2n25_loilid.dat',
    'e2n12.5': '/home/scotts/bumodis_gen//loilid_files/e2n12.5_loilid.dat',
    'e2n6.25': '/home/scotts/bumodis_gen//loilid_files/e2n6.25_loilid.dat',
    'e2n3.125': '/home/scotts/bumodis_gen//loilid_files/e2n3.125_loilid.dat',

    'e2s25': '/home/scotts/bumodis_gen//loilid_files/e2s25_loilid.dat',
    'e2s12.5': '/home/scotts/bumodis_gen//loilid_files/e2s12.5_loilid.dat',
    'e2s6.25': '/home/scotts/bumodis_gen//loilid_files/e2s6.25_loilid.dat',
    'e2s3.125': '/home/scotts/bumodis_gen//loilid_files/e2s3.125_loilid.dat',
}

binary_shapes = {
    'psn25': (448, 304),
    'psn12.5': (896, 608),
    'psn6.25': (1792, 1216),
    'psn3.125': (3584, 2432),

    'pss25': (316, 332),
    'pss12.5': (632, 664),
    'pss6.25': (1264, 1328),
    'pss3.125': (2528, 2656),

    'e2n25': (720, 720),
    'e2n12.5': (1440, 1440),
    'e2n6.25': (2880, 2880),
    'e2n3.125': (5760, 5760),

    'e2s25': (720, 720),
    'e2s12.5': (1440, 1440),
    'e2s6.25': (2880, 2880),
    'e2s3.125': (5760, 5760),
}


def xwm(m='exiting in xwm()'):
    raise SystemExit(m)


def get_flag_labels(vals_arr):
    # Given a list of values, return a string
    # with a label for each value in the array

    # The first value should be 50, which is land
    assert vals_arr[0] == 50
    flag_str = "Ocean"

    for val in vals_arr:
        if val == 80:
            flag_str += ' ocean_disconnected'
        elif val == 150:
            flag_str += ' land'
        elif val == 175:
            flag_str += ' fresh_free_water'
        elif val == 200:
            flag_str += ' ice_on_land'
        elif val == 220:
            flag_str += ' floating_ice_shelf'
        elif val == 250:
            flag_str += ' off_earth'
        else:
            if val != 50:
                xwm(f'Unknown land mask value: {val}')

    return flag_str


def get_gridid_info(gridid):
    # Return the crs for this gridid
    if gridid[:3] == 'psn':
        grid_str = 'NSIDC Polar Stereo Northern Hemisphere'
        xleft = -3850000
        xright = 3750000
        yup = 5850000
        ydown = -5350000
        crs_dict = {
            'grid_mapping_name': "polar_stereographic",
            'straight_vertical_longitude_from_pole': -45.,
            'false_easting': 0.,
            'false_northing': 0.,
            'latitude_of_projection_origin': 90.,
            'standard_parallel': 70.,
            'long_name': 'CRS definition',
            'longitude_of_prime_meridian': 0.,
            'semi_major_axis': 6378137.,
            'inverse_flattening': 298.257223563,
            'spatial_ref': 'PROJCS[\"WGS 84 / NSIDC Sea Ice Polar Stereographic North\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Polar_Stereographic\"],PARAMETER[\"latitude_of_origin\",70],PARAMETER[\"central_meridian\",-45],PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",SOUTH],AXIS[\"Northing\",SOUTH],AUTHORITY[\"EPSG\",\"3413\"]]',  # noqa
            'GeoTransform': "-3850000 25000 0 5850000 0 -25000 ",
        }
    elif gridid[:3] == 'pss':
        grid_str = 'NSIDC Polar Stereo Southern Hemisphere'
        xleft = -3950000
        xright = 3950000
        yup = 4350000
        ydown = -3950000
        crs_dict = {
            'grid_mapping_name': "polar_stereographic",
            'straight_vertical_longitude_from_pole': 0.,
            'false_easting': 0.,
            'false_northing': 0.,
            'latitude_of_projection_origin': -90.,
            'standard_parallel': -70.,
            'long_name': 'CRS definition',
            'longitude_of_prime_meridian': 0.,
            'semi_major_axis': 6378137.,
            'inverse_flattening': 298.257223563,
            'spatial_ref': 'PROJCS[\"WGS 84 / NSIDC Sea Ice Polar Stereographic South\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Polar_Stereographic\"],PARAMETER[\"latitude_of_origin\",-70],PARAMETER[\"central_meridian\",0],PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",NORTH],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"3976\"]]',  # noqa
            'GeoTransform': '-3850000 25000 0 5850000 0 -25000 ',
        }
    elif gridid[:3] == 'e2n':
        grid_str = 'EASE 2.0 Northern Hemisphere'
        xleft = -9000000
        xright = 9000000
        yup = 9000000
        ydown = -9000000
        crs_dict = {
            'grid_mapping_name': 'lambert_azimuthal_equal_area',
            'false_easting': 0.,
            'false_northing': 0.,
            'latitude_of_projection_origin': 90.,
            'longitude_of_projection_origin': 0.,
            'long_name': 'CRS definition',
            'longitude_of_prime_meridian': 0.,
            'semi_major_axis': 6378137.,
            'inverse_flattening': 298.257223563,
            'spatial_ref': 'PROJCS[\"WGS 84 / NSIDC EASE-Grid 2.0 North\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Lambert_Azimuthal_Equal_Area\"],PARAMETER[\"latitude_of_center\",90],PARAMETER[\"longitude_of_center\",0],PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",SOUTH],AXIS[\"Northing\",SOUTH],AUTHORITY[\"EPSG\",\"6931\"]]',  # noqa
            'GeoTransform': '-9000000 25000 0 9000000 0 -25000 ',
        }
    elif gridid[:3] == 'e2s':
        grid_str = 'EASE 2.0 Southern Hemisphere'
        xleft = -9000000
        xright = 9000000
        yup = 9000000
        ydown = -9000000
        crs_dict = {
            'grid_mapping_name': 'lambert_azimuthal_equal_area',
            'false_easting': 0.,
            'false_northing': 0.,
            'latitude_of_projection_origin': -90.,
            'longitude_of_projection_origin': 0.,
            'long_name': 'CRS definition',
            'longitude_of_prime_meridian': 0.,
            'semi_major_axis': 6378137.,
            'inverse_flattening': 298.257223563,
            'spatial_ref': 'PROJCS[\"WGS 84 / NSIDC EASE-Grid 2.0 South\",GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]],PROJECTION[\"Lambert_Azimuthal_Equal_Area\"],PARAMETER[\"latitude_of_center\",-90],PARAMETER[\"longitude_of_center\",0],PARAMETER[\"false_easting\",0],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AXIS[\"Easting\",NORTH],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"6932\"]]',  # noqa
            'GeoTransform': '-9000000 25000 0 9000000 0 -25000 ',
        }
    else:
        xwm(f'Cannon get crs_dict from gridid: {gridid}')

    return xleft, xright, yup, ydown, crs_dict, grid_str


def get_gridres(gridid):
    # Determine the grid resolution from the gridid
    if '3.125' in gridid:
        res = 3125
        res_str = '3.125km'
    elif '6.25' in gridid:
        res = 6250
        res_str = '6.25km'
    elif '12.5' in gridid:
        res = 12500
        res_str = '12.5km'
    elif '25' in gridid:
        res = 25000
        res_str = '25km'
    else:
        xwm(f'Could not determine res from gridid {gridid}')

    return res, res_str


def create_landmask_nc(gridid, nc_fn):
    # Create a netCDF file from geotiffs with valid snow and seaice
    #    nc_fn='./NSIDC-XXXX_{gridid.upper()}-SeaIceRegions-v1.0.nc'):

    xleft, xright, yup, ydown, crs_dict, grid_str = get_gridid_info(gridid)
    res, res_str = get_gridres(gridid)
    xdim = (xright - xleft) // res
    ydim = (yup - ydown) // res

    if 'psn' in gridid or 'e2n' in gridid:
        hem = 'north'
    elif 'pss' in gridid or 'e2s' in gridid:
        hem = 'south'
    else:
        xwm(f'Could not determine hem from gridid {gridid}')

    x = np.linspace(xleft + res // 2, xright - res // 2, num=xdim, dtype=np.float32)  # noqa
    y = np.linspace(yup - res // 2, ydown + res // 2, num=ydim, dtype=np.float32)  # noqa

    # Create output netCDF file via xarray
    fn_mask = landmask_fns[gridid]
    try:
        assert os.path.isfile(fn_mask)
    except AssertionError:
        xwm(f'No such .dat file: {fn_mask}')

    land_mask = np.fromfile(fn_mask, dtype=np.uint8).reshape(ydim, xdim)

    # Different summary strings for Northern and Southern Hemispheres
    if hem == 'north':
        summary_string = 'This file provides a land mask derived from the MODIS/Terra+Aqua Land Cover Type Yearly L3 Global 500 m SIN Grid product (2021).  Mask values near Greenland are derived from IceBridge BedMachine, Version 5',  # noqa
    elif hem == 'south':
        summary_string = 'This file provides a land mask derived from the MODIS/Terra+Aqua Land Cover Type Yearly L3 Global 500 m SIN Grid product (2021).  Mask values near Antarctica are derived from the Antarctic Digital Database Seamask product.',  # noqa

    ds = xr.Dataset(
        data_vars=dict(
            land_mask=(['y', 'x'], land_mask, {
                'standard_name': 'area_type',
                'long_name': 'land mask',
                'grid_mapping': 'crs',
                'valid_range': np.array((0, land_mask.max()), dtype=np.uint8),  # noqa
                '_Unsigned': 'true',
                '_FillValue': np.array((255), dtype=np.uint8),
                'flag_values': np.unique(land_mask),
                'flag_meanings': get_flag_labels(np.unique(land_mask)),  # noqa
            }),
            crs=([], '', crs_dict),
        ),
        coords=dict(
            x=(['x'], x, {
                'standard_name': 'projection_x_coordinate',
                'long_name': 'x coordinate of projection',
                'units': 'm',
                'coverage_content_type': 'coordinate',
                'valid_range': np.array((xleft, xright), dtype=np.float32)
            }),
            y=(['y'], y, {
                'standard_name': 'projection_y_coordinate',
                'long_name': 'y coordinate of projection',
                'units': 'm',
                'coverage_content_type': 'coordinate',
                'valid_range': np.array((ydown, yup), dtype=np.float32)
            }),
        ),
        attrs=dict(
            title=f'Land mask for the {res_str} {grid_str} grid',  # noqa
            summary=summary_string,
            id='<DOI>',
            acknowledgment='These data are produced and supported by the NASA National Snow and Ice Data Center Distributed Active Archive Center',  # noqa
            license='Access Constraint: These data are freely, openly, and fully accessible, provided that you are logged into your NASA Earthdata profile (https://urs.earthdata.nasa.gov/).  Use Constraint: These data are freely, openly, and fully available to use without restrictions, provided that you cite the data according to the recommended citation at https://nsidc.org/about/use_copyright.html. For more information on the NASA EOSDIS Data Use Policy, see https://earthdata.nasa.gov/earth-observation-data/data-use-policy.',  # noqa
            product_version=1.0,
            metadata_link='<DOI>',
            Conventions='CF-1.6, ACDD-1.3',
            institution='NASA National Snow and Ice Data Center Distributed Active Archive Center',  # noqa
            contributor_name='Stewart J. S., W. N. Meier',
            contributor_role='scientific_programmer project_scientist',
            publisher_type='institution',
            publisher_institution='National Snow and Ice Data Center, Cooperative Institute for Research in Environmental Sciences, University of Colorado at Boulder, Boulder, CO',  # noqa
            publisher_url='https://nsidc.org/daac',
            publisher_email='nsidc@nsidc.org',
            geospatial_bounds_crs=geospatial_bounds_crs_str,
            geospatial_bounds=geospatial_bounds_str,
            geospatial_lat_min=geospatial_lat_min_str,
            geospatial_lat_max=geospatial_lat_max_str,
            geospatial_lat_units='degrees_north',
            geospatial_lon_min=geospatial_lon_min_str,
            geospatial_lon_max=geospatial_lon_max_str,
            geospatial_lon_units='degrees_east',

        )
    )

    ofn = nc_fn

    ds.to_netcdf(
        ofn,
        encoding={
            'land_mask': {'zlib': True},
        },
    )

    print(f'Wrote: {ofn}')


if __name__ == '__main__':
    import sys

    try:
        gridid = sys.argv[1]
    except IndexError:
        gridid = 'psn25'
        print(f'Using default gridid: {gridid}')

    assert gridid in landmask_fns.keys()
    assert gridid in binary_shapes.keys()

    if 'psn' in gridid:
        proj = 'PS'
        geospatial_bounds_crs_str = 'EPSG:3411'
        geospatial_bounds_str = 'POLYGON ((-3850000 5850000, 3750000 5850000, 3750000 -5350000, -3850000 -5350000, -3850000 5850000))'  # noqa
        geospatial_lat_min_str = 30.98
        geospatial_lat_max_str = 90.
        geospatial_lon_min_str = -180.
        geospatial_lon_max_str = 180.
    elif 'pss' in gridid:
        proj = 'PS'
        geospatial_bounds_crs_str = 'EPSG:3412'
        geospatial_bounds_str = 'POLYGON ((-3950000 4350000, 3950000 4350000, 3950000 -3950000, -3950000 -3950000, -3950000 4350000))'  # noqa
        geospatial_lat_min_str = -90.
        geospatial_lat_max_str = -39.23
        geospatial_lon_min_str = -180.
        geospatial_lon_max_str = 180.
    elif 'e2n' in gridid:
        proj = 'EASE2'
        geospatial_bounds_crs_str = 'EPSG:6931'
        geospatial_bounds_str = 'POLYGON ((-9000000 9000000, 9000000 9000000, 9000000 -9000000, -9000000 -9000000, -9000000 9000000))'  # noqa
        geospatial_lat_min_str = 0.
        geospatial_lat_max_str = 90.
        geospatial_lon_min_str = -180.
        geospatial_lon_max_str = 180.
    elif 'e2s' in gridid:
        proj = 'EASE2'
        geospatial_bounds_crs_str = 'EPSG:6932'
        geospatial_bounds_str = 'POLYGON ((-9000000 9000000, 9000000 9000000, 9000000 -9000000, -9000000 -9000000, -9000000 9000000))'  # noqa
        geospatial_lat_min_str = -90.
        geospatial_lat_max_str = 0.
        geospatial_lon_min_str = -180.
        geospatial_lon_max_str = 180.

    H = gridid[2].upper()
    res = gridid[3:]
    nc_fn = f'./NSIDC-XXXX_{proj}-{H}{res}km_LandMask_v1.0.nc'

    create_landmask_nc(gridid, nc_fn)
