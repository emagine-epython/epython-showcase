# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from plotly.data import iris

import kydb
from datetime import date
import pandas as pd
import plotly.express as px
from .server import app


tsdb = kydb.connect('dynamodb://epython/timeseries')
ts = tsdb['/symbols/fxcm/minutely/USDJPY']
hist_data = ts.curve(date(2018, 4, 8), date(2018, 4, 11))
hist_data.sort_index(inplace=True)

UNIT_QTY = [
    ('M', 1e6),
    ('k', 1e3),
    ('', 0),
]


FAKE_TRADES = [
    (1*60, 'John', 'USDJPY', 1.5 * 1e6),
    (3*60, 'Peter', 'USDJPY', 0.5 * 1e6),
    (5*60, 'Kanako', 'USDJPY', -1. * 1e6),
    (7*60, 'John', 'USDJPY', 0.1 * 1e6),
    (10*60, 'Peter', 'USDJPY', 1.5 * 1e6),
    (12*60, 'John', 'USDJPY', -1. * 1e6),
    (15*60, 'John', 'USDJPY', 0.3 * 1e6),
    (17*60, 'Kanako', 'USDJPY', 0.1 * 1e6),
    (21*60, 'John', 'USDJPY', 1.5 * 1e6),
    (25*60, 'Peter', 'USDJPY', 0.5 * 1e6),
    (29*60, 'John', 'USDJPY', -1. * 1e6),
]

def get_row(index, book, asset, qty):
    hist_row = hist_data.iloc[index]
    return (hist_row.name, book, asset, qty, abs(qty), hist_row.closeprice,
        'BUY' if qty > 0 else 'SELL')


trade_data = [get_row(*x) for x in FAKE_TRADES]
columns = ['dt', 'book', 'asset', 'qty', 'trade_size', 'price', 'trade_type']
trade_df = pd.DataFrame(trade_data, columns=columns)

flex_row_style = {
            'display': 'flex',
            'flex-direction': 'row'
        }
        
buy_sell_button_style = {
    'border-radius': '10px',
    'border': '2px solid orange',
    'font-size': '15pt',
    'margin': '5px',
    'padding': '5px 10px 5px 10px',
    'box-shadow': '2px 2px 4px 4px #888888'
}

layout = html.Div([
    dcc.Slider(
        id='trade-size-slider',
        min=100e3,
        max=2e6,
        step=100e3,
        value=100e3,
    ),
    html.Div([
        dcc.Input(id='trade-size',
            style={'font-size': '16pt', 'width': '75px'}),
        html.Button('Buy', id='buy', n_clicks=0,
            style={'background-color': 'green', **buy_sell_button_style}),
        html.Button('Sell', id='sell', n_clicks=0,
            style={'background-color': 'red', **buy_sell_button_style}),
    ], style=flex_row_style),
    html.Div(id='trade-msg'),
    html.Div([
        dcc.Graph(id='price-pos-plot')], style=flex_row_style),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        #interval=100000000, # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('trade-size', 'value'),
    Input('trade-size-slider', 'value'))
def update_trade_size(value):
    unit, qty = next((u, value / (q or 1)) for u, q in UNIT_QTY if value >= q)
    return f'{qty}{unit}'
    

@app.callback(Output('price-pos-plot', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_price_pos(n):
    period = 60 * 2 
    price_df = hist_data[:n+period]
    
    price_fig = px.line(hist_data, y='closeprice')
    scatter_df = trade_df[(trade_df.dt >= price_df.iloc[0].name) &
        (trade_df.dt <= price_df.iloc[-1].name)]
        
    if scatter_df.empty:
        return
    
    fig = px.scatter(scatter_df, x=scatter_df.dt, y=scatter_df.price, size='trade_size', color='trade_type')
    fig.add_scatter(x=price_df.index, y=price_df.closeprice, mode='lines',
        opacity=0.5, name='price')
    return fig
    
@app.callback(
    Output('trade-msg', 'children'),
    [
        Input('buy', 'n_clicks'),
        Input('sell', 'n_clicks')
    ],
    State('trade-size', 'value')
    )
def apply_trade(buy_clicks, sell_clicks, qty):
    if not qty:
        return
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'buy' in  changed_id:
        verb = 'Bought'
    else:
        verb = 'Sold'
    
    f_qty = next(float(qty[:-1]) * q if u else float(qty) for u, q in UNIT_QTY if qty.endswith(u))
    if not f_qty:
        return '0 quantity. Do nothing'

    return f'{verb} {qty}'
