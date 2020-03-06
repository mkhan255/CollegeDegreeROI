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


user = ''
password = ''
host = ''
port = ''
db = ''
url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
#connects to postgresql database using user credentials


con = create_engine(url)
#creates connection to database using sqlalchemy


tuition_query = 'SELECT * FROM tuition WHERE name IS NOT NULL 
                AND WHERE ("In District - Living on Campus" IS NOT NULL
                OR "In State - Living on Campus" IS NOT NULL
                OR "Out of State - Living on Campus" IS NOT NULL
                OR "In District - Living off Campus" IS NOT NULL
                OR "In State - Living off Campus" IS NOT NULL
                OR "Out of State - Living off Campus" IS NOT NULL 
                OR "In District - Living With Family" IS NOT NULL 
                OR "In State - Living With Family" IS NOT NULL
                OR "Out of State - Living With Family" IS NOT NULL)'
                #queries tuition table, and selects all rows where name is not a null value
                #and at least one value pertaining to in-school residency in not null
                 
tuition_df = pd.read_sql(tuition_query, con)
#saves tuition_query into a pandas dataframe


majors_query = 'SELECT major, wagp_2018 FROM income 
                WHERE major is NOT NULL 
                AND wagp_2018 is NOT NULL'
#queries income table and selects the major and wagp_2018 columns, excluding all null values

majors_income_df = pd.read_sql(majors_query, con)
#saves majors_query into a pandas dataframe 


