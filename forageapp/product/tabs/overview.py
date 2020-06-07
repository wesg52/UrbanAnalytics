from collections import OrderedDict


population_columns = [
    #'2009-E-population',
    '2010-E-population',
    '2011-E-population',
    '2012-E-population',
    '2013-E-population',
    '2014-E-population',
    '2015-E-population',
    '2016-E-population',
    '2017-E-population',
    '2018-E-population',
]

total_housing_unit_columns = [
    #'2009-E-total_housing_units',
    '2010-E-total_housing_units',
    '2011-E-total_housing_units',
    '2012-E-total_housing_units',
    '2013-E-total_housing_units',
    '2014-E-total_housing_units',
    '2015-E-total_housing_units',
    '2016-E-total_housing_units',
    '2017-E-total_housing_units',
    '2018-E-total_housing_units',
]

unemployment_columns = [
    #'2009-P-unemployment_rate',
    '2010-P-unemployment_rate',
    '2011-P-unemployment_rate',
    '2012-P-unemployment_rate',
    '2013-P-unemployment_rate',
    '2014-P-unemployment_rate',
    '2015-P-unemployment_rate',
    '2016-P-unemployment_rate',
    '2017-P-unemployment_rate',
    '2018-P-unemployment_rate',
]

median_rent_columns = [
    #'2009-E-median_rent',
    '2010-E-median_rent',
    '2011-E-median_rent',
    '2012-E-median_rent',
    '2013-E-median_rent',
    '2014-E-median_rent',
    '2015-E-median_rent',
    '2016-E-median_rent',
    '2017-E-median_rent',
    '2018-E-median_rent',
]

median_household_income_columns = [
    #'2009-E-median_household_income',
    '2010-E-median_household_income',
    '2011-E-median_household_income',
    '2012-E-median_household_income',
    '2013-E-median_household_income',
    '2014-E-median_household_income',
    '2015-E-median_household_income',
    '2016-E-median_household_income',
    '2017-E-median_household_income',
    '2018-E-median_household_income',
]

renters_percentage_columns = [
    #'2009-P-renters_percentage',
    '2010-P-renters_percentage',
    '2011-P-renters_percentage',
    '2012-P-renters_percentage',
    '2013-P-renters_percentage',
    '2014-P-renters_percentage',
    '2015-P-renters_percentage',
    '2016-P-renters_percentage',
    '2017-P-renters_percentage',
    '2018-P-renters_percentage',
]

overview_graphs = OrderedDict({
    'population': {
        'type': 'census_single_line_CI',
        'columns': population_columns,
        'title': 'Population',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': False
    },
    'total_housing_units': {
        'type': 'census_single_line_CI',
        'columns': total_housing_unit_columns,
        'title': 'Total Housing Units',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': False
    },
    'unemployment': {
        'type': 'census_single_line_CI',
        'columns': unemployment_columns,
        'title': 'Unemployment Rate',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': True
    },
    'median_rent': {
        'type': 'census_single_line_CI',
        'columns': median_rent_columns,
        'title': 'Median Rent',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': False
    },
    'median_household_income': {
        'type': 'census_single_line_CI',
        'columns': median_household_income_columns,
        'title': 'Median Household Income',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': False
    },
    'renters_percentage': {
        'type': 'census_single_line_CI',
        'columns': renters_percentage_columns,
        'title': 'Percentage Renters',
        'xaxis-label': '',
        'yaxis-label': '',
        'percentage': True
    }
})

overview_table = [
    ('Population', population_columns[-1]),
    ('Total Housing Units', total_housing_unit_columns[-1]),
    ('Unemployment Rate', unemployment_columns[-1]),
    ('Median Rent ($)', median_rent_columns[-1]),
    ('Median Household Income ($)', median_household_income_columns[-1]),
    ('Percentage Renters', renters_percentage_columns[-1])
]