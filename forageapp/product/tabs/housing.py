from collections import OrderedDict
from forageapp.product.tabs.overview import *


bedroom_count = [
'2018-P-housing_units_no_bedrooms',
'2018-P-housing_units_1_bedrooms',
'2018-P-housing_units_2_bedrooms',
'2018-P-housing_units_3_4_bedrooms',
'2018-P-housing_units_5_or_more_bedrooms'
]

rent_lt_1000 = [
#'2009-P-rent_lt_1000',
'2010-P-rent_lt_1000',
'2011-P-rent_lt_1000',
'2012-P-rent_lt_1000',
'2013-P-rent_lt_1000',
'2014-P-rent_lt_1000',
'2015-P-rent_lt_1000',
'2016-P-rent_lt_1000',
'2017-P-rent_lt_1000',
'2018-P-rent_lt_1000',
]

rent_1000_1500 = [
#'2009-P-rent_1000_1500',
'2010-P-rent_1000_1500',
'2011-P-rent_1000_1500',
'2012-P-rent_1000_1500',
'2013-P-rent_1000_1500',
'2014-P-rent_1000_1500',
'2015-P-rent_1000_1500',
'2016-P-rent_1000_1500',
'2017-P-rent_1000_1500',
'2018-P-rent_1000_1500',
]


rent_1500andover = [
#'2009-P-rent_1500andover',
'2010-P-rent_1500andover',
'2011-P-rent_1500andover',
'2012-P-rent_1500andover',
'2013-P-rent_1500andover',
'2014-P-rent_1500andover',
'2015-P-rent_1500andover',
'2016-P-rent_1500andover',
'2017-P-rent_1500andover',
'2018-P-rent_1500andover',
]

GRAPI_15below = [
#'2009-P-GRAPI_15below',
'2010-P-GRAPI_15below',
'2011-P-GRAPI_15below',
'2012-P-GRAPI_15below',
'2013-P-GRAPI_15below',
'2014-P-GRAPI_15below',
'2015-P-GRAPI_15below',
'2016-P-GRAPI_15below',
'2017-P-GRAPI_15below',
'2018-P-GRAPI_15below',
]

GRAPI_15_25 = [
#'2009-P-GRAPI_15_25',
'2010-P-GRAPI_15_25',
'2011-P-GRAPI_15_25',
'2012-P-GRAPI_15_25',
'2013-P-GRAPI_15_25',
'2014-P-GRAPI_15_25',
'2015-P-GRAPI_15_25',
'2016-P-GRAPI_15_25',
'2017-P-GRAPI_15_25',
'2018-P-GRAPI_15_25',
]

GRAPI_25_35 = [
#'2009-P-GRAPI_25_35',
'2010-P-GRAPI_25_35',
'2011-P-GRAPI_25_35',
'2012-P-GRAPI_25_35',
'2013-P-GRAPI_25_35',
'2014-P-GRAPI_25_35',
'2015-P-GRAPI_25_35',
'2016-P-GRAPI_25_35',
'2017-P-GRAPI_25_35',
'2018-P-GRAPI_25_35',
]

GRAPI_35andover = [
#'2009-P-GRAPI_35andover',
'2010-P-GRAPI_35andover',
'2011-P-GRAPI_35andover',
'2012-P-GRAPI_35andover',
'2013-P-GRAPI_35andover',
'2014-P-GRAPI_35andover',
'2015-P-GRAPI_35andover',
'2016-P-GRAPI_35andover',
'2017-P-GRAPI_35andover',
'2018-P-GRAPI_35andover',
]

homeowner_vacancy_rate = [
#'2009-P-homeowner_vacancy_rate',
'2010-P-homeowner_vacancy_rate',
'2011-P-homeowner_vacancy_rate',
'2012-P-homeowner_vacancy_rate',
'2013-P-homeowner_vacancy_rate',
'2014-P-homeowner_vacancy_rate',
'2015-P-homeowner_vacancy_rate',
'2016-P-homeowner_vacancy_rate',
'2017-P-homeowner_vacancy_rate',
'2018-P-homeowner_vacancy_rate',
]

renters_vacancy_rate = [
#'2009-P-renters_vacancy_rate',
'2010-P-renters_vacancy_rate',
'2011-P-renters_vacancy_rate',
'2012-P-renters_vacancy_rate',
'2013-P-renters_vacancy_rate',
'2014-P-renters_vacancy_rate',
'2015-P-renters_vacancy_rate',
'2016-P-renters_vacancy_rate',
'2017-P-renters_vacancy_rate',
'2018-P-renters_vacancy_rate',
]

renter_occupied = [
#'2009-P-renter_occupied',
'2010-P-renter_occupied',
'2011-P-renter_occupied',
'2012-P-renter_occupied',
'2013-P-renter_occupied',
'2014-P-renter_occupied',
'2015-P-renter_occupied',
'2016-P-renter_occupied',
'2017-P-renter_occupied',
'2018-P-renter_occupied',
]

owner_occupied = [
#'2009-P-owner_occupied',
'2010-P-owner_occupied',
'2011-P-owner_occupied',
'2012-P-owner_occupied',
'2013-P-owner_occupied',
'2014-P-owner_occupied',
'2015-P-owner_occupied',
'2016-P-owner_occupied',
'2017-P-owner_occupied',
'2018-P-owner_occupied',
]

