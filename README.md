# Is your degree worth it? 

### Have all the information, before registration!

## 1. Motivation

        Over 60% of new job openings will require a college degree , with collective student 
    debt at over $1.6 trillion and fewer students attending college, it's important for 
    families to know the true cost of a college degree. 
    
        My tool allows prospective college students to see how much it will cost to attend a 
    specific college/university and how much they can expect to earn with their intended major. 
    By providing information on their financial aid package and selecting their intended college 
    and major, students are able to estimate out-of-pocket costs for  tuition and fees. 
    
        Using 10 years of data collected by the Census Bureau, my project estimates the expected 
    yearly income for over 160 college majors. 

## 2. Requirements

- Python3
- AWS CLI
- boto3

## 3. Architecture

Spark
- 4 EC2 m4.large instances (1 master 3 slaves spark cluster)

PostgreSQL
- 1 EC2 m4.large instance

Dash
- 1 EC2 t2.micro instance

## 4. DataSets

ACS PUMS: An annual survey administered by the US Cencus Bureau, 
contains over 200 columns including the average income for over 160 college majors.

https://www.census.gov/programs-surveys/acs/data/pums.html

IPEDS Dataset: Contains data on tution and fees for US colleges/universites

https://nces.ed.gov/ipeds/use-the-data

## 5. Methodology

- Use Spark to calculate average income by major from the ACS PUMS data set, join all the tables, 
and store data in Postgres database

- Use Spark to clean IPEDS Dataset and store data in Postgres database

- Use Dash to build front end and calculate the following based on user inputs:
       
        Total cost of a loan:
        principal + total interest over loan term 
        
        Cost of a four year degree at the selected college:
        (Tuition * 4) - Scholarship/grants - Loan principal  + Total cost of the loan

## 6. Outcome

The app is live and can be accessed at http://predictiveanalytics.me





