from collections import OrderedDict
import pandas as pd
import numpy as np
import json
import shapely
from click import group
from flask import Blueprint, flash, jsonify, redirect, render_template, request
from json2html import *

from forageapp import polygons, tract_table, city_table, embedding_df
from forageapp.product.forms import FeedbackForm
from forageapp.product.tabs import housing, overview, economics, demographics
import forageapp.product.coloring as color
import forageapp.product.aggregator as agg
from forageapp.cities import SAVE_TO_DISPLAY_NAME
from forageapp import constants
#from forageapp.spatial_models import CityMap
#from forageapp.user_models import User

product = Blueprint('product', __name__)


@product.route("/send_map_color_data")
def send_map_color_data(city=None):
    if not city:
        city = request.args.get('city')
    default_color_column = 'Median Rent'
    key = request.args.get('key', default_color_column)
    
    if key == 'similarity':
        city_embedding=embedding_df.loc[city_table == city]
        tract_ids = request.args.get('tract_ids', '').split(',')
        #TODO: weight by population
        embedding_vector = city_embedding.loc[tract_ids].mean(axis=0).values
        norm = np.linalg.norm(city_embedding.values, axis=1) * np.linalg.norm(embedding_vector)
        sim_scores = city_embedding.values @ embedding_vector / norm
        data_series = pd.Series(sim_scores, index=city_embedding.index)
    else:
        column = color.default_color_columns[key]
        data_series = tract_table[column].loc[city_table == city]
        data_series[data_series < 0] = 0
        data_series = data_series.fillna(0)

    fill_color = color.make_map_coloring(data_series, key)
    payload = {
        'legend_title': key,
        'fill_color': fill_color,
        'value_dict': data_series.to_dict()
    }
    return payload

sum_columns = ['E-population', 'E-total_housing_units']
def aggregate_tracts(GEOIDS):
    sub_df = tract_df.loc[tract_ids]
    pop_column = '%d-E-population' % constants.ACS_BASE_YEAR
    population_weight = sub_df[pop_column] / sub_df[pop_column].sum()
    area_values = sub_df.multiply(population_weight, axis=0).sum()


@product.route("/")
@product.route("/city_explorer")
def opp_index():
    city = request.args.get('city')
    if not city:
        city = 'nyc'

    color_payload = send_map_color_data(city)

    city_data = tract_table.loc[city_table == city]
    default_table_data = city_data[list(color.default_color_columns.values())]
    default_table_data[default_table_data < 0] = np.nan
    default_table_data = default_table_data.mean()
    

    return render_template('home.html', city=city,
             city_selector=SAVE_TO_DISPLAY_NAME,
             color_selector=list(color.default_color_columns.keys()),
             legend_title=color_payload['legend_title'],
             color_data=color_payload['value_dict'],
             fill_color=color_payload['fill_color'],
             table_data=default_table_data)


@product.route("/tract_dashboard", methods=['GET', 'POST'])
def tract_dashboard():
    tract_ids = request.args.get('tract_ids', '').split(',')
    use_city = False
    if tract_ids == ['']:
        city = request.args.get('city')
        tract_ids = list(city_table.loc[city_table == city].index)
        use_city = True
    try:
        shape = polygons.loc[tract_ids].geometry
    except KeyError:
        shape = polygons.loc[[t for t in tract_ids if t in polygons.index]].geometry

    bounds = shape.total_bounds
    geo_data = shape.__geo_interface__

    if use_city:
        tract_ids = city
        
    panel_data, table = get_panel_data('overview', tract_ids=tract_ids)
    return render_template('dashboard.html', tract_ids=tract_ids,
     geo_data=geo_data, bounds=bounds,
      panel_data=panel_data, table=table)


def make_single_line_census_data(row, columns):
    years = [int(column.split('-')[0]) for column in columns]
    values = [row[column] for column in columns]
    CIs = [row[column.replace('E', 'M').replace('P', 'M')] for column in columns]
    return years, values, CIs
    


