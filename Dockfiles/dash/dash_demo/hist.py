# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from plotly.data import iris

import kydb
from datetime import date
import pandas as pd
import plotly.express as px
from .server import app

DEFAULT_DATES = {
    'bitflyer': (date(2020, 6, 1), date(2020, 6, 4)),
    'fxcm': (date(2018, 6, 4), date(2018, 6, 6)),
    'ml': (date(2018, 6, 4), date(2018, 6, 6)),
}

tsdb = kydb.connect('dynamodb://epython/timeseries')

exchanges = [x[:-1] for x in tsdb.ls('/symbols/')]
exchange_dropdown = dcc.Dropdown(
    id='exchange-dropdown',
    options=[{'label': x, 'value': x} for x in exchanges],
    value='bitflyer'
)

    
exchange = 'bitflyer'
resolution_dropdown =  dcc.Dropdown(
        id='resolution-dropdown',
        value='minutely'
    )


symbols_dropdown = dcc.Dropdown(
    id='ts-symbol'
)

date_range = dcc.DatePickerRange(
        id='date-range',
        min_date_allowed=date(2016, 8, 5),
        max_date_allowed=date(2020, 9, 19),
    )
    
measures = dcc.Checklist(
    id='measures'
) 
    
            
layout =  html.Div([
    html.Div([
        exchange_dropdown,
        resolution_dropdown,
        symbols_dropdown,
        ], className='flex-row'),
    html.Div(date_range),
    html.Div([
        measures,
        dcc.Input(id='ts-path')
        ], className='flex-row'),
        
    html.Div(
            dcc.Loading(
                id="loading",
                type="default",
            children=html.Div(id="loading-output-1"))
        ),
        
    html.Div(dcc.Graph(
        id='curve-plot'
    ))
    ])
    
    
@app.callback(
    [
    Output('resolution-dropdown', 'options'),
    Output('resolution-dropdown', 'value'),
    Output('date-range', 'start_date'),
    Output('date-range', 'end_date'),
    ],
    Input('exchange-dropdown', 'value'))
def update_exchange(exchange):
    start_date, end_date = DEFAULT_DATES[exchange]
    resolutions = [x[:-1] for x in tsdb.ls('/symbols/' + exchange)]
    return ([{'label': x, 'value': x} for x in resolutions],
        resolutions[0], start_date, end_date)
    

@app.callback(
    [
    Output('ts-symbol', 'options'),
    Output('ts-symbol', 'value'),
    ],
    [
    Input('exchange-dropdown', 'value'),
    Input('resolution-dropdown', 'value')
    ])
def update_resolution(exchange, resolution):
    if not (exchange and resolution):
        return []
        
    symbols = tsdb.ls(f'/symbols/{exchange}/{resolution}')
    return [{'label': x, 'value': x} for x in symbols], symbols[0]
    
    
@app.callback(
    [
    Output('curve-plot', 'figure'),
    Output('measures', 'options'),
    Output("ts-path", "value"),
    Output("loading-output-1", "children")
    ],
    [
    Input('exchange-dropdown', 'value'),
    Input('resolution-dropdown', 'value'),
    Input('ts-symbol', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
    ])
def update_date_range(exchange, resolution, symbol, start_date, end_date):
    if not (resolution and start_date and end_date):
        return []
    path = f'/symbols/{exchange}/{resolution}/{symbol}'
    start_date = date(*[int(x) for x in start_date.split('-')])
    end_date = date(*[int(x) for x in end_date.split('-')])
    ts = tsdb[path]
    hist_data = ts.curve(start_date, end_date
        ).sort_index()
        
    measures = hist_data.columns
    measure_options = [{'label': x, 'value': x} for x in hist_data.columns]
    
    hist_data = pd.melt(hist_data.reset_index(),
        id_vars=['dt'],
        value_vars=list(hist_data.columns))
    
    fig = px.line(hist_data, x='dt', y='value', color='variable')
    
    return (fig, measure_options, path, None)