import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
# from app import app
from app import app

import dateutil.relativedelta
from datetime import date

# Imports for Machine Learning
import numpy as np
from pmdarima.arima import AutoARIMA
from pmdarima.arima.utils import ndiffs
from tqdm.notebook import tqdm
from sklearn.metrics import mean_squared_error
import yfinance as yf
from statsmodels.tools.eval_measures import rmse
import statsmodels.api as sm
import itertools
from statsmodels.tsa.arima_model import ARIMA, ARMA
import warnings
warnings.filterwarnings("ignore")
import time


# This will create the card for ticker
def make_card(alert_message, color, style_dict={"textAlign": "center"}):
    return dbc.Card([ dbc.Alert(alert_message, color = color)], style = style_dict)

# children=html.Div(id='loading-output'

layout = html.Div([
    html.Br(),
    html.H1('Train your Model!', style={"textAlign": "center"}),
    html.Br(),
    dbc.Row([dbc.Col(make_card("Search for a stock to train", "primary"))]),
    html.Br(),
    html.Div([dcc.Input(id='input-box', placeholder='MSFT', type='text', style={"textAlign": "center"}),
    html.Br(),
    html.Br(),
    html.Div(html.Button('Train Model', id='button'), style={"textAlign": "center"}),
    html.Br(),
    dcc.Loading(id='loading-output', type='graph', fullscreen=True ,style={"textAlign": "center"})], style={"textAlign": "center"}),
    html.Br(),
    html.Div(id='projected-results', style={"textAlign": "center", 'marginLeft':'40%', 'marginRight':'40%','font-weight':'bold'}),
    html.Div(id='model-graph', style={"textAlign": "center", 'marginLeft':'15%', 'marginRight':'15%'}),
    html.Br(),
    html.Div(html.H4(id='model-summary-title', style={"textAlign": "center"})),
    html.Br(),
    html.Div(id='model-summary-0', style={"textAlign": "center",'marginLeft':'15%', 'marginRight':'15%'}),
    html.Br(),
    html.Div(id='model-summary-1', style={"textAlign": "center", 'whiteSpace': 'pre-wrap','marginLeft':'15%', 'marginRight':'15%'}),
])

@app.callback(
    [Output('model-graph', 'children'), 
        Output('model-summary-0', 'children'), 
        Output('model-summary-1', 'children'), 
        Output('loading-output', 'children'), 
        Output('model-summary-title', 'children'),
        Output('projected-results', 'children')],
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
    ticker = value.upper()
    df = yf.Ticker(ticker).history(period='Max')
    # df.reset_index(inplace=True)
    df = df.filter(['Close'])

    # Define the p, d and q parameters to take any value between 0 and 3
    d_value = ndiffs(df['Close'], test='adf')
    d = range(0,d_value+1)
    p = range(0,4)
    q = range(0,3)
    # p = d = q = range(0,3)
    # Generate all different combinations of p, q and q
    pdq = list(itertools.product(p, d, q))

    warnings.filterwarnings("ignore")
    aic= []
    parameters = []
    for param in pdq:
    #for param in pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(df, order=param, enforce_stationarity=True, enforce_invertibility=True)
            results = mod.fit()
            # save results in lists
            aic.append(results.aic)
            parameters.append(param)
            #seasonal_param.append(param_seasonal)
            # print('ARIMA{} - AIC:{}'.format(param, results.aic))
        except:
            continue
    # find lowest aic          
    index_min = min(range(len(aic)), key=aic.__getitem__)           

    print('The optimal model is: ARIMA{} -AIC{}'.format(parameters[index_min], aic[index_min]))

    model = ARIMA(df, order=parameters[index_min])
    model_fit = model.fit(disp=0)

    # Updating Indexed
    last_date = df.index[-1]
    days = 5
    for day in range(1, days+1):
        newEntry = last_date + pd.Timedelta(day, unit='D')
        forecastValue = model_fit.forecast(days)[0][day-1]
        dfSeries = df.append(pd.DataFrame({'Close': forecastValue}, index=[newEntry]))

    fig = go.Figure(data=[go.Scatter(x=dfSeries.index, y=dfSeries['Close'])])
    graph = dcc.Graph(figure=fig)

    # Print Summary for Website
    for i in range(2):
        if i == 0:
            html = model_fit.summary().tables[i].as_html()
            df_table = pd.read_html(html, header=0, index_col=0)[0]
            df_table = df_table.reset_index()
            # df_table = df_table.dropna
            table1 = dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
        else:
            html = model_fit.summary().tables[i].as_html()
            df_table = pd.read_html(html, header=0, index_col=0)[0]
            df_table = df_table.reset_index()
            table2 = dbc.Table.from_dataframe(df_table, striped=True, bordered=True, hover=True)
    
    # Create the forecasted values results to print
    days=[]
    predList = []
    for i in range(5):
        days.append(i+1)
        predValue = '$ ' + str(round(model_fit.forecast(5)[0][i],2))
        predList.append(predValue)

    df_pred_table = pd.DataFrame({'Number of Days in Future':days,
                    'Close Price': predList})

    table3 = dbc.Table.from_dataframe(df_pred_table, striped=True, bordered=True, hover=True, size='sm')

    empty_string = ''
    table_title = 'Arima Summary Results'
    return graph, table1, table2, empty_string, table_title, table3

