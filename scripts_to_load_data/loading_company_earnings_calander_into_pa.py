import csv
import requests
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)

db_name = os.getenv("PA_DB_NAME")
db_username = os.getenv("PA_DB_U")
db_password = os.getenv("PA_DB_PW")
db_host = os.getenv("PA_DB_URL")

av_key = os.getenv("AV_KEY")

con_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username,db_password,db_host,3306,db_name)
CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={}'.format(av_key)

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')

    my_list = list(cr)
    col = my_list[0]
del my_list[0]


df = pd.DataFrame(my_list,columns = col)

engine = create_engine(con_string)
df.to_sql(name = 'earnings_calander', con = engine, index=True, if_exists='replace' )

engine.dispose()
