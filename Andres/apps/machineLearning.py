# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import dash_core_components as dcc
# import dash_html_components as html
# # from dash.dependencies import Input, Ouput
# import plotly.express as px
# import pandas as pd
# from dash_utils import make_table, make_card, ticker_inputs


# import numpy as np
# from pmdarima.arima import AutoARIMA
# import plotly.graph_objects as go
# from tqdm.notebook import tqdm
# from sklearn.metrics import mean_squared_error
# import yfinance as yf
# import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
# from statsmodels.tools.eval_measures import rmse
# import seaborn as sns
# import statsmodels.api as sm
# import itertools
# from statsmodels.tsa.arima_model import ARIMA, ARMA
# import warnings
# warnings.filterwarnings("ignore")

# # from index import app


# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Machine Learning", href="http://127.0.0.1:8050/ML")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True)
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="Stonks Market Analysis",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )

# layout = html.Div([
#         # html.Div(id = 'cards')
#                 navbar
#                 ,html.Br()
#                 ,html.Br()
#                 ,dbc.Row([dbc.Col(make_card("Train a stock!", "primary", ticker_inputs('ticker-input', 'date-picker', 36)))])#row 1
#                 ,html.Br()
#                 ,html.Br()
#                 ,dbc.Row([dbc.Col([dbc.Row([dbc.Alert("    Chart Visualization  ", color="primary")], justify = 'center')
#                                 ,dbc.Row(html.Div(id='x-vol-1'), justify = 'center')
#                                 #dcc.Graph(id = 'x-vol-1')
#                                 #,dbc.Row([dbc.Alert("place holder 5", color="primary")])
#                                 , dcc.Interval(
#                                                 id='interval-component',
#                                                 interval=1*150000, # in milliseconds
#                                                 n_intervals=0)   
#                                 , dcc.Interval(
#                                                 id='interval-component2',
#                                                 interval=1*60000, # in milliseconds
#                                                 n_intervals=0)      
#                                 ,dbc.Row([html.Div(id='tweets')])
#                                 ])#end col
#                         ,dbc.Col([make_card("Fin table ", "primary", html.Div(id="fin-table"))])
#                         ])
#                 ,html.Br()
#                 ,dcc.Location(id='url', refresh=False)
#                 ,html.Div(id='page-content', children=[])
# ]) #end div

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# from app import app

layout = html.Div([
    html.H1('Train your Model!', style={"textAlign": "center"})


])