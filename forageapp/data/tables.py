import json
import os

import pandas as pd
import numpy as np
import requests

import sys
sys.path.append("..")

import constants
from cities import CITY_MAP, SAVE_TO_DISPLAY_NAME, COUNTY_TO_CITY_MAP
from columns import census_column_name_map


def load_variable_mapping(year, columns=None):
    dirname = constants.CENSUS_DATA_PATH
    file_path = os.path.join(dirname, '%d_acs5' % year, 'profile_variables.json')
    with open(file_path, 'r') as f:
        var_map = json.load(f)['variables']

        if columns is None:
            return var_map

        else:
            return {v: var_map.get(v, 'None')\
                        .get('label', 'Not a census variable')
                         for v in columns}
                         

API_KEY = "e70c2da2298439c24a3bb24f6dd24a03fb30189b"

def download_census_tables(name, areas=None, year=None):
    """Download census tables for every census tract is areas.
    
    areas : str list - state or county fips codes to download tracts for
    year : str - year of census data to download from"""
    DATASET = "acs/acs5"

    # Selected social, economic, housing, and demographic indicators
    TABLES = ["DP02", "DP03", "DP04", "DP05"]


    areas = [str(a) for a in areas]
    year = str(year)
    BASE_URL = "https://api.census.gov/data/%s/%s" % (year, DATASET)

    base_save_dir = constants.CENSUS_DATA_PATH

    data_name = year + "_" + DATASET.split("/")[1]
    path_name = os.path.join(base_save_dir, data_name)
    try:
        os.mkdir(path_name)
    except FileExistsError:
        pass

    save_path = os.path.join(path_name, name + '.csv')
    if os.path.exists(save_path):
        return

    # Download variable mapping
    var_path = os.path.join(path_name, "profile_variables.json")
    if not (os.path.exists(var_path) and os.stat(var_path).st_size > 10):
        vars_request = requests.get(BASE_URL + "/profile/variables.json")
        vars_json = vars_request.json()
        with open(os.path.join(path_name, "profile_variables.json"), "w") as f:
            json.dump(vars_json, f)
        print("Successfully downloaded variable mapping")

    # Download census tract data for all counties and all tables
    county_dfs = []
    for fips_code in areas:
        table_dfs = []
        for table in TABLES:

            table_url = BASE_URL + "/profile?get=group(%s)" % table

            if len(fips_code) == 2:  # State
                table_url += "&for=tract:*&in=state:%s" % fips_code

            elif len(fips_code) == 5:  # County
                state = fips_code[:2]
                county = fips_code[2:]
                table_url += "&for=tract:*&in=state:%s&in=county:%s" % (state, county)

            if API_KEY:
                table_url += "&key=" + API_KEY

            r = requests.get(table_url)
            try:
                json_df = r.json()
            except:
                print('WARNING: table download failure')
                print('url:', table_url)
                print('text', r.text)

            df = pd.DataFrame(json_df[1:], columns=json_df[0])            

            if int(year) < 2011:
                df.rename(columns={"GEO_ID": "GEOID"}, inplace=True)
                df['GEOID'] = df['GEOID'].apply(lambda x: x.split("US")[1])
            else:
                df['state'] = df['state'].astype(str).apply(lambda x: x.zfill(2))
                df['county'] = df['county'].astype(str).apply(lambda x: x.zfill(3))
                df['tract'] = df['tract'].astype(str).apply(lambda x: x.zfill(6))
                df['GEOID'] = df['state'] + df['county'] + df['tract']

            df = df.set_index('GEOID')

            table_dfs.append(df)

        county_year_df = pd.concat(table_dfs, axis=1)
        county_dfs.append(county_year_df)

    city_year_df = pd.concat(county_dfs)
    city_year_df.to_csv(save_path)
    print("Successfully downloaded acs for" , name, 'for', year)


def make_product_table():
    # Make df per year
    year_dfs = {}
    for year in constants.ACS_TIME_COVERAGE:
        city_dfs = []
        for city in CITY_MAP:
            print('Loading', SAVE_TO_DISPLAY_NAME[city], 'for', year)
            df_path = os.path.join(constants.CENSUS_DATA_PATH, '%s_acs5' % str(year), '%s.csv' % city)
            city_df = pd.read_csv(df_path, low_memory=False)
            city_df['GEOID'] = city_df['GEOID'].astype(str)
            city_dfs.append(city_df.set_index('GEOID'))

        year_df = pd.concat(city_dfs)
        year_dfs[year] = year_df

    # Build up the table columns
    print('Extracting columns')
    table_dict = {}
    for table_column_name, census_columns\
        in census_column_name_map.items():

        if isinstance(census_columns, list):
            table_dict[table_column_name] = sum([year_dfs[year][column]
                                            for year, column in census_columns])

            moe_census_columns = [name.replace('E', 'M') for _, name in census_columns]

            year = census_columns[0][0]
            moe_table_column = "%d-M-%s" % (year, table_column_name.split('-')[-1])

            moe_sum = sum([year_dfs[year][column]
                            for column in moe_census_columns])
            table_dict[moe_table_column] = moe_sum / len(moe_census_columns)**.5
        else:
            year, census_column_name = census_columns
            table_dict[table_column_name] = year_dfs[year][census_column_name]

            moe_census_column = census_column_name.replace('E', 'M')
            moe_table_column = "%d-M-%s" % (year, table_column_name.split('-')[-1])

            table_dict[moe_table_column] = year_dfs[year][moe_census_column]

    print('Join and save...')
    df = pd.DataFrame(table_dict)
    df = df[df['%d-E-population' % constants.ACS_BASE_YEAR] > 250]
    df[df < 0] = np.nan


    df['city'] = df.apply(lambda x: COUNTY_TO_CITY_MAP[str(x.name).zfill(11)[:5]], axis=1)
    df.to_csv(os.path.join(constants.PRODUCT_GEO_PATH, 'tract_table.csv'), index_label='GEOID')

    return set([i.zfill(11) for i in df.index])
