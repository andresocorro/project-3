import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import machineLearning

app.layout = html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Machine Learning", href="/apps/machineLearning")),
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
    brand="Stonks Market Analysis",
    brand_href="/",
    color="primary",
    dark=True,
),

     dcc.Location(id='url', refresh=False),
#     html.Div([
#         dcc.Link('Machine Learning |', href='/apps/machineLearning'),
#     ], className="row"),
     html.Div(id='page-content', children=[])
])

layout1 = html.Div([
    html.H1('Dashboard!', style={"textAlign": "center"})


])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layout1
    if pathname == '/apps/machineLearning':
        return machineLearning.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)