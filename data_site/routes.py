from data_site import app, api
from flask import render_template, redirect, url_for, flash
import pandas as pd
from data_site import db
from data_site.models import *
from data_site.web_functs import *
from datetime import datetime
from flask import request
from data_site.apis import *


@app.route('/')
@app.route('/home')
def home_page():
    indexes = {}
    syms = {'CL=F':'Crude Oil',
            '^GSPC':'S&P 500',
            '^IXIC':'Nasdaq',
            '^DJI':'Dow Jones'}
    for s in syms:
        val = functs.getting_current_index_values(s)
        indexes[syms[s]] = val
    gspc_prev = functs.getting_prev_close_value_for_index(GSPC)
    ixic_prev = functs.getting_prev_close_value_for_index(IXIC)
    dji_prev = functs.getting_prev_close_value_for_index(DJI)
    crude_oil_prev = functs.getting_prev_close_value_for_index(CRUDE_OIL)
    apod = functs.getting_nasa_apod()
    return render_template('home.html',indexes=indexes,apod=apod,
                        gspc_prev = gspc_prev,ixic_prev=ixic_prev,dji_prev=dji_prev,crude_oil_prev=crude_oil_prev,
                        zip=zip)

@app.route('/econ_data')
def econ():
    headers = ['CPI','Unemployment Rate','GDP']
    datas = functs.geting_top_table_vals()
    chart_dict = functs.getting_values_for_charts_econ()
    total_wealth_results = functs.getting_total_wealth_info()
    tot_w_legend = total_wealth_results[0]
    tot_w_labels = total_wealth_results[1]
    tot_w_values = total_wealth_results[2]
    return render_template('econ.html',tot_w_values = tot_w_values, tot_w_labels = tot_w_labels, tot_w_legend=tot_w_legend,chart_dict = chart_dict,headers = headers, datas = datas)

@app.route('/econ_dataV2')
def econ_dataV2():
    gdp_graph = functs.getting_gdp_graph()
    cpi_grpah = functs.getting_cpi_graph()
    total_wealth_graph = functs.making_total_wealth_pie_cahrt()
    return render_template('econ_dataV2.html',gdp_graph=gdp_graph,total_wealth_graph=total_wealth_graph, cpi_grpah=cpi_grpah )

@app.route('/market_data')
def market_data():
    return render_template('market_data.html')

@app.route('/calcs')
def calcs():
    return render_template('calcs.html')

@app.route('/stock_ticker/<sym>')
def stock_ticker_data(sym):
    return render_template('stock_ticker.html', zip = zip,len = len )

@app.route('/etf_ticker/<sym>')
def etf_ticker_data(sym):
    result_dict = functs.getting_ticker_price_results(sym)
    quote = functs.getting_ticker_current_quote(sym)
    return render_template('etf_ticker.html',sym = sym,result_dict=result_dict,quote = quote, len=len)

@app.route('/stock_market')
def stock_market():
    dow_graphJSON = functs.making_stock_charts(DJI,'Dow Jones','Adjusted Close')
    sp500_graphJSON = functs.making_stock_charts(GSPC, 'S&P 500','Adjusted Close')
    nas_graphJSON = functs.making_stock_charts(IXIC, 'Nasdaq','Adjusted Close')
    crude_oil_graphJSON = functs.making_stock_charts(CRUDE_OIL,'Crude Oil','Price Per Barrel')

    indexes = {}
    syms = {'CL=F':'Crude Oil',
            '^GSPC':'S&P 500',
            '^IXIC':'Nasdaq',
            '^DJI':'Dow Jones'}
    for s in syms:
        val = functs.getting_current_index_values(s)
        indexes[syms[s]] = val

    gspc_prev = functs.getting_prev_close_value_for_index(GSPC)
    ixic_prev = functs.getting_prev_close_value_for_index(IXIC)
    dji_prev = functs.getting_prev_close_value_for_index(DJI)
    crude_oil_prev = functs.getting_prev_close_value_for_index(CRUDE_OIL)

    gainers_losers= functs.getting_daily_gainers_and_losers()
    gainers=gainers_losers[0]
    losers=gainers_losers[1]
    return render_template('stock_market.html',zip=zip,dow_graphJSON=dow_graphJSON, sp500_graphJSON=sp500_graphJSON,nas_graphJSON=nas_graphJSON,crude_oil_graphJSON=crude_oil_graphJSON,
                            gainers=gainers, losers=losers,
                            gspc_prev = gspc_prev,ixic_prev=ixic_prev,dji_prev=dji_prev,crude_oil_prev=crude_oil_prev,
                            indexes=indexes)
@app.route('/data_apis')
def data_apis():
    return render_template('data_apis.html')

api.add_resource(Markets,'/apiv1/markets')
api.add_resource(Total_Wealth,'/apiv1/total_wealth')
