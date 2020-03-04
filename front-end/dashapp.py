import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import math
import pandas as pd
from sqlalchemy import create_engine, column, table
from sqlalchemy.dialects import postgresql
from flask import Flask
from dash.exceptions import PreventUpdate

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

user = 'postgres'
password = ''
host = 'ec2-3-222-161-50.compute-1.amazonaws.com'
port = '5432'
db = 'college'
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

con = create_engine(url)

tuition_query = 'SELECT * FROM tuition WHERE name IS NOT NULL AND ("In District - Living on Campus" IS NOT NULL OR "In State - Living on Campus" IS NOT NULL O$

tuition_df = pd.read_sql(tuition_query, con)

majors_query = 'SELECT major, wagp_2018 FROM income1 WHERE major is NOT NULL AND wagp_2018 is NOT NULL'

majors_income_df = pd.read_sql(majors_query, con)

majors_list = majors_income_df['major'].unique()

app.layout = html.Div(className="my-app",
children=[

html.Div(
        className="app-header",
        children=[
            html.Div('Is Your Degree Worth It?')
        ], style={"display":"inline-block", "textAlign":"center", "width":"100%"}),

html.Div(className="college-names-dd",
children=[
    dcc.Dropdown(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in tuition_df['name'].unique()],
        placeholder="Select Your College"
),
], style={"display":"inline-block", "textAlign":"center", "width":"100%"}),

html.Div(className="registration-dd",
children=[
    dcc.Dropdown(id='cities-dropdown', placeholder="Select Your in School Residency"),
], style={"textAlign":"center", "width":"100%"}),

html.Div(className="majors-dd",
children=[
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in majors_list],
        placeholder="Select Your Major",
        )
], style={"textAlign":"center", "width":"100%"}),

html.Div(className="scholarship-input",
children=[
    html.Label(["Enter Any Scholarships/Grants (4 Years) ",
    dcc.Input(id="scholarships", type="number", style={"float" : "right"})]),
]),

html.Div(className="loan-amount-input",
children=[
    html.Label(["Enter Loan Principal (4 years) ",
    dcc.Input(id="input-1", type="number", style={"float" : "right"})]),
]),

html.Div(className="interest-input",
children=[
    html.Label(["Enter Average Interest Rate ",
    dcc.Input(id="input-2", type="number", style={"float" : "right"})]),
]),

html.Div(className="loan-term-input",
children=[
    html.Label(["Enter Loan Term ",
    dcc.Input(id="input-3", type="number", style={"float" : "right"})]),
]),


html.Div(className="submit-button",
children=[
html.Button('Submit', id='button', style={"display" : "center"}),

]),

html.Div(id="degree-cost"),

html.Div(id='majors-dd-output-container'),


])


@app.callback(
   dash.dependencies.Output(component_id='cities-dropdown', component_property='options'),
   [dash.dependencies.Input(component_id='countries-dropdown', component_property='value')]
)
def set_cities_options(selected_country):
    ddf = tuition_df[tuition_df['name'] == selected_country]
    return[{'label': i, 'value': i} for i in ddf.drop(['name'], axis=1)]

@app.callback(
    dash.dependencies.Output('degree-cost', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value'),
    dash.dependencies.Input('cities-dropdown', 'value'),
    dash.dependencies.Input("input-1", "value"),
    dash.dependencies.Input("input-2", "value"),
    dash.dependencies.Input("input-3", "value"), 
    dash.dependencies.Input("scholarships", "value"),
    dash.dependencies.Input(component_id='button', component_property='n_clicks')
])
def set_cities_value(selected_country, selected_city, input1, input2, input3, scholarships, n_clicks):
    dd1 = tuition_df[tuition_df['name'] == selected_country]
    dd2 = dd1[selected_city]
    p = input1
    r = (input2 / 100) / 12
    n = (input3 * 12) + 48
    s = scholarships
    y =  (dd2.values.tolist())
    z = str(y)[1:-1]
    tuition = float(z)
    tuition_4 = tuition * 4
    loancost = (r * p * n) / (1 - (math.pow(( 1 + r), (-n))))
    degree_cost =  (tuition_4 - s - p) + loancost
    rounded_degree_cost = round (degree_cost, 2)
    final_degree_cost = "{:,}".format(rounded_degree_cost)
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "The Estimated Total Cost of Your Degree is ${}".format(final_degree_cost)   
# return 'Your tuition is {}'.format(tuition_4)

@app.callback(
    dash.dependencies.Output('majors-dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value'),
     dash.dependencies.Input(component_id='button', component_property='n_clicks')
])
def update_output(value, n_clicks):
    ddf = majors_income_df[majors_list == value]
    x = (ddf['wagp_2018'])
    y =  (x.values.tolist())
    z = str(y)[1:-1]
    income = float(z)
    final_income = "{:,}".format(income)
    
    if n_clicks is None:
        raise PreventUpdate
    else:
        return 'The Average Income for Your Major is ${}'.format(final_income)
        
    if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80)
