from yahoo_fin import stock_info
import time as t
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from sqlalchemy.orm import sessionmaker
import models
from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)

now = datetime.now()
now = now - timedelta(hours=5)
print(now.weekday())

if now.weekday() in [0,1,2,3,4]:
    tommorow = now + timedelta(days=1)
    end_dt = tommorow.strftime('%m/%d/%Y')

    print('end date:', end_dt)
    now_dt_string = now.strftime('%m/%d/%Y')

    db_name = os.getenv("PA_DB_NAME")
    db_username = os.getenv("PA_DB_U")
    db_password = os.getenv("PA_DB_PW")
    db_host = os.getenv("PA_DB_URL")
    con_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username,db_password,db_host,3306,db_name)
    engine = create_engine(con_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    dji_results = session.query(models.DJI).order_by(models.DJI.date.desc()).first()
    ixic_results = session.query(models.IXIC).order_by(models.IXIC.date.desc()).first()
    gspc_results = session.query(models.GSPC).order_by(models.GSPC.date.desc()).first()
    crude_oil_results = session.query(models.CRUDE_OIL).order_by(models.CRUDE_OIL.date.desc()).first()

    max_dji = dji_results.date
    max_ixic = ixic_results.date
    max_gspc = gspc_results.date
    max_crude_oil = crude_oil_results.date

    dji_date_list=[]
    ixic_date_list=[]
    gspc_date_list=[]
    crude_oil_date_list=[]

    dji_results = session.query(models.DJI).order_by(models.DJI.date.desc()).all()
    ixic_results = session.query(models.IXIC).order_by(models.IXIC.date.desc()).all()
    gspc_results = session.query(models.GSPC).order_by(models.GSPC.date.desc()).all()
    crude_oil_results = session.query(models.CRUDE_OIL).order_by(models.CRUDE_OIL.date.desc()).all()

    for x in dji_results:
        dji_date_list.append(x.date)

    for x in ixic_results:
        ixic_date_list.append(x.date)

    for x in gspc_date_list:
        gspc_date_list.append(x.date)

    for x in crude_oil_date_list:
        crude_oil_date_list.append(x.date)

    session.commit()
    session.close()
    engine.dispose()

    max_dji = max_dji + timedelta(days=1)
    max_ixic = max_ixic + timedelta(days=1)
    max_gspc = max_gspc + timedelta(days=1)
    max_crude_oil = max_crude_oil + timedelta(days=1)

    max_dji_str = max_dji.strftime('%m/%d/%Y')
    max_ixic_str = max_ixic.strftime('%m/%d/%Y')
    max_gspc_str = max_gspc.strftime('%m/%d/%Y')
    max_crude_oil_str =  max_crude_oil.strftime('%m/%d/%Y')

    print('dow date: ',max_dji_str)
    print('nasdaq date: ',max_ixic_str)
    print('sp500 date: ',max_gspc_str)
    engine = create_engine(con_string)
    if max_dji < now:
        try:
            dow = stock_info.get_data('^DJI',start_date = max_dji_str, end_date = end_dt,index_as_date = False)
            dow = dow.drop_duplicates(subset = "date", keep = "last")
            dow = dow[~dow['date'].isin( dji_date_list)]
            num_rows = len(dow.index)
            print(dow)
            if num_rows > 0:
                dow.to_sql(name = 'dji', con = engine, index=True, if_exists='append' )
                print('updating_dow')
            t.sleep(1)
        except:
            print('problem updating dow')
            pass
        print('dow updated')
    else:
        print("dow up to date")
    if max_ixic < now:
        try:
            nas = stock_info.get_data('^IXIC',start_date = max_ixic_str, end_date = end_dt,index_as_date = False)
            nas = nas.drop_duplicates(subset = "date", keep = "last")
            nas = nas[~nas['date'].isin( ixic_date_list)]
            num_rows = len(nas.index)
            if num_rows > 0:
                nas.to_sql(name = 'ixic', con = engine, index=True, if_exists='append' )
                print('updating nasdaq')
            t.sleep(1)
        except:
            print('problem updating nasdaq')
            pass
        print('nasdaq updated')
    else:
        print("nasdaq up to date")
    if max_gspc < now:
        try:
            sp500 = stock_info.get_data('^GSPC',start_date = max_gspc_str, end_date = end_dt,index_as_date = False)
            sp500 = sp500.drop_duplicates(subset = "date", keep = "last")
            sp500 = sp500[~sp500['date'].isin( gspc_date_list)]
            num_rows = len(sp500.index)
            if num_rows > 0:
                sp500.to_sql(name = 'gspc', con = engine, index=True, if_exists='append' )
                print('updating sp500')
            t.sleep(1)
        except:
            print('problem updating sp500')
            pass
        print('sp500 updated')
    else:
        print("sp500 up to date")
    if max_crude_oil < now:
        try:
            crude_oil = stock_info.get_data('CL=F',start_date = max_dji_str, end_date = end_dt,index_as_date = False)
            crude_oil = crude_oil.drop_duplicates(subset = "date", keep = "last")
            crude_oil = crude_oil[~crude_oil['date'].isin( crude_oil_date_list)]
            num_rows = len(crude_oil.index)
            if num_rows > 0:
                crude_oil.to_sql(name = 'crude_oil', con = engine, index=True, if_exists='append' )
                print('updating crude oil')
            t.sleep(1)
        except:
            print('problem updating crude oil')
            pass
        print('crude oil updated')
    else:
        print("crude oil up to date")
    engine.dispose()
else:
    print('weekend')
