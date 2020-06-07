import os
from io import BytesIO
from ftplib import FTP
from zipfile import ZipFile
from urllib.request import urlopen
import sys
sys.path.append("..")
import cities
import constants
import geopandas as gpd
import pandas as pd

def download_state_shapes(state_list=None, year=None):
    """Download shapefiles for states.
    
    state_list: str list - state codes to download
    year : str - year for data to be collected
    
    If arguments are not added, will download shapefiles for all states
    for which we cover for the ACS_BASE_YEAR"""

    if not state_list:
        state_set = set()
        for city, counties in cities.CITY_MAP.items():
            for cfips in counties:
                state_set.add(cfips[:2])
        state_list = list(state_set)

    if not year:
        year = str(constants.ACS_BASE_YEAR)
    

    shapes_dir = constants.CENSUS_SHAPE_PATH
    year = str(year)
    TIGER_URL = "https://www2.census.gov/geo/tiger/TIGER%s/TRACT/" % year

    if not state_list:
        # All states
        state_list = [str(i) for i in range(57)]

    # Defensive programming
    state_list = [str(code) for code in state_list]
    state_list = ["0" + code if len(code) < 2 else code for code in state_list]
    year = str(year)

    try:
        os.mkdir(shapes_dir)
    except FileExistsError:
        pass

    # Check if already have
    downloaded_files = os.listdir(shapes_dir)
    downloaded_files = [f.split("_") for f in downloaded_files]
    cached = [state for state, year in downloaded_files if year == year]
    state_list = [state for state in state_list if state not in cached]
    if not state_list:
        return

    # Login to census FTP server
    ftp = FTP("ftp.census.gov")
    ftp.login()
    ftp.cwd("/geo/tiger/TIGER%s/TRACT/" % year)
    print("Successfully made FTP connection")

    # Download and extract all files for states in state_list
    for file_name in ftp.nlst():
        print(file_name)
        state_code = file_name.split("_")[2]
        if state_code not in state_list:
            continue

        dir_name = os.path.join(shapes_dir, "_".join([state_code, year]))
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            continue

        resp = urlopen(TIGER_URL + file_name)
        zipfile = ZipFile(BytesIO(resp.read()))

        zipfile.extractall(dir_name)
        print("Successfully downloaded and extracted state", state_code)


def make_city_geojson_files(geoids):
    all_gdfs = []
    for city, county_list in cities.CITY_MAP.items():
        counties = []
        for fips in county_list:
            state = fips[:2]
            county = fips[2:]
            fname = os.path.join(constants.CENSUS_SHAPE_PATH,
                                 '%s_%s' % (state, constants.ACS_BASE_YEAR))
            gdf = gpd.read_file(fname)
            gdf = gdf.loc[gdf.ALAND.div(gdf.AWATER + gdf.ALAND) > .1]
            county_gdf = gdf.loc[gdf.COUNTYFP == county, ['GEOID', 'geometry']]
            counties.append(county_gdf)
        if len(counties) > 1:
            city_gdf = gpd.GeoDataFrame(pd.concat(counties, ignore_index=True),
                                         crs=counties[0].crs)
        else:
            city_gdf = counties[0]
            
        city_gdf['GEOID'] = city_gdf['GEOID'].astype(str)
        city_gdf = city_gdf[city_gdf.GEOID.isin(geoids)]
        all_gdfs.append(city_gdf)
        save_name = os.path.join(constants.PRODUCT_GEO_PATH, city + '.geojson')
        city_gdf.to_file(save_name, index=False, driver='GeoJSON')
    all_gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True),
                                         crs=all_gdfs[0].crs)
    save_name = os.path.join(constants.PRODUCT_GEO_PATH, 'polygons.geojson')
    all_gdf.to_file(save_name, index=False, driver='GeoJSON')
    
        




# if __name__ == '__main__':
#     download_state_shapes()