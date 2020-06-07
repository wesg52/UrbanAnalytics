import os


ACS_BASE_YEAR = 2018
# Currently 
ACS_TIME_COVERAGE = [y for y in range(2010, ACS_BASE_YEAR + 1)]

# The root directory of the repository
PROJECT_ROOT_DIR = os.path.dirname(__file__)

PROJECT_TEMP_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, '..', 'tmp')

CENSUS_SHAPE_PATH = os.path.join(PROJECT_TEMP_DATA_DIR, 'shapes')

CENSUS_DATA_PATH = os.path.join(PROJECT_TEMP_DATA_DIR, 'acs_data')

PRODUCT_GEO_PATH = os.path.join(PROJECT_ROOT_DIR, 'static', 'tracts')
