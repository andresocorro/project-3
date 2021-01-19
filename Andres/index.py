import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table 
import dash_table_experiments as dt
from dash.exceptions import PreventUpdate

import flask
from flask import Flask
import pandas as pd
import dateutil.relativedelta
from datetime import date
import datetime
import yfinance as yf
import numpy as np
import praw
import sqlite3

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash_utils import make_table, make_card, ticker_inputs, make_item
from reddit_data import get_reddit
from tweet_data import get_options_flow
from fin_report_data import get_financial_report #, get_financial_reportformatted


FL = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css"
# DL = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css"
conn = sqlite3.connect('stocks.sqlite')
server = Flask(__name__)
app = dash.Dash(__name__,server = server ,meta_tags=[{ "content": "width=device-width"}], external_stylesheets=[FL])

app.config.suppress_callback_exceptions = True

get_options_flow()
flow= pd.read_sql("select datetime, text from tweets order by datetime desc", conn)

global dfr 
dfr = get_reddit()
                
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Machine Learning", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Stonk Market Analysis",
    brand_href="#",
    color="primary",
    dark=True,
)

layout1 = html.Div([
        # html.Div(id = 'cards')
                navbar
                ,html.Br()
                ,html.Br()
                ,dbc.Row([dbc.Col(make_card("Search a stock", "primary", ticker_inputs('ticker-input', 'date-picker', 36)))])#row 1
                ,html.Br()
                ,dbc.Row([make_card("select ticker", "warning", "select ticker")],id = 'cards') #row 2 
                ,html.Br()
                ,dbc.Row([dbc.Col([make_card("Twitter Order Flow", "primary", make_table('table-sorting-filtering2', flow, '17px', 10))])
                        ,dbc.Col([make_card("Fin table ", "primary", html.Div(id="fin-table"))])
                        ])
                ,html.Br()
                ,dbc.Row([
                        dbc.Col([ 
                          dbc.Row([make_card("Wallstreet Bets New Posts", "primary"
                                             ,[html.P(html.Button('Refresh', id='refresh'))
                                               , make_table('table-sorting-filtering', dfr, '17px', 4)])
                                  ], justify = 'center')
                                ])

                        ,dbc.Col([dbc.Row([dbc.Alert("    Chart Visualization  ", color="primary")], justify = 'center')
                                ,dbc.Row(html.Div(id='x-vol-1'), justify = 'center')
                                #dcc.Graph(id = 'x-vol-1')
                                #,dbc.Row([dbc.Alert("place holder 5", color="primary")])
                                , dcc.Interval(
                                                id='interval-component',
                                                interval=1*150000, # in milliseconds
                                                n_intervals=0)   
                                , dcc.Interval(
                                                id='interval-component2',
                                                interval=1*60000, # in milliseconds
                                                n_intervals=0)      
                                ,dbc.Row([html.Div(id='tweets')])
                                ])#end col
                
                ])#end row 
                    
                    ]) #end div

app.layout= layout1


if __name__ == '__main__':
    app.run_server(debug = True)