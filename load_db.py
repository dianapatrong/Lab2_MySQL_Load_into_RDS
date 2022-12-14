import boto3
import config as conf
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f"mysql://{conf.mysql_user}:{conf.mysql_pwd}@{conf.mysql_host}:{conf.mysql_port}/{conf.mysql_name}")
conn = engine.connect()

# Reads from the dockerized mysql
df = pd.read_sql(sql="SELECT * FROM teams", con=conn)
print(df)

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

# Generates the signed IAM authentication token
token = client.generate_db_auth_token(DBHostname=conf.pg_host, Port=conf.pg_port, DBUsername=conf.pg_user, Region=conf.pg_region)

pg_engine = create_engine(f"postgresql+psycopg2://{conf.pg_user}:{token}@{conf.pg_host}:{conf.pg_port}/{conf.pg_name}")
conn = pg_engine.connect()

# Writes into AWS RDS instance
df.to_sql("teams", conn)