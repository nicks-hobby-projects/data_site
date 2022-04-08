from data_site import db
from data_site.models import *
import pandas as pd
from datetime import datetime
from datetime import date
from sqlalchemy import func
import requests
import os
import json as j
class functs():
    #displaying live prices of stocks on home page
    def getting_current_index_values(s):
        from yahoo_fin import stock_info
        try:
            current_value = stock_info.get_live_price(s)
        except:
            current_value = 0
        return(current_value)

    def getting_prev_close_value_for_index(mod):
        result = mod.query.order_by(mod.date.desc()).first()
        close = result.adjclose
        return close

    #getting nasa picture of the day
    def getting_nasa_apod():
        import requests as r
        import json as j
        key = os.getenv('NASA_API_KEY')
        url = "https://api.nasa.gov/planetary/apod?api_key={}&thumbs=True".format(key)
        img_dict = r.get(url)
        img_dict = j.loads(img_dict.text)
        try:
            img_dict['url_for_pic'] = img_dict['thumbnail_url']
        except:
            img_dict['url_for_pic'] = img_dict['url']
        return(img_dict)

    #making stock market charts for indexes. this uses a model as one of the variables
    def making_stock_charts(mod,sym,y):
        import plotly
        import plotly.express as px
        results = mod.query.order_by(mod.date.desc()).all()
        result_dict = {'date':[],
               'adjclose':[]
               }

        for r in results:
            result_dict['date'].append(r.date)
            result_dict['adjclose'].append(r.adjclose)
        result_df = pd.DataFrame.from_dict(result_dict)
        fig = px.line(result_df, x='date', y='adjclose',
                        labels = {'date':'Date',
                                 'adjclose':y},
                        title = sym,
                        template = 'plotly_dark')
        fig.update_xaxes(rangeslider_visible=True)
        graphJSON = j.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    def getting_gdp_graph():
        import plotly
        import plotly.express as px
        results = GDP.query.order_by(GDP.date.desc()).all()
        result_dict = {'date':[],
                        'vals':[]}
        for r in results:
            result_dict['date'].append(r.date)
            result_dict['vals'].append(r.vals)
        result_df = pd.DataFrame.from_dict(result_dict)
        fig = px.line(result_df, x='date', y='vals',
                        labels = {'date':'Quarter',
                                 'vals':'GDP'},
                        title = 'Gross Domestic Product',
                        template = 'plotly_dark')
        fig.update_xaxes(rangeslider_visible=True)
        graphJSON = j.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def getting_cpi_graph():
        import plotly
        import plotly.express as px
        results = CPIAUCSL.query.order_by(CPIAUCSL.date.desc()).all()
        result_dict = {'date':[],
                        'vals':[]}
        for r in results:
            result_dict['date'].append(r.date)
            result_dict['vals'].append(r.vals)
        result_df = pd.DataFrame.from_dict(result_dict)
        fig = px.line(result_df, x='date', y='vals',
                        labels = {'date':'Date',
                                 'vals':'CPIAUCSL'},
                        title = 'Consumer Price Index',
                        template = 'plotly_dark')
        fig.update_xaxes(rangeslider_visible=True)
        graphJSON = j.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def making_total_wealth_pie_cahrt():
        import plotly
        import plotly.express as px

        table_name = "TOTAL_WEALTH_DIST".lower()
        results = TOTAL_WEALTH_DIST.query.order_by(TOTAL_WEALTH_DIST.date.desc()).first()
        data = []
        head = []
        data.append(results.bot50)
        data.append(results.f50to90)
        data.append(results.f90to99)
        data.append(results.f99to100)

        head.append('Bottom 50')
        head.append('50 to 90')
        head.append('90 to 99')
        head.append('99 to 100')

        result_df = pd.DataFrame({'Percentage':data,
                                'header':head
                                })
        fig = px.pie(result_df,
        values = 'Percentage',
        names = 'header',
        title = "Total Wealth Distribution",
        template = 'plotly_dark'
        )
        graphJSON = j.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    #geting top values from some of the ecomic data tables to display on the econ page
    def geting_top_table_vals():
        n = []
        x = CPIAUCSL.query.order_by(CPIAUCSL.date.desc()).first().vals
        n.append(x)
        x = UNRATE.query.order_by(UNRATE.date.desc()).first().vals
        n.append(x)
        x = GDP.query.order_by(GDP.date.desc()).first().vals
        n.append(x)
        return(n)
    #geting values for the charts on the economic page
    def getting_values_for_charts_econ():

        table_dict = {"CPIAUCSL":'Consumer Price Index'
                        ,"UNRATE":'Unemployment Rate'
                        ,"GDP":'Gross Domestic Product'
                        ,"MICH":'Inflation Expectation'
                        }
        chart_dict = {}
        for k in table_dict:
            table_name = k
            data = pd.read_sql_table(table_name.lower(), con=db.engine)
            data['date'] = data['date'].dt.date
            data['date_added'] = data['date_added'].dt.date
            data = data.loc[data['date'] >= datetime.strptime('1990/01/01','%Y/%m/%d').date()]
            legend = table_dict[k]
            var_dict = data.to_dict(orient='list')
            var_dict['legend'] = legend
            chart_dict[k] = var_dict

        return chart_dict
    #getting data to make the pie chart on the econ page
    def getting_total_wealth_info():
        table_name = "TOTAL_WEALTH_DIST".lower()
        results = TOTAL_WEALTH_DIST.query.order_by(TOTAL_WEALTH_DIST.date.desc()).first()
        data = []
        data.append(results.bot50)
        data.append(results.f50to90)
        data.append(results.f90to99)
        data.append(results.f99to100)
        tot_w_legend = 'Total Wealth Distribution'
        tot_w_labels = ['bottom 50%','50% to 90%','90% to 99%','99% to 100%']
        tot_w_values = data

        return[tot_w_legend,tot_w_labels,tot_w_values]
    #getting ticker quote info
    def getting_ticker_current_quote(sym):
        from yahoo_fin import stock_info
        try:
            s = sym.upper()
            quote = stock_info.get_quote_table(sym)
        except:
            quote = {'52 Week Range': '',
             'Ask': '',
             'Avg. Volume': '',
             'Beta (5Y Monthly)': '',
             'Bid': '',
             "Day's Range": '',
             'Expense Ratio (net)': '',
             'NAV': '',
             'Net Assets': '',
             'Open': '',
             'PE Ratio (TTM)': '',
             'Previous Close': '',
             'Quote Price': '',
             'Volume': '',
             'YTD Daily Total Return': '',
             'Yield': ''}
        return quote
    #getting the info from the gainer and loser table in mysql
    def getting_daily_gainers_and_losers():
        gainers_dict = {'symbol':[],
                        'name':[],
                        'price_intra':[],
                        'change_per':[],
                        'date':[]}
        losers_dict = {'index':[],
                'symbol':[],
                'name':[],
                'price_intra':[],
                'change_per':[],
                'date':[]}
        gainer_results = BIGGEST_GAINERS_LOSERS_DAILY.query.filter_by(type = 'gainer').order_by(BIGGEST_GAINERS_LOSERS_DAILY.change_per.asc()).all()
        loser_results = BIGGEST_GAINERS_LOSERS_DAILY.query.filter_by(type = 'loser').order_by(BIGGEST_GAINERS_LOSERS_DAILY.change_per.desc()).all()
        for r in gainer_results:
            gainers_dict['symbol'].append(r.symbol)
            gainers_dict['name'].append(r.name)
            gainers_dict['price_intra'].append(r.price_intra)
            gainers_dict['change_per'].append(r.change_per)
            gainers_dict['date'].append(r.date)
        for r in loser_results:
            losers_dict['symbol'].append(r.symbol)
            losers_dict['name'].append(r.name)
            losers_dict['price_intra'].append(r.price_intra)
            losers_dict['change_per'].append(r.change_per)
            losers_dict['date'].append(r.date)
        return [gainers_dict,losers_dict]
    #getting results to display earning calander
    def getting_earnings_calander():
        earnings_calander_dict = {'sym':[],
                                  'name':[],
                                  'report_date':[],
                                  'estimate':[]}
        earning_results = EARNINGS_CALANDER.query.order_by(EARNINGS_CALANDER.symbol.asc()).all()

        for e in earning_results:
            earnings_calander_dict['sym'].append(r.symbol)
            earnings_calander_dict['name'].append(r.name)
            earnings_calander_dict['report_date'].append(r.report_date)
            earnings_calander_dict['estimate'].append(r.estimate)

        return earnings_calander_dict



