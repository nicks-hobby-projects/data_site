from yahoo_fin import stock_info
import time as t
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)
db_name = os.getenv("PA_DB_NAME")
db_username = os.getenv("PA_DB_U")
db_password = os.getenv("PA_DB_PW")
db_host = os.getenv("PA_DB_URL")
con_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username,db_password,db_host,3306,db_name)

sp500 = stock_info.get_data('^GSPC',start_date = "01/01/1980", end_date = "04/05/2022",index_as_date = False )
sp500 = sp500.drop_duplicates(subset = "date", keep = "last")
t.sleep(1)

dow = stock_info.get_data('^DJI',start_date = "01/01/1980", end_date = "04/05/2022",index_as_date = False)
dow = dow.drop_duplicates(subset = "date", keep = "last")
t.sleep(1)

nas = stock_info.get_data('^IXIC',start_date = "01/01/1980", end_date = "04/05/2022",index_as_date = False)
nas = nas.drop_duplicates(subset = "date", keep = "last")
t.sleep(1)

crude_oil = stock_info.get_data('CL=F',start_date = "01/01/1980", end_date = "04/05/2022",index_as_date = False)
crude_oil = crude_oil.drop_duplicates(subset = "date", keep = "last")
t.sleep(1)

engine = create_engine(con_string)
sp500.to_sql(name = 'gspc', con = engine, index=True, if_exists='replace' )
dow.to_sql(name = 'dji', con = engine, index=True, if_exists='replace' )
nas.to_sql(name = 'ixic', con = engine, index=True, if_exists='replace' )
crude_oil.to_sql(name = 'crude_oil', con = engine, index=True, if_exists='replace' )
engine.dispose()
