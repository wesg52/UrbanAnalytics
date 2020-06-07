import numpy as np
import pandas as pd
import geopandas as gpd
import sklearn
import random
import os
import copy
from scipy.spatial.distance import pdist, squareform

# explicitly require this experimental feature
from sklearn.experimental import enable_iterative_imputer  # noqa
# now you can import normally from sklearn.impute
from sklearn.impute import IterativeImputer
import sys
sys.path.append("..")
import cities
from constants import *
from sklearn.decomposition import PCA

hi_columns = ['P-with_health_insurance',
       'P-with_private_health_insurance', 'P-with_public_health_insurance']

only_2018_columns = ['P-housing_units_no_bedrooms',
       'P-housing_units_1_bedrooms', 'P-housing_units_2_bedrooms',
       'P-housing_units_3_4_bedrooms', 'P-housing_units_5_or_more_bedrooms',
       'P-buildings_built_after_2010', 'P-buildings_built_2000_to_2009',
       'P-buildings_built_1980_to_1999', 'P-buildings_built_1960_to_1979',
       'P-buildings_built_1940_to_1959', 'P-buildings_built_before_1939',
       'P-moved_in_2017_or_later', 'P-moved_in_2015_to_2016',
       'P-moved_in_2010_to_2014', 'P-moved_in_2000_to_2009',
       'P-moved_in_before2000']

non_essential_columns = [
    'E-total_housing_units',
    'P-rent_lt_1000',
    'P-rent_1000_1500',
    'P-rent_1500andover',
    'P-GRAPI_15below',
    'P-GRAPI_15_25',
    'P-GRAPI_25_35',
    'P-homeowner_vacancy_rate',
    'P-owner_occupied',
    'P-housing_units_1_2_room',
    'P-housing_units_3_4_room',
    'P-housing_units_5_6_7_room',
    'P-housing_units_8_9_room',
    'P-buildings_2units',
    'P-buildings_3or4_units',
    'P-buildings_5to9_units',
    'P-buildings_10to19_units',
    'P-family_households',
    'P-born_in_us',
    'P-black',
    'P-asain',
    'P-hispanic',
    'P-multi_racial',
    'P-other_race',
    'E-male_population',
    'E-female_population',
    'P-under20',
    'P-20to34',
    'P-35to64',
    'P-over65',
    'P-walk_to_work',
    'P-with_supplemental_security_income',
    'P-with_cash_public_assistance_income',
    'P-with_snap_benefits',
    'P-industry_healthcare_and_education',
    'P-industry_manufacturing',
    'P-industry_recreation_and_service',
    'P-industry_public_administration',
]

drop_columns = hi_columns + only_2018_columns + non_essential_columns

def clean_df():
    print('Loading tract table')
    df = pd.read_csv(os.path.join(PRODUCT_GEO_PATH, 'tract_table.csv'))
    df['GEOID'] = df['GEOID'].astype(str).apply(lambda x: x.zfill(11))
    df = df.set_index('GEOID')
    geoid_to_city = df.city.to_dict()

    df = df[[c for c in df.columns if '-M-' not in c]]

    print('Reformatting tract table')
    year_dfs = []
    for year in ACS_TIME_COVERAGE:
        year_df = df[[c for c in df.columns if c.split('-')[0] == str(year)]]
        year_df = year_df.rename(columns={c: '-'.join(c.split('-')[1:]) for c in year_df.columns})
        year_df['year'] = year
        year_df = year_df.set_index('year', append=True)
        year_dfs.append(year_df) 

    gydf = pd.concat(year_dfs)
    gydf['city'] = gydf.apply(lambda x: geoid_to_city[x.name[0]], axis=1)
    gydf = gydf.set_index('city', append=True)

    gydf = gydf.drop(columns=drop_columns)

    print('Imputing missing values')
    imp_mean = IterativeImputer(random_state=0,
                                min_value=0,
                                skip_complete=True,
                                imputation_order='random')
    X = imp_mean.fit_transform(gydf.values)

    cdf = copy.deepcopy(gydf)
    cdf.iloc[:, :] = X

    return cdf, geoid_to_city



def normalize_df(cdf):
    scalers = {}
    cy_dfs = []
    city_year_groups = cdf.groupby(['year', 'city'])
    for (city, year), cy_group in city_year_groups.groups.items():
        cy_skaler = sklearn.preprocessing.StandardScaler()
        X = cdf.loc[cy_group]
        cy_skaler.fit(X.values)
        cy_df = pd.DataFrame(cy_skaler.transform(X.values),
                                        columns=X.columns,
                                        index=X.index)
        cy_dfs.append(cy_df)
        scalers[(city, year)] = cy_skaler
    ndf = pd.concat(cy_dfs)
    return ndf, scalers

