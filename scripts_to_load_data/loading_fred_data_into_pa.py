from sqlalchemy import create_engine
import pymysql
import datapungi_fed as dpf
import pandas as pd
from datetime import date
import time as t
from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)

def get_fred_data(series,key):
    data = dpf.data(key)
    data = data.series(series)
    data = pd.DataFrame(data)
    data['vals'] = data[series]
    data['date_added'] = date.today()
    data = data.drop(columns=[series])
    data.to_sql(name = series.lower(), con = engine, index=True, if_exists='replace')
    t.sleep(1)
def get_fred_data_totalwealth(key):
    data = dpf.data(key)
    bottom50 = data.series('WFRBLB50107')
    t.sleep(1)
    t50to90 = data.series('WFRBLN40080')
    t.sleep(1)
    t90to99 = data.series('WFRBLN09053')
    t.sleep(1)
    top1 = data.series('WFRBLT01026')

    df = pd.merge(bottom50,t50to90, on=['date'])
    df =pd.merge(df,t90to99,on=['date'])
    df =pd.merge(df,top1,on=['date'])
    df['sum'] = df.agg('sum',1)
    df.columns = ['bot50','f50to90','f90to99','f99to100','sum']
    df['bot50_per'] = (df['bot50']/df['sum']).round(4)
    df['f50to90_per'] = (df['f50to90']/df['sum']).round(4)
    df['f90to99_per'] = (df['f90to99']/df['sum']).round(4)
    df['f99to100_per'] = (df['f99to100']/df['sum']).round(4)
    df['date_added'] = date.today()
    df.to_sql(name = 'total_wealth_dist', con = engine, index=True, if_exists='replace' )

key = os.getenv("FRED")
db_name = os.getenv("PA_DB_NAME")
db_username = os.getenv("PA_DB_U")
db_password = os.getenv("PA_DB_PW")
db_host = os.getenv("PA_DB_URL")

con_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username,db_password,db_host,3306,db_name)
engine = create_engine(con_string)
metrics = ['CPIAUCSL', 'UNRATE','DCOILWTICO', 'GDP', 'UMCSENT', 'MICH']
for m in metrics:
    get_fred_data(m,key)
get_fred_data_totalwealth(key)
engine.dispose()
print('done')
