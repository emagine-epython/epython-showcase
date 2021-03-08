# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import redis
from dash.dependencies import Output, Input, State
from plotly.data import iris

import kydb
import pickle
from datetime import date
import pandas as pd
from .server import app
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


tsdb = kydb.connect('dynamodb://epython/timeseries')
ts = tsdb['/symbols/fxcm/minutely/USDJPY']
hist_data = ts.curve(date(2018, 4, 8), date(2018, 4, 11))
hist_data.sort_index(inplace=True)

db = kydb.connect('dynamodb://epython')
config = db['/demos/epython-dash-demo/config']

host = config.get('REDIS_HOST', '127.0.0.1')
port = config.get('REDIS_PORT', '6379')
redis_conn = redis.Redis(host=host, port=port)

UNIT_QTY = [
    ('M', 1e6),
    ('k', 1e3),
    ('', 0),
]

trades_df = None

layout = html.Div([
    dcc.Slider(
        id='trade-size-slider',
        min=100e3,
        max=2e6,
        step=100e3,
        value=100e3,
    ),
    html.Div([
        dcc.Input(id='book', value='Book1'),
        dcc.Input(id='trade-size',
                  style={'font-size': '16pt', 'width': '75px'}),
        html.Button('Buy', id='buy-button', n_clicks=0,
                    className='buy-sell-button'),
        html.Button('Sell', id='sell-button', n_clicks=0,
                    className='buy-sell-button'),
    ]),
    html.Div(id='trade-msg'),
    html.Div([
        dcc.Graph(id='price-pos-plot'),
        dash_table.DataTable(id='trade-table')
    ], className='flex-row'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    ),
    # hidden signal value
    html.Div(id='tick-signal', style={'display': 'none'}),
    html.Div(id='trade-signal', style={'display': 'none'})
])


@app.callback(
    Output('trade-size', 'value'),
    Input('trade-size-slider', 'value'))
def update_trade_size(value):
    unit, qty = next((u, value / (q or 1)) for u, q in UNIT_QTY if value >= q)
    return f'{qty}{unit}'


@app.callback(
    Output('tick-signal', 'children'),
    Input('interval-component', 'n_intervals'),
    State('tick-signal', 'children')
)
def compute_value(n, prev_tick):
    tick = redis_conn.get('tick')

    if tick is None:
        raise PreventUpdate

    tick = int(tick)
    if prev_tick == tick:
        raise PreventUpdate

    return tick


@app.callback(
    Output('trade-signal', 'children'),
    Input('interval-component', 'n_intervals'),
)
def check_new_trades(n):
    global trades_df
    prev_len = 0 if trades_df is None else trades_df.shape[0]

    num_trades = int(redis_conn.llen('trades'))
    if num_trades and prev_len == num_trades:
        raise PreventUpdate

    trades = [pickle.loads(x) for x in redis_conn.lrange('trades', 0, -1)]

    if not trades:
        trades_df = None
        raise PreventUpdate

    def get_row(dt, book, asset, qty):
        hist_row = hist_data.loc[dt]
        return (hist_row.name, book, asset, qty, hist_row.closeprice)

    trade_data = [get_row(*x) for x in trades]
    columns = ['dt', 'book', 'asset', 'qty', 'price']
    trades_df = pd.DataFrame(trade_data, columns=columns).sort_values('dt')

    return n


@app.callback(
    [
        Output('trade-table', 'columns'),
        Output('trade-table', 'data'),
    ],
    Input('tick-signal', 'children')
)
def update_trade_table(trade):
    if trades_df is None:
        raise PreventUpdate

    columns=[{"name": i, "id": i} for i in trades_df.columns]
    data = trades_df.to_dict('records')
    return columns, data
    
