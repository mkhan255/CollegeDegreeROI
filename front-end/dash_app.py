import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from sqlalchemy import create_engine, column, table
from sqlalchemy.dialects import postgresql

import math
import pandas as pd

from flask import Flask


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
#stylesheet for dropdowns and input fields


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#initializes dash app


user = '**********'
password = ''
host = '**********'
port = '5432'
db = '***********'
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
#connects to postgresql database using user credentials


con = create_engine(url)
#creates connection to database using sqlalchemy


tuition_query = 'SELECT * FROM tuition WHERE name IS NOT NULL 
                AND WHERE ("In District - Living on Campus"  
                OR "In State - Living on Campus" 
                OR "Out of State - Living on Campus" 
                OR "In District - Living off Campus" 
                OR "In State - Living off Campus" 
                OR "Out of State - Living off Campus"  
                OR "In District - Living With Family" 
                OR "In State - Living With Family" 
                OR "Out of State - Living With Family") IS NOT NULL'
                #queries 'tuition table, and selects all rows where name is not a null value
                #and at least one value pertaining to in-school residency in not null
                 
tuition_df = pd.read_sql(tuition_query, con)
#saves tuition_query into a pandas dataframe


majors_query = 'SELECT major, wagp_2018 FROM income WHERE major is NOT NULL AND wagp_2018 is NOT NULL'
#queries income table and selects the major and wagp_2018 columns, excluding all null values

majors_income_df = pd.read_sql(majors_query, con)
#saves majors_query into a pandas dataframe 


app.layout = html.Div(className="my-app",children=[ 
#creates app layout using Dash HTML and CSS components
  
        html.Div(
                className="app-header", children=[
                        html.Div('Is Your Degree Worth It?')
                        #Dash HTML component that creates the title 
                
                        ], style={"display":"inline-block", "textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the title
        
        
        html.Div
                (className="college-names-dropdown",children=[
                        dcc.Dropdown(id='college-dd',
                        #creates searchable dropdown menu for college names
            
                        options=[{'label': k, 'value': k} for k in tuition_df['name'].unique()],
                        #inserts all unique colege names into dropdown from tuition_df dataframe
     
                        placeholder="Select Your College"),
                        #sets intial place holder in dropdown menu
                        
                        ], style={"textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the dropdown menu
        
        
        html.Div
                (className="registration-dropdown", children=[
                        dcc.Dropdown(id='in-school-residency-dd', 
                        #creates searchable dropdown menu for student's in-school residency status
                                     
                        placeholder="Select Your in School Residency"),
                        #sets intial place holder in dropdown menu
                        
                        ], style={"textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the dropdown menu

        
        html.Div(className="majors-dropdown", children=[
                        dcc.Dropdown(id='majors-dd',
                        #creates searchable dropdown menu for college majors
                             
                        options=[{'label': i, 'value': i} for i in majors_income_df['major'].unique()],
                        #inserts all unique colege names into dropdown from majors_income_df dataframe
                  
                        placeholder="Select Your Major"),
                        #sets intial place holder in dropdown menu
                
                        ], style={"textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the dropdown menu
        
        
        html.Div(className="scholarship-input", children=[
        #contains code for scholarships/grants input
                
                        html.Label(["Enter Any Scholarships/Grants (4 Years) ",
                        #label for the input field
                             
                        dcc.Input(id="scholarships", type="number", style={"float" : "right"})]),
                        ]),  
                        #creates the input field, sets the datatype and positions the input field to the right of the label
        
        html.Div(className="loan-principal-input",children=[
        #contains code for student loan principal input     
                
                        html.Label(["Enter Loan Principal (4 years) ",
                        #label for the input field
                            
                        dcc.Input(id="loan-principal", type="number", style={"float" : "right"})]),
                        ]),
                        #creates the input field, sets the datatype and positions the input field to the right of the label
        
        html.Div(className="interest-input",children=[
        #contains code for loan interest rate input
                
                        html.Label(["Enter Average Interest Rate ",
                        #label for the input field
                            
                        dcc.Input(id="loan-interest", type="number", style={"float" : "right"})]),
                        ]),
                        #creates the input field, sets the datatype and positions the input field to the right of the label
                
        html.Div(className="loan-term-input", children=[
        #contains code for loan term input
                
                        html.Label(["Enter Loan Term ",
                        #label for the input field
                                    
                        dcc.Input(id="input-3", type="number", style={"float" : "right"})]),
                        ]),
                        #creates the input field, sets the datatype and positions the input field to the right of the label


        html.Div(className="submit-button",children=[
        #contains code for submit button
                
                        html.Button('Submit', id='button', style={"display" : "center"}),
                        ]),
                        #creates the submit button, creates the label, and centers the button

        html.Div(id="total-degree-cost"),
        #Dash HTML component that contains the total degree cost and will initiate an output when called

        html.Div(id='selected-major-income'),
        #Dash HTML component that contains the average income for a selected major and will initiate an output when called

]) #encases all code regarding app layout


@app.callback(
#Dash compenent directing all actions taken when users engage with specific app fields
        
        dash.dependencies.Output(component_id='in-school-residency-dd', component_property='options'),
        #stores the result of function set_residency_options in the in-school reresidency dropdown menu 
        
        [dash.dependencies.Input(component_id='college-dd', component_property='value')])
        #calls college dropdown menu and stores user selected value
      

def set_residency_options(selected_college):
        #function that creates the option for the in-school reresidency dropdown menu 
        
                select_college_df = tuition_df[tuition_df['name'] == selected_college]
               
                # matches selection from college-dd to the name column in the tuition_df dataframe, 
                # then stores all the information for the selected college from the tuition_df dataframe into new dataframe
        
                return[{'label': i, 'value': i} for i in select_college_df.drop(['name'], axis=1)]
                
                '''Sets the values for in-school-residency-dd menu, excluding the name column.
                Beacuse in-school-residency-dd menu is dependent on college-dd menu, 
                this must happen in a callbacks opposed too when the in-school-residency-dd was initailly created'''

@app.callback(
    dash.dependencies.Output(component_id='majors-dd-output-container', component_property='children'),
    [dash.dependencies.Input(component_id='majors-dd', component_property='value'),
     dash.dependencies.Input(component_id='button', component_property='n_clicks')]
    )

def update_output(selected_major, n_clicks):
    sel_major_df = majors_income_df[majors_income_df['major'] == selected_major]
    sel_major_income = (sel_major_df['wagp_2018'])
    
    sel_major_income_list =  (sel_major_income.values.tolist())
    string_income = str(sel_major_income_list)[1:-1]
    
    float_income = float(string_income)
    final_income = "{:,}".format(float_income)
    
    if n_clicks is None:
        raise PreventUpdate
    else:
        return 'The Average Income for Your Major is ${}'.format(final_income)

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