app.layout = html.Div(className="my-app",children=[ 
#creates app layout using Dash HTML and CSS components
  
        html.Div(className="app-header", children=[
                        html.Div('Is Your Degree Worth It?')
                        #Dash HTML component that creates the title 
                
                        ], style={"display":"inline-block", "textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the title
        
        
        html.Div(className="college-names-dropdown",children=[
                        dcc.Dropdown(id='college-dd',
                        #creates searchable dropdown menu for college names
            
                        options=[{'label': k, 'value': k} for k in tuition_df['name'].unique()],
                        #inserts all unique colege names into dropdown from tuition_df dataframe
     
                        placeholder="Select Your College"),
                        #sets intial place holder in dropdown menu
                        
                        ], style={"textAlign":"center", "width":"100%"}),
                        #Dash CSS component the centers and sizes the dropdown menu
        
        
        html.Div(className="registration-dropdown", children=[
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
        
        
        html.Div(className="scholarships-input", children=[
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
                                    
                        dcc.Input(id="loan-term", type="number", style={"float" : "right"})]),
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
        
             [dash.dependencies.Input(component_id='college-dd', component_property='selected_college')])
              #calls college dropdown menu and user selected college
      
def set_residency_options(selected_college):
  #creates the options for the in-school reresidency dropdown menu 
        
              selected_college_df = tuition_df[tuition_df['name'] == selected_college]
               
              # matches selection from college-dd to the name column in the tuition_df dataframe, 
              # then stores all the information for just the selected college into new dataframe
        
              return[{'label': i, 'value': i} for i in selected_college_df.drop(['name'], axis=1)]
                
              '''Sets the values for in-school-residency-dd menu, excluding the name column.
              Beacuse in-school-residency-dd menu is dependent on college-dd menu, 
              this must happen in a callbacks opposed too when the in-school-residency-dd was initailly created'''

      
      
      
@app.callback(
              dash.dependencies.Output(component_id='majors-dd-output-container', component_property='children'),
              #stores the result of function output_income in majors-dd-output-container
  
              [dash.dependencies.Input(component_id='majors-dd', component_property='selected_major'),
     
              dash.dependencies.Input(component_id='button', component_property='n_clicks')]
              ) #

def output_income(selected_major, n_clicks):
  #outputs the average income for the selected colleg major if the submit button has been clicked
  
              sel_major_df = majors_income_df[majors_income_df['major'] == selected_major]
              # matches selection from majors-dd to the major column in the majors_income_df dataframe, 
              # then stores just the information for the selected major in a new datafram
    
              sel_major_income = (sel_major_df['wagp_2018'])
              #removes major column from dataframe and stores just the average income in new dataframe
    
              sel_major_income_list = (sel_major_income.values.tolist())
              #write sel_major_income value to a list to remove dataframe index from output
    
              string_income = str(sel_major_income_list)[1:-1]
              #store sel_major_income_list value as a string to remove brackets from output
    
              float_income = float(string_income)
              #takes string and stores it as a float
    
              final_income = "{:,}".format(float_income)
              #adds commas for user readability
    
    if n_clicks is None:
              raise PreventUpdate
              #prevents any output if button has not been clicked
    
    else:
              return 'The Average Income for Your Major is ${}'.format(final_income)
              #outputs message with final_income if button has been clicked
     
    
    
@app.callback(
    
              dash.dependencies.Output(component_id='degree-cost-container', component_property='children'),
              #stores the result of function output_income in degree-cost-ontainer
  
              [dash.dependencies.Input(component_id='college-dd', component_property='selected_college'),
              dash.dependencies.Input(component_id='in-school-residency-dd', component_property='selected_residency'),
              #calls college and in-school reresidency dropdown menus and the user selected options
     
              dash.dependencies.Input(component_id="loan-principal", component_property="principal_input"),
              dash.dependencies.Input(component_id="loan-interest", component_property="interest_input"),
              dash.dependencies.Input(component_id="loan-term", component_property="term_input"), 
              dash.dependencies.Input(component_id"scholarships", component_property="scholarships_input"),
              #calls loan principal, loan interest, loan term and scholarsip input feilds and input values
               
              dash.dependencies.Input(component_id='button', component_property='n_clicks')
              ])  #calls the submit button and th number of clicks it has recieved


def output_degree_cost(selected_country, selected_residency, principal_input, 
                      interest_input, term_input, scholarships_input, n_clicks):
  
              sel_college_tuition = tuition_df[tuition_df['name'] == selected_college]
              # matches selection from college-dd to the name column in the tuition_df dataframe, 
              # then stores just the information for the selected college in a new datafram
    
              sel_residency_tution = sel_college_tuition[selected_residency]
              # matches selection from in-school-residency-dd to the selected college, 
              # and stores the single tution value in a new dataframe
    
              sel_res_tution_list =  (sel_residency_tution.values.tolist())
              #write sel_residency_tution value to a list to remove dataframe index from output
        
              tuition_list = str(sel_res_tution_list)[1:-1]
              #store sel_res_tution_list value as a string to remove brackets from output
            
              tuition_float = float(tuition_list)
              #takes string and stores it as a float
              
              tuition_4 = tuition_float * 4
              #calculate estimated tuition over four years
    
              loan_principal = principal_input #store user input for loan principal in variable loan_principal
              apr = (interest_input / 100) / 12 
              #take interest_input percentage and divide by 100 for decimal value, then divide by 12 for monthly apr
              
              term = (term_input * 12) + 48
              #multiply term_input by 12 to get total number of months, 
              #add 48 with the assumption that the user is a freshman who will begin paying off the loan after graduation
              
              total_scholarships = scholarship_input 
              #store user input for scholarsips/grants in variable total_scholarships
              
              total_loan_cost = (loan_principal * apr * term) / (1 - (math.pow(( 1 + apr), (-term))))
              #formaula for calculating total loan cost
    
              degree_cost =  (tuition_4 - total_scholarships - loan_principal) + total_loan_cost
              #calculate total degree costs
        
              rounded_degree_cost = round(degree_cost, 2)
              #round degree_cost to 2 decimal points
            
              final_degree_cost = "{:,}".format(rounded_degree_cost)
              #adds commas for user readability
              
    if n_clicks is None:
            raise PreventUpdate
            #prevents any output if button has not been clicked
        
    else:
            return "The Estimated Total Cost of Your Degree is ${}".format(final_degree_cost)
            #outputs message with final_degree_cost if button has been clicked


