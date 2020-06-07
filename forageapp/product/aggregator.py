from pandas.tests.groupby import aggregate
import pandas as pd
from forageapp import city_table, polygons, tract_table
from forageapp import constants

INFO_TABLE_COLUMNS = [
    ('Total Population', '%d-E-population' % constants.ACS_BASE_YEAR, 'int'),
    ('Total Housing Units', '%d-E-total_housing_units' % constants.ACS_BASE_YEAR, 'int'),
    ('Percent Renters', '%d-P-renters_percentage' % constants.ACS_BASE_YEAR, 'percent'),
    ('Median Rent', '%d-E-median_rent' % constants.ACS_BASE_YEAR, 'money'),
    ('Median Household Income', '%d-E-median_household_income' % constants.ACS_BASE_YEAR, 'money'),
    ('Unemployment Rate', '%d-P-unemployment_rate' % constants.ACS_BASE_YEAR, 'percent'),
    ('College Educated', '%d-P-bachelors_or_higher' % constants.ACS_BASE_YEAR, 'percent'),
    ('Family Poverty Rate', '%d-P-families_below_poverty_line' % constants.ACS_BASE_YEAR, 'percent'),
]
info_df = tract_table[[c[1] for c in INFO_TABLE_COLUMNS]]
total_columns = [
    '%d-E-population' % constants.ACS_BASE_YEAR,
    '%d-E-total_housing_units' % constants.ACS_BASE_YEAR
]
def generate_info_table_data(geoids):
    if len(geoids) == 1:
        area_values = info_df.loc[geoids[0]].fillna(0)
    else:
        sub_df = info_df.loc[geoids]
        pop_column = '%d-E-population' % constants.ACS_BASE_YEAR
        population_weight = sub_df[pop_column] / sub_df[pop_column].sum()
        area_values = sub_df.multiply(population_weight, axis=0).sum()
        area_values[total_columns] = sub_df[total_columns].sum()

    return area_values


weight_root_columns = {
    'E-population': set([
        'P-20to34',
        'P-35to64',
        'P-asain',
        'P-bachelors_or_higher',
        'P-black',
        'P-born_in_us',
        'P-commute_w_public_transit',
        'P-foriegn_born',
        'P-highschool_grad_or_higher',
        'P-hispanic',
        'P-industry_finance',
        'P-industry_healthcare_and_education',
        'P-industry_manufacturing',
        'P-industry_public_administration',
        'P-industry_recreation_and_service',
        'P-industry_tech',
        'E-mean_commute_time',
        'E-mean_household_income',
        'E-median_age',
        'E-median_household_income',
        'P-multi_racial',
        'P-nonfamily_households',
        'P-occupation_in_management_business_and_science',
        'P-occupation_in_sales_and_office',
        'P-occupation_in_service',
        'P-other_race',
        'P-over65',
        'P-owner_occupied',
        'P-rent_1000_1500',
        'P-rent_1500andover',
        'P-rent_lt_1000',
        'P-same_house_year_ago',
        'P-under20',
        'P-unemployment_rate',
        'P-walk_to_work',
        'P-white',
        'P-with_cash_public_assistance_income',
        'P-with_health_insurance',
        'P-with_private_health_insurance',
        'P-with_public_health_insurance',
        'P-with_snap_benefits',
        'P-with_supplemental_security_income'
    ]),
    'E-total_housing_units': set([
        'P-GRAPI_15_25',
        'P-GRAPI_15below',
        'P-GRAPI_25_35',
        'P-GRAPI_35andover',
        'E-average_family_size',
        'E-average_household_size',
        'P-buildings_10to19_units',
        'P-buildings_1unit',
        'P-buildings_20ormore_units',
        'P-buildings_2units',
        'P-buildings_3or4_units',
        'P-buildings_5to9_units',
        'P-buildings_built_1940_to_1959',
        'P-buildings_built_1960_to_1979',
        'P-buildings_built_1980_to_1999',
        'P-buildings_built_2000_to_2009',
        'P-buildings_built_after_2010',
        'P-buildings_built_before_1939',
        'P-families_below_poverty_line',
        'P-family_households',
        'P-homeowner_vacancy_rate',
        'P-households_w_children',
        'P-households_w_elderly',
        'P-housing_units_1_2_room',
        'P-housing_units_1_bedrooms',
        'P-housing_units_2_bedrooms',
        'P-housing_units_3_4_bedrooms',
        'P-housing_units_3_4_room',
        'P-housing_units_5_6_7_room',
        'P-housing_units_5_or_more_bedrooms',
        'P-housing_units_8_9_room',
        'P-housing_units_no_bedrooms',
        'E-median_owner_occupied_value',
        'E-median_rent',
        'E-monthly_owner_costs',
        'P-moved_in_2000_to_2009',
        'P-moved_in_2010_to_2014',
        'P-moved_in_2015_to_2016',
        'P-moved_in_2017_or_later',
        'P-moved_in_before2000',
        'P-renter_occupied',
        'P-renters_percentage',
        'P-renters_vacancy_rate',
    ])
}

