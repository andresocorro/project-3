import dash

FL = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/flatly/bootstrap.min.css"

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}], external_stylesheets=[FL]
                )
server = app.server