buildings_built_date = [
'2018-P-buildings_built_after_2010',
'2018-P-buildings_built_2000_to_2009',
'2018-P-buildings_built_1980_to_1999',
'2018-P-buildings_built_1960_to_1979',
'2018-P-buildings_built_1940_to_1959',
'2018-P-buildings_built_before_1939']

buildings_unit_count = [
'2018-P-buildings_1unit',
'2018-P-buildings_2units',
'2018-P-buildings_3or4_units',
'2018-P-buildings_5to9_units',
'2018-P-buildings_10to19_units',
'2018-P-buildings_20ormore_units'
]

buildings_room_count = [
'2018-P-housing_units_1_2_room',
'2018-P-housing_units_3_4_room',
'2018-P-housing_units_5_6_7_room',
'2018-P-housing_units_8_9_room']

median_owner_occupied_value = [
#'2009-E-median_owner_occupied_value',
'2010-E-median_owner_occupied_value',
'2011-E-median_owner_occupied_value',
'2012-E-median_owner_occupied_value',
'2013-E-median_owner_occupied_value',
'2014-E-median_owner_occupied_value',
'2015-E-median_owner_occupied_value',
'2016-E-median_owner_occupied_value',
'2017-E-median_owner_occupied_value',
'2018-E-median_owner_occupied_value']

monthly_owner_costs = [
#'2009-E-monthly_owner_costs',
'2010-E-monthly_owner_costs',
'2011-E-monthly_owner_costs',
'2012-E-monthly_owner_costs',
'2013-E-monthly_owner_costs',
'2014-E-monthly_owner_costs',
'2015-E-monthly_owner_costs',
'2016-E-monthly_owner_costs',
'2017-E-monthly_owner_costs',
'2018-E-monthly_owner_costs']

same_house_year_ago = [
#'2009-P-same_house_year_ago',
'2010-P-same_house_year_ago',
'2011-P-same_house_year_ago',
'2012-P-same_house_year_ago',
'2013-P-same_house_year_ago',
'2014-P-same_house_year_ago',
'2015-P-same_house_year_ago',
'2016-P-same_house_year_ago',
'2017-P-same_house_year_ago',
'2018-P-same_house_year_ago',
]

move_in_time = [
'2018-P-moved_in_2017_or_later',
'2018-P-moved_in_2015_to_2016',
'2018-P-moved_in_2010_to_2014',
'2018-P-moved_in_2000_to_2009',
'2018-P-moved_in_before2000'
]

housing_graphs = OrderedDict({
    'occupied_units': {
        'type': 'multi_line',
        'columns': [renter_occupied, owner_occupied],
        'title': 'Occupied Units',
        'legend': ['Renter %', 'Owner %'],
        'percentage': True
    },
    'vacancy': {
        'type': 'multi_line',
        'columns': [renters_vacancy_rate, homeowner_vacancy_rate],
        'title': 'Vacancy Rate',
        'legend': ['Renter vacancy', 'Owner vacancy'],
        'percentage': True
    },
    'rent': {
        'type': 'multi_line',
        'columns': [rent_lt_1000, rent_1000_1500,
                    rent_1500andover],
        'legend': ['<$1000', '$1000-1499', '$1500+'],
        'title': 'Monthly Rent Costs',
        'percentage': True
    },
    'GRAPI': {
        'type': 'multi_line',
        'columns': [GRAPI_15below, GRAPI_15_25,
                    GRAPI_25_35, GRAPI_35andover],
        'legend': ['<15%', '15-25%', '25-35%', '>35%'],
        'title': 'Gross Rent as a Percentage of Income',
        'percentage': True
    },
    'median_costs': {
        'type': 'multi_line',
        'columns': [median_rent_columns, monthly_owner_costs],
        'legend': ['Median Rent', 'Median Owner Costs'],
        'title': 'Median Housing Costs',
        'percentage': False
    },
    'median_owner_value': {
        'type': 'census_single_line_CI',
        'columns': median_owner_occupied_value,
        'title': 'Median Owner Occupied unit Value',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': False
    },
    'same_house_year_ago': {
        'type': 'census_single_line_CI',
        'columns': same_house_year_ago,
        'title': 'Lived in same house 1 year ago',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': True
    },
    'move_in_time': {
        'type': 'pie',
        'columns': move_in_time,
        'legend': ['2017 or later', '2015-2016', '2010-2014',
                     '2000-2009', 'before 2000'],
        'title': 'Time of move to current residence',
        'percentage': True
    },
    'building_age': {
        'type': 'pie',
        'columns': buildings_built_date,
        'legend': ['Built after 2010', 'Built 2000-2009', 'Built 1980-1999',
                 'Built 1960-1979', 'Built 1940-1959', 'Built before 1939'],
        'title': 'Housing Unit Construction Date',
        'percentage': True
    },
    'building_units': {
        'type': 'pie',
        'columns': buildings_unit_count,
        'legend': ['1 unit', '2 units', '3-4 units', '5-9 units',
                     '10-19 units', '20+ units'],
        'title': 'Units per Structure',
        'percentage': True
    },
    'building_br_count': {
        'type': 'pie',
        'columns': bedroom_count,
        'legend': ['Studio', '1 BR', '2 BRs', '3-4 BRs', '5+ BRs'],
        'title': 'Bedrooms per Unit',
        'percentage': True
    },
    'building_room_count': {
        'type': 'pie',
        'columns': buildings_room_count,
        'legend': ['1-2 rooms', '3-4 rooms', '5-7 rooms', '8+ rooms'],
        'title': 'Rooms per Unit',
        'percentage': True
    },
})