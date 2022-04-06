from yahoo_fin import stock_info
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path("/home/justsomeguy/data_website_v2/.env")
load_dotenv(dotenv_path = dotenv_path)

now = datetime.now()
if now.hour in range(12,21):
    db_name = os.getenv("PA_DB_NAME")
    db_username = os.getenv("PA_DB_U")
    db_password = os.getenv("PA_DB_PW")
    db_host = os.getenv("PA_DB_URL")


    con_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_username,db_password,db_host,3306,db_name)

    def getting_biggest_gainers( now):
        gainers_df = stock_info.get_day_gainers()
        gainers_dict = gainers_df.to_dict(orient ='list')
        gainers_dict['date'] = []
        gainers_dict['type'] = []
        for g in gainers_dict['Symbol']:
            gainers_dict['type'].append('gainer')
            gainers_dict['date'].append(now)
        return gainers_dict

    def getting_biggest_losers( now):
        losers_df = stock_info.get_day_losers()
        losers_dict = losers_df.to_dict(orient ='list')
        losers_dict['date'] = []
        losers_dict['type'] = []
        for g in losers_dict['Symbol']:
            #print(g)
            losers_dict['type'].append('loser')
            losers_dict['date'].append(now)
        return losers_dict

    gainers_df = pd.DataFrame.from_dict(getting_biggest_gainers( now))
    losers_df = pd.DataFrame.from_dict(getting_biggest_losers(now))
    gainers_df = gainers_df.rename(columns = {'% Change':'change_per',
                                        'Symbol':'symbol',
                                        'Name':'name',
                                        'Price (Intraday)':'price_intra',
                                        'Change':'change',
                                        '% Change':'change_per',
                                        'Volume':'volume',
                                        'Avg Vol (3 month)':'avg_3m_vol',
                                        'Market Cap':'market_cap',
                                        'PE Ratio (TTM)':'pe'

                                            })
    losers_df = losers_df.rename(columns = {'% Change':'change_per',
                                        'Symbol':'symbol',
                                        'Name':'name',
                                        'Price (Intraday)':'price_intra',
                                        'Change':'change',
                                        '% Change':'change_per',
                                        'Volume':'volume',
                                        'Avg Vol (3 month)':'avg_3m_vol',
                                        'Market Cap':'market_cap',
                                        'PE Ratio (TTM)':'pe'

                                            })

    gainer_loser_df = gainers_df.append(losers_df)
    gainer_loser_df = gainer_loser_df.reset_index(drop = True)
    engine = create_engine(con_string)
    gainer_loser_df.to_sql(name = 'biggest_gainers_losers_daily', con = engine, index=True, if_exists='replace' )

    engine.dispose()
else:
    print("outside of hours")
