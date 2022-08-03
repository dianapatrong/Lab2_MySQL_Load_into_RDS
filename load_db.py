import boto3
import config as conf
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f"mysql://{conf.mysql_db_user}:{conf.mysql_db_pwd}@{conf.mysql_db_host}:{conf.mysql_db_port}/{conf.mysql_db_name}")
conn = engine.connect()

# Reads from the dockerized mysql
df = pd.read_sql(sql="SELECT * FROM teams", con=conn)
print(df)

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

# Generates the signed IAM authentication token
token = client.generate_db_auth_token(DBHostname=conf.pg_db_host, Port=conf.pg_db_port, DBUsername=conf.pg_db_user, Region=conf.pg_db_region)

pg_engine = create_engine(f"postgresql+psycopg2://{conf.pg_db_user}:{token}@{conf.pg_db_host}:{conf.pg_db_port}/{conf.pg_db_name}")
conn = pg_engine.connect()

# Writes into AWS RDS instance
df.to_sql("teams", conn)