@app.callback(
    Output('price-pos-plot', 'figure'),
    Input('tick-signal', 'children')
)
def update_price_pos(n):
    if trades_df is None:
        raise PreventUpdate

    price_df = hist_data[:n]

    scatter_df = trades_df[(trades_df.dt >= price_df.iloc[0].name) &
                           (trades_df.dt <= price_df.iloc[-1].name)]

    if scatter_df.empty:
        return
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
        specs=[[{"secondary_y": True}], [{}]])
        
    # Price
    fig.add_trace(
        go.Scatter(x=price_df.index, y=price_df.closeprice, name="Price",
            line={
                'color': 'grey'
            }),
        secondary_y=False,
    )
    
    largest_trade = scatter_df.qty.abs().max()

    # Trades
    for trade_type, direction in [('Buy', 1), ('Sell', -1)]: 
        trade_plot = scatter_df[scatter_df.qty * direction > 0]
        is_buy = trade_type == 'Buy'
        fig.add_trace(
            go.Scatter(x=trade_plot.dt, y=trade_plot.price, name=trade_type,
                mode='markers',
                marker=dict(
                    color='Green' if is_buy else 'Red',
                    line=dict(
                        color='Black',
                        width=2
                    )
                ),
                marker_size=np.log(trade_plot.qty.abs() / largest_trade + 1) * 25,
                marker_symbol=['triangle-' + ('up' if is_buy else 'down')] * scatter_df.shape[0]
            ),
            secondary_y=False,
        )
    
    
    # Position
    pos_df = scatter_df[['dt', 'qty']]
    pos_df = pd.concat([
        pd.DataFrame([(price_df.index[0], 0)], columns=pos_df.columns),
        pos_df,
        pd.DataFrame([(price_df.index[-1], 0)], columns=pos_df.columns)
        ])
    pos_df['position'] = pos_df.qty.cumsum()
    
    # PNL
    fig.add_trace(
        go.Scatter(x=pos_df.dt, y=pos_df.position, name="Position",
            line={ "shape": 'hv'},
            mode='lines'),
        secondary_y=True,
    )
    
    pnl_df = pos_df.set_index('dt')
    pnl_df = price_df.join(pnl_df).fillna(0.).copy()
    pnl_df['position'] = pnl_df.qty.cumsum()
    pnl_df['prev_pos'] = pnl_df.position.shift()
    pnl_df['prev_price'] = pnl_df.closeprice.shift()
    i0 = pnl_df.index[0]
    i1 = pnl_df.index[1]
    pnl_df.loc[i0, 'prev_pos'] = 0.
    pnl_df.loc[i0, 'prev_price'] = pnl_df.loc[i1, 'closeprice']
    pnl_df['pnl'] = pnl_df.prev_pos * (pnl_df.closeprice - pnl_df.prev_price)
    
    
    fig.add_trace(
        go.Scatter(x=pnl_df.index, y=pnl_df.pnl.cumsum(), name="PNL"),
        row=2, col=1
    )
    
    
    # Add figure title
    fig.update_layout(
        title_text="Price Trade Position"
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="Date/Time")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="Position", secondary_y=True)
    return fig


@app.callback(
    Output('trade-msg', 'children'),
    [
        Input('buy-button', 'n_clicks'),
        Input('sell-button', 'n_clicks')
    ],
    [
        State('book', 'value'),
        State('trade-size', 'value'),
        State('tick-signal', 'children')
    ]
)
def apply_trade(buy_clicks, sell_clicks, book, qty, n):
    if not qty:
        return

    if not book:
        return 'Book not defined. Do nothing'

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    f_qty = next(float(qty[:-1]) * q if u else float(qty)
                 for u, q in UNIT_QTY if qty.endswith(u))
    if not f_qty:
        return '0 quantity. Do nothing'

    if 'buy' in changed_id:
        verb = 'Bought'
    else:
        verb = 'Sold'
        f_qty *= -1

    dt = hist_data.index[n]
    trade = (dt, book, 'USDJPY', f_qty)
    redis_conn.lpush('trades', pickle.dumps(trade))
    return f'{verb} {qty}'
