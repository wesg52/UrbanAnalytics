import os
import sys
sys.path.append("..")
import constants
from cities import CITY_MAP
from geographies import *
from tables import * 
from embedding import create_product_embedding_df


# Pull TIGER shapefiles from census databases
print('Downloading state shapes...')
download_state_shapes()

if not os.path.exists(constants.CENSUS_DATA_PATH):
    os.mkdir(constants.CENSUS_DATA_PATH)

# Download raw profile tables for all cities for all times
print('Downloading raw census tables...')
for year in constants.ACS_TIME_COVERAGE:
    for city, county_list in list(CITY_MAP.items()):
        download_census_tables(city, county_list, year)

# Process above and pull only columns used by product
print('Processing raw census tables into product tables...')
geoids = make_product_table()

# Process state shapefile to city geojson files for serving on product
# keeping only those that meet a population threshold.
print('Converting state shapefiles to city geojsons...')
make_city_geojson_files(geoids)

print('Constructing product embedding dataframe...')
create_product_embedding_df()