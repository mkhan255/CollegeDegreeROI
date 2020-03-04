import files
rom db_connector import Database
# initializes spark session locally, should import __init__.py instead
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)

from pyspark.sql import SQLContext
from pyspark.sql.types import *
import boto3
import * from files

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')



major_and_wage = []


for f in filenames_a:
	csv_df_a = (spark.read.csv(f, header='true', inferSchema='true'))

		for f in filenames_b:
    		csv_df_b = (spark.read.csv(f, header='true', inferSchema='true'))

			concat = csv_df_a.union(csv_df_b)

			sorted_majors = concat.groupBy(concat.FOD1P).agg({'WAGP': 'avg'})# group by major and get the avg income

			for f in income_year:
 					avg_wage = sorted_majors.withColumnRenamed('avg(WAGP)', f) #rename income column, must rename before making into int, or will take avg() as function

    			 #make income into int
					major_and_wage.append(avg_wage.withColumn(f, avg_wage[f].cast(IntegerType())))

major_and_wage_resuts = major_and_wage[0]
for df_next in major_and_wage[1:]:
    major_and_wage_resuts = major_and_wage_resuts.join(df_next,on='major',how='inner')

db = db_connector()
        db.save(tuition_data, table='income')

