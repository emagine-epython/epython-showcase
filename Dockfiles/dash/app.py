# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash_demo.server import app
import dash_demo.hist
import dash_demo.trading

server = app.server

app.layout = html.Div(
    dcc.Tabs([
        dcc.Tab(label='Trading', children=dash_demo.trading.layout),
        dcc.Tab(label='Historical', children=dash_demo.hist.layout)
        ])
    )

# This is used when not running inside gunicorn
if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8080
        )