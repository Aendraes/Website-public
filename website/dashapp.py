import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


def create_dash_app(flask_app):
    dash_app = dash.Dash(server=flask_app,name="Dashboard", url_base_pathname="/Workoutdash/")

    dash_app.layout = html.Div(
        children=[
            html.H1(children="Hello dash!"),
            html.Div(
                children = """
                Dash: a web application framework
                """
            ),
            dcc.Graph(
                id="Workout-graph",
                figure=px.bar(x=[1,2,3,4,5], y=[1,2,3,4,5])
            )
        ]
    )





















    return dash_app