def construct_neighborhoods(cdf, geoid_to_city, space_k, distance_exponential=1):
    '''Returns the neighborhood weights based off of population / distance^p'''
    tracts = gpd.read_file(os.path.join(PRODUCT_GEO_PATH, 'polygons.geojson'))
    tracts['GEOID'] = tracts['GEOID'].astype(str).apply(lambda x: x.zfill(11))
    tracts = tracts.set_index('GEOID').to_crs(epsg=3078) # Change units to meters
    tracts['city'] = tracts.apply(lambda x: geoid_to_city[x.name], axis=1)
    tracts['x'] = tracts.centroid.x
    tracts['y'] = tracts.centroid.y

    def dist_df(x):
        return pd.DataFrame(squareform(pdist(x[['x', 'y']].values)),
                            columns=x.index,
                            index=x.index)

    city_groups = tracts.groupby('city')
    all_city_dist_df = city_groups.apply(dist_df)

    city_distance_dfs = {}
    for city, group in city_groups.groups.items():
        city_tracts = list(group)
        city_distance_dfs[city] = all_city_dist_df.loc[city_tracts, city_tracts] / 1000

    city_tract_to_neighborhood = {}
    for city, dist_df in city_distance_dfs.items():
        city_tract_to_neighborhood[city] = {}
        for tract, dist_row in dist_df.iterrows():
            closest_nbors = dist_row.sort_values()[1:space_k + 1]
            closest_nbors_ix = [(nbor, ACS_BASE_YEAR, city) for nbor in closest_nbors.index
                            if (nbor, ACS_BASE_YEAR, city) in cdf.index]
            closent_nbors_pop = cdf.loc[closest_nbors_ix]['E-population'].reset_index(level=[1,2],drop=True)
            weight = closent_nbors_pop / closest_nbors**1
            n_weight = weight / weight.sum()
            city_tract_to_neighborhood[city][tract] = n_weight

    return city_tract_to_neighborhood


def calc_nborhood(df_index, cdf, city_tract_to_neighborhood):
    gid, year, city = df_index
    try:
        nbor_weights = city_tract_to_neighborhood[city][gid]
    except KeyError:
            return
        
    try:
        nbor_index = [(nbor_id, year, city)  for nbor_id in nbor_weights.index]
        weights = nbor_weights.values

        nborhood_vec = cdf.loc[nbor_index].multiply(weights, axis=0).sum(axis=0)
        return nborhood_vec
        
    except KeyError: # If missing entry
        nbor_info = [((nbor_id, year, city), w)  for nbor_id, w in nbor_weights.iteritems()
                     if (nbor_id, year, city) in cdf.index]

        nbor_index, weights = map(list, zip(*nbor_info))

        nborhood_vec = cdf.loc[nbor_index].multiply(weights, axis=0).sum(axis=0)
        return nborhood_vec

def calc_nborhood_var(df_index, cdf, city_tract_to_neighborhood, wrt_to_mean=False):
    gid, year, city = df_index
    try:
        nbor_weights = city_tract_to_neighborhood[city][gid]
    except KeyError:
            return
        
    try:
        nbor_index = [(nbor_id, year, city)  for nbor_id in nbor_weights.index]
        weights = nbor_weights.values
        nbor_df = cdf.loc[nbor_index]
        if wrt_to_mean:
            nborhood_mean = nbor_df.multiply(weights, axis=0).sum(axis=0)
            return nbor_df.subtract(nborhood_mean).pow(2).multiply(weights, axis=0).sum(axis=0)
        else:
            return nbor_df.subtract(cdf.loc[df_index]).pow(2).multiply(weights, axis=0).sum(axis=0)
        
    except KeyError: # If missing entry
        nbor_info = [((nbor_id, year, city), w)  for nbor_id, w in nbor_weights.iteritems()
                     if (nbor_id, year, city) in cdf.index]

        nbor_index, weights = map(list, zip(*nbor_info))

        nbor_df = cdf.loc[nbor_index]
        if wrt_to_mean:
            nborhood_mean = nbor_df.multiply(weights, axis=0).sum(axis=0)
            return nbor_df.subtract(nborhood_mean).pow(2).multiply(weights, axis=0).sum(axis=0)
        else:
            return nbor_df.subtract(cdf.loc[df_index]).pow(2).multiply(weights, axis=0).sum(axis=0)
    

def construct_feature_components(
    df,
    include_neighborhood_observations=False,
    include_neighborhood_variance=False,
    distance_exponential_penality=2,
    space_k=15,
    include_history=False,
    include_neighborhood_history=False,
    include_neighborhood_history_variance=False,
    time_k=2):

    if include_neighborhood_observations or\
            include_neighborhood_variance or\
            include_neighborhood_history or\
            include_neighborhood_history_variance:

        city_tract_to_neighborhood = construct_neighborhoods(df, space_k)

    ndf = normalize_df(df)

    observation_time_range = list(range(min(ACS_TIME_COVERAGE) + time_k,
                                         max(ACS_TIME_COVERAGE) + 1))

    historical_obs = t0_df.query('year in @observation_time_range')\
                            .apply(lambda x: historical_obs(x), axis=1)

    if use_historical_dif:
        full = pd.concat([t0_df.query('year in @observation_time_range'),
                              t0_df.query('year in @observation_time_range') - historical_obs],
                             axis=1)
    else:
        full = pd.concat([t0_df.query('year in @observation_time_range'),
                          historical_obs],
                         axis=1)


def create_product_embedding_df():
    cdf, geoid_to_city = clean_df()
    ndf, _ = normalize_df(cdf)

    current_df = ndf.query('year == @ACS_BASE_YEAR')
    historical_df = ndf.query('year == @ACS_BASE_YEAR - 3')

    current_df = current_df.reset_index(level=[1,2], drop=True)
    historical_df = historical_df.reset_index(level=[1,2], drop=True)

    current_pca_df = pd.DataFrame(PCA(n_components=.8).fit_transform(current_df.values), index=current_df.index)           
    historical_pca_df = pd.DataFrame(PCA(n_components=.7).fit_transform(historical_df.values), index=historical_df.index)   

    embedding_df = pd.concat([current_pca_df, historical_pca_df], axis=1)
    embedding_df.to_csv(os.path.join(PRODUCT_GEO_PATH, 'embedding_df.csv'))    




        
