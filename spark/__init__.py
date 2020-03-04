# -*- coding: utf-8 -*-
from os.path import abspath
from configparser import ConfigParser
from pyspark.sql import SparkSession

# -- Load Configuration --
config = ConfigParser()
config.read(abspath('config.ini'))
jar_path = config.get('Jar', 'jar_path')

# -- Init Spark --
spark = SparkSession.builder.appName('college_roi').config("spark.jars", "{}/postgresql-42.2.9.jar".format(jar_path)).getOrCreate()

