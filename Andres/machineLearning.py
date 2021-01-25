import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from index import app

import dateutil.relativedelta
from datetime import date

# Imports for Machine Learning
import numpy as np
from pmdarima.arima import AutoARIMA
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
def make_card(alert_message, color, cardbody, style_dict={"textAlign": "center"}):
    return dbc.Card([ dbc.Alert(alert_message, color = color), dbc.CardBody(cardbody)], style = style_dict)

# Takes the input
def ticker_inputs(inputID):

    return html.Div([
        dcc.Input(id = inputID, type="text", placeholder="MSFT", style={"textAlign": "center"}),
        html.P(" "),
    ])

layout = html.Div([
    html.H1('Train your Model!', style={"textAlign": "center"}),
    html.Br(),
    html.Br(),
    dbc.Row([dbc.Col(make_card("Search for a stock to train", "primary", ticker_inputs('ticker-input')))]),
    html.Br(),
    html.Div(dcc.Input(id='input-box', placeholder='MSFT', type='text', style={"textAlign": "center"}), style={"textAlign": "center"}),
    html.Div(html.Button('Train Model', id='button'), style={"textAlign": "center"}),
    html.Div(id='output-container-button', children='Enter stock ticker and click submit', style={"textAlign": "center"}),
    html.Div(id='model-graph', style={"textAlign": "center"})
])

@app.callback(
    Output('model-graph', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, value):
    ticker = value.upper()
    df = yf.Ticker(ticker).history(period='Max')
    # df.reset_index(inplace=True)
    df = df.filter(['Close'])

    # Define the p, d and q parameters to take any value between 0 and 3
    p = d = q = range(0, 3)
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
    # Gives us next 5 days forecasted
    # graph = [round(model_fit.forecast(5)[0][0],2), round(model_fit.forecast(5)[0][1],2), round(model_fit.forecast(5)[0][2],2), round(model_fit.forecast(5)[0][3],2), round(model_fit.forecast(5)[0][4],2)]
    
    forecastValues = model_fit.forecast(5)[0]
    dfSeries = df['Close'].append(pd.Series(forecastValues), ignore_index=True)

    fig = go.Figure(data=[go.Scatter(x=dfSeries.index.to_list(), y=dfSeries.to_list())])
    graph = dcc.Graph(figure=fig)

    return graph


# @app.callback([Output('model-graph', 'children')], [Input('ticker-input', 'value')])
# def graph_model(ticker):
#     result = 'Your Model will be based on:' + ticker
#     return result







# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px
# import pandas as pd

# # from app import app

# layout = html.Div([
#     html.H1('Train your Model!', style={"textAlign": "center"})


# ])