# CollegeDegreeROI

Is your degree worth it? Have all the information, before registration!

## 1. Motivation

    Over 60% of new job openings will require a college degree , with collective student debt at over $1.6 trillion and fewer students attending college, it's important for families to know the true cost of a college degree. 
    My tool allows prospective college students to see how much it will cost to attend a specific college/university and how much they can expect to earn with their intended major. By providing information on their financial aid package and selecting their intended college and major, students are able to estimate out-of-pocket costs for tuition and fees. 
    Using 10 years of data collected by the Census Bureau, my project estimates the expected yearly income for over 160 college majors. 

## 2. Requirements

- Python3
- AWS CLI
- boto3

## 3. Architecture

Spark
4 EC2 m5ad.2xlarge instances (1 master 3 slaves spark cluster)

PostgreSQL
1 EC2 m5ad.xlarge instance

Dash
1 EC2 m5ad.large instance

## 4. DataSet

ACS PUMS https://www.census.gov/programs-surveys/acs/data/pums.html

IPEDS Dataset https://nces.ed.gov/ipeds/use-the-data

