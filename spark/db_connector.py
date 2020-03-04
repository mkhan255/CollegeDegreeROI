from os.path import abspath
from configparser import ConfigParser

config = ConfigParser()
config.read(abspath('config.ini'))

class Database(object):

def __init__():
    username = config.get('PostgreSQL', 'username')
    password = config.get('PostgreSQL', 'password')
    instance = config.get('PostgreSQL', 'instance')
    database = config.get('PostgreSQL', 'database')
    url = 'jdbc:postgresql://{}:5432/{}'.format(instance, database)

def save(data, table, mode='append'):
    data.write.format('jdbc') \
    .option("url", url) \
    .option("dbtable",table) \
    .option("user", username) \
    .option("password",password) \
    .option("driver", "org.postgresql.Driver") \
    .mode(mode).save()
