from db_connector import Database
from . import spark

from pyspark.sql import SQLContext
from pyspark.sql.types import *
import boto3

config = ConfigParser()
config.read(abspath('config.ini'))
#read configuration file

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
#uses boto3 to read from AWS S3


ipeds_bucket = config.get('AWS', 'ipeds_bucket')
tuition_csv = config.get('AWS', 'tuition_csv')
#retrieve data from S3 bucket
        
tuition_df = spark.read.csv("s3a://{}/{}".format(ipeds_bucket, tuition_csv) header='true', inferSchema='true')
#read the csv file and store it in a dataframe
        
new_column_name_list = ["unit_id",
                       "name",
                        "in-district living on campus", 
                        "in-state living on campus", 
                        "out-of-state living on campus", 
                        "in-district living off campus", 
                        "in-state living off campus", 
                        "out-of-state living off campus", 
                        "in-district living with family", 
                        "in-state living with family", 
                        "out-of-state living with family",
                        "blank"]
#re-write the colmun names into a more front-end friendly format

tuition_data = tuition_df.toDF(*new_column_name_list).drop("blank")
#save the dataframe with the new column names 

db = db_connector()
db.save(tuition_data, table='tuition')
#call the db_connector function and save the dataframe to the database in table named tuition
