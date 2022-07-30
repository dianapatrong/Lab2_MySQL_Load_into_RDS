import boto3
from config import *
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(f"mysql://{mysql_db_user}:{mysql_db_pwd}@{mysql_db_host}:{mysql_db_port}/{mysql_db_name}")
conn = engine.connect()

# Reads from the dockerized mysql
df = pd.read_sql(sql="SELECT * FROM teams", con=conn)
print(df)

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

# Generates the signed IAM authentication token
token = client.generate_db_auth_token(DBHostname=pg_db_host, Port=pg_db_port, DBUsername=pg_db_user, Region=pg_db_region)

pg_engine = create_engine(f"postgresql+psycopg2://{pg_db_user}:{token}@{pg_db_host}:{pg_db_port}/{pg_db_name}")
conn = pg_engine.connect()

# Writes into AWS RDS instance
df.to_sql("teams", conn)