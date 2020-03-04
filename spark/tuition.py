from db_connector import Database

from utils import config, s3, s3_resource, spark

from pyspark.sql import SQLContext
from pyspark.sql.types import *



def save_tuition()
        ipeds_bucket = config.get('AWS', 'ipeds_bucket')
        tuition_csv = config.get('AWS', 'tuition_csv')

        tuition_df = spark.read.csv("s3a://{}/{}".format(ipeds_bucket, tuition_csv) header='true', inferSchema='true')

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

        tuition_data = tuition_df.toDF(*new_column_name_list).drop("blank")

        db = db_connector()
        db.save(tuition_data, table='tuition')
