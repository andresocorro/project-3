import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table 

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

def make_table(id, dataframe, lineHeight = '17px', page_size = 5):

    return dash_table.DataTable(
        id=id,
        css=[{'selector': '.row', 'rule': 'margin: 0'}],
        columns=[
            {"name": i, "id": i} for i in dataframe.columns
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'},
        style_cell={'textAlign': 'left'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': lineHeight
              },
        # style_table = {'width':300},
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
          ],
        style_cell_conditional=[
           {'if': {'column_id': 'title'},
           'width': '130px'},
           {'if': {'column_id': 'post'},
           'width': '500px'},
           {'if': {'column_id': 'datetime'},
           'width': '130px'},
           {'if': {'column_id': 'text'},
           'width': '500px'}],
        page_current=0,
        page_size=page_size,
        page_action='custom',

        filter_action='custom',
        filter_query='',

        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        #dataframe.to_dict('records')    

    )