column_weights = {('%d-' % y) + w: [] for w in weight_root_columns
                     for y in constants.ACS_TIME_COVERAGE}

moe_column_weights = {('%d-' % y) + w: [] for w in weight_root_columns
                     for y in constants.ACS_TIME_COVERAGE}
for c in tract_table.columns:
    try:
        year, ctype, name = c.split('-')
    except:
        continue
    c_weight = None
    for weight, col_set in weight_root_columns.items():
        if ctype + '-' + name in col_set:
            c_weight = weight
            break
    if c_weight is None:
        continue
        
    moe_column_weights[('%s-' % year) + c_weight].append(c.replace('-' + ctype + '-', '-M-'))
    column_weights[('%s-' % year) + c_weight].append(c)
    

# column_weights = {}
# moe_column_weights = {}
# for y in constants.ACS_TIME_COVERAGE:
#     for weight_column, column_list in weight_root_columns.items():
#         full_weight_column = ('%d-' % y) + weight_column
#         column_weights[full_weight_column] = []
#         moe_column_weights[full_weight_column] = []
#         for col in column_list:
#             df_col = ('%d-' % y) + col
#             column_weights[full_weight_column].append(df_col)
#             moe_col = ('%d-' % y) + 'M' + col[1:]
#             moe_column_weights[full_weight_column].append(moe_col)


sum_columns = list(column_weights.keys()) + ['%d-E-%s' % (y, c) 
                                            for y in constants.ACS_TIME_COVERAGE
                                            for c in ['female_population', 'male_population']]
moe_sum_columns = [c.replace('-E-', '-M-') for c in sum_columns]



def aggregate_rows(geoids):
    if len(geoids) == 1:
        return tract_table.loc[geoids[0]].to_dict()
    else:
        sub_df = tract_table.loc[geoids]
        area_dicts = []
        for weight_column, column_list in column_weights.items():
            weight = sub_df[weight_column] / sub_df[weight_column].sum()
            sub_row = round(sub_df[column_list].multiply(weight, axis=0).sum(), 2)
            area_dicts.append(sub_row.to_dict())

        for weight_column, moe_column_list in moe_column_weights.items():
            weight = sub_df[weight_column] #/ sub_df[weight_column].sum()
            variance_sum = (sub_df[moe_column_list].multiply(weight, axis=0)**2).sum()
            moe_row = round((variance_sum / sub_df[weight_column].sum()**2) ** .5 , 2)
            area_dicts.append(moe_row.to_dict())

        area_dicts.append(sub_df[sum_columns].sum().astype(int).to_dict())
        area_dicts.append(round((sub_df[moe_sum_columns] ** 2).sum() ** .5, 2).to_dict())

        return {k: v for d in area_dicts for k, v in d.items()}

tract_table['city'] = city_table
city_series = tract_table.groupby('city').apply(lambda x: aggregate_rows(x.index.get_level_values(0)))
city_agg_df = pd.DataFrame(list(city_series), index=city_series.index)