colors = [
    '#0000FF',
    '#FF0000',
    '#00FF00',
    '#e6ff05',
    '#5200bd',
    '#ff8400',
    '#08c27e',
    '#bd006e'
]
def make_multi_line_census_data(row, columns, legend):
    xvals = sorted(list(set([column.split('-')[0] 
                         for column_set in columns
                 for column in column_set])))

    col_dicts = [
        OrderedDict({
            column.split('-')[0]: column for column in column_set
        }) for column_set in columns
    ]

    datasets =  [{
        'data': [row.get(column_set.get(xval, np.nan), None)
                 for xval in xvals],
        'label': legend_label,
        'fill': 'false',
        'borderColor': colors[ix]
    } for ix, (legend_label, column_set) in enumerate(zip(legend, col_dicts))]

    return datasets, xvals

def make_pie_data(row, columns):
    data = [row[c] for c in columns]
    background_colors = [colors[ix] for ix in range(len(columns))]
    return data, background_colors


def get_panel_data(tab, tract_ids):
    if isinstance(tract_ids, str): # If city
        row = agg.city_agg_df.loc[tract_ids].to_dict()
        tract_ids = [tract_ids]
    else:
        row = agg.aggregate_rows(tract_ids)
        
    table_dict = {'ID': tract_ids[0] if len(tract_ids) == 1 else hash(frozenset(tract_ids))}
    for table_name, column_name in overview.overview_table:
        table_dict[table_name] = round(row[column_name], 2)

    table = json2html.convert(json=table_dict,
            table_attributes="class=\"table table-bordered table-hover\"")

    if tab == 'overview':
        graphs = overview.overview_graphs
    elif tab == 'housing':
        graphs = housing.housing_graphs
    elif tab == 'demographics':
        graphs = demographics.demographics_graphs
    elif tab == 'economics':
        graphs = economics.economics_graphs

    # Collect data for panel graphs
    payload = {name: {} for name in graphs}
    for name, parameters in graphs.items():
        if parameters['type'] == 'census_single_line_CI':
            years, values, CIs = make_single_line_census_data(row,
                                                 parameters['columns'])

            payload[name]['data'] = values
            payload[name]['xvals'] = years
            payload[name]['CI'] = CIs


        elif parameters['type'] == 'multi_line':
            data, xvals = make_multi_line_census_data(row,
                                                 parameters['columns'],
                                                 parameters['legend'])
            payload[name]['data'] = data
            payload[name]['xvals'] = xvals
            payload[name]['legend'] = parameters['legend']

        elif parameters['type'] == 'pie':
            data, background_colors = make_pie_data(row, parameters['columns'])
            payload[name]['data'] = data
            payload[name]['colors'] = background_colors
            payload[name]['legend'] = parameters['legend']

        payload[name]['element'] = '#' + name
        payload[name]['plot_title'] = parameters['title']
        payload[name]['type'] = parameters['type']
    return payload, table

@product.route("/_render_panel")
def _render_panel():
    tab = request.args.get('tab')
    tract_ids = json.loads(request.args.get('tract_ids'))
    payload, _ = get_panel_data(tab, tract_ids)

    return render_template('graph_panel.html', panel_data=payload)


def get_dashboard_tab_table(tab):
    pass


@product.route("/city_select")
def city_select():
    return render_template('city_select.html', title='City Select')






@product.route("/make_info_table", methods=['GET', 'POST'])
def make_info_table():
    tract_ids = request.args.get('tract_ids').split(',')
    if tract_ids == ['']:
        city_id = request.args.get('city', 'nyc')
        area_values = agg.city_agg_df.loc[city_id].to_dict()
    else:
        area_values = agg.generate_info_table_data(tract_ids)

    table_string = []
    for display_name, column_name, c_type in agg.INFO_TABLE_COLUMNS:
        try:
            if c_type == 'int':
                v = str(int(area_values[column_name]))
            elif c_type == 'percent':
                v = '%s' % str(round(area_values[column_name], 1)) + '%'
            elif c_type == 'money':
                v = '$' + str(int(area_values[column_name]))
        except ValueError:
            v = 'N/A'

        table_string.append({
            '': display_name,
            'Value': v
        })

    table = json2html.convert(json=table_string,
            table_attributes="class=\"table table-bordered table-hover\"")
    return table



@product.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        flash('We appreciate your feedback!', 'success')
 
    return render_template('feedback.html', title='Feedback', form=form)
