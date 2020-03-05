import files 
from db_connector import Database
from . import spark

from pyspark.sql import SQLContext
from pyspark.sql.types import *
import boto3
import * from files

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')



major_and_wage = []
#list containing names of college majors and their average income from 2009-2018, 
#after they have been concatinated and filtered


for f in filenames_a:
	csv_df_a = (spark.read.csv(f, header='true', inferSchema='true'))
	#for loop to read reads csv file from list containing first half of income data

		for f in filenames_b:
    		csv_df_b = (spark.read.csv(f, header='true', inferSchema='true'))
		#for loop to read reads csv file from list containing second half of income data
		
			concat = csv_df_a.union(csv_df_b)
			#concatinates the two resulting dataframes
			
			sorted_majors = concat.groupBy(concat.FOD1P).agg({'WAGP': 'avg'})
			# group by major and get the avg income, resulting in column named 'avg(WAGP)'
			
			for f in income_year:
 					avg_wage = sorted_majors.withColumnRenamed('avg(WAGP)', f) 
					#rename income column with names from list 'income_year'

    			 
					major_and_wage.append(avg_wage.withColumn(f, avg_wage[f].cast(IntegerType())))
					#make income into integer
					
major_and_wage_resuts = major_and_wage[0]
for df_next in major_and_wage[1:]:
    major_and_wage_resuts = major_and_wage_resuts.join(df_next,on='major',how='inner')
    #takes list of dataframes and joins them into one table

db = db_connector()
        db.save(major_and_wage_resuts, table='income')
	#calls db_connector function and writes table named 'income' to postgres database
	

