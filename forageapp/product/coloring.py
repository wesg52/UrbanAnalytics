import pandas as pd
from colour import Color
from numpy import interp
from math import log10, floor

default_color_columns = {
    'Median Rent' : '2018-E-median_rent',
    'Median Household Income': '2018-E-median_household_income',
    'Population': '2018-E-population',
    'Unemployment Rate': '2018-P-unemployment_rate',
    'Percentage Renter': '2018-P-renters_percentage',
    'Percentage Bachelors+': '2018-P-bachelors_or_higher',
    'Percentage in Poverty': '2018-P-families_below_poverty_line'
}

default_min_alpha = 0.03
default_alpha = .75

default_color_schemes = { # Low to high
    'Median Rent' : [
        (Color(hsl=(2/3, 1, .5)), default_alpha),
        (Color(hsl=(1, 1, .5)), default_alpha)
    ],
    'Median Household Income': [
        (Color(hsl=(0, 1, .5)), default_alpha),
        (Color(hsl=(1/3, 1, .5)), default_alpha)
    ],
    'Population': [
        (Color('blue'), default_min_alpha), 
        (Color('blue'), default_alpha)
    ],
    'Unemployment Rate': [
        (Color('red'), default_min_alpha), 
        (Color('red'), default_alpha)
    ],
    'Percentage Renter': [
        (Color('blue'), default_min_alpha), 
        (Color('blue'), default_alpha)
    ],
    'Percentage Bachelors+': [
        (Color(hsl=(0, 1, .5)), default_alpha),
        (Color(hsl=(1/3, 1, .5)), default_alpha)
    ],
    'Percentage in Poverty': [
        (Color('red'), default_min_alpha), 
        (Color('red'), default_alpha)
    ],
    'similarity': [
        (Color(hsl=(0, 0, 0)), 0), 
        (Color(hsl=(0, 0, 0)), 0),
        (Color('blue'), default_alpha)
    ]
}

def round_to_n(x, n):
    return round(x, -int(floor(log10(abs(x)+.0001))) + (n - 1))


def interpolator(color_scheme, n=5):
    if color_scheme[0][0].hue != color_scheme[1][0].hue:
        c1, a1 = color_scheme[0]
        c2, a2 = color_scheme[1]

        color_list = [c1] *3 + [c2] * 3
        alpha_list = [a1, (a1 + default_min_alpha)/ 2, default_min_alpha,
                        default_min_alpha, (default_min_alpha + a2) / 2, a2]

    elif len(color_scheme) == 2:
        c1, a1 = color_scheme[0]
        c2, a2 = color_scheme[1]
        color_list = list(c1.range_to(c2, 5))
        alpha_list = [a1] + list(interp([1, 2, 3], [0, 4], [a1, a2])) + [a2]

    elif len(color_scheme) == 3:
        c1, a1 = color_scheme[0]
        c2, a2 = color_scheme[1]
        c3, a3 = color_scheme[2]
        color_half_list1 = list(c1.range_to(c2, 3))
        color_half_list2 = list(c2.range_to(c3, 3))
        color_list = color_half_list1 + color_half_list2[1:]
        alpha_list = [a1, (a1 + a2) / 2, a2, (a2 + a3) / 2, a3]

    return color_list, alpha_list

def make_map_coloring(value_series, column):
    lb = value_series.quantile(0.1)
    p30 = value_series.quantile(0.3)
    median = value_series.quantile(0.5)
    p70 = value_series.quantile(0.7)
    ub = value_series.quantile(0.9)

    color_scheme = default_color_schemes[column]
    color_list, alpha_list = interpolator(color_scheme)

    fill_color_spec = [
        "interpolate",
          ["linear"],
          ["feature-state", "color_column"]
    ]
    if len(color_list) == 6:
        percentiles = [.1, .3, .5, .5, .7, .9]
    else:
        percentiles = [.1, .3, .5, .7, .9]

    percentile_values = [round_to_n(value_series.quantile(x), 3)
                         for x in percentiles]

    for v, c, a in zip(percentile_values, color_list, alpha_list):
        fill_color_spec.append(v)
        rgba = (int(c.red * 255), int(c.green * 255), int(c.blue * 255), a)
        fill_color_spec.append("rgba" + str(rgba))

    if len(fill_color_spec) == 15:
        fill_color_spec[9] += .01 # Ensure color scheme is in ascending order
        

    print('fill_color_spec', len(fill_color_spec))
    
    return fill_color_spec


def make_similarity_coloring():
    pass

