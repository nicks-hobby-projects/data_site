from data_site import api
from flask_restful import Resource, Api, reqparse
from data_site.models import *
from datetime import datetime
from data_site import db
from data_site import app
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def limiter():
    _limiter = Limiter(
        app,
        key_func=get_remote_address
    )
    return _limiter





class Markets(Resource):
    decorators = [limiter().limit("6/minute;1/10 seconds", methods=["GET"])]

    def get(self):


        parser = reqparse.RequestParser()
        parser.add_argument('sym', required = True)
        parser.add_argument('st_date', required = True)
        parser.add_argument('en_date', required = True)
        args = parser.parse_args()

        pos_syms = ['gspc','ixic','dji','crude_oil']
        start_date = datetime.strptime(args['st_date'],'%Y-%m-%d')
        end_date = datetime.strptime(args['en_date'],'%Y-%m-%d')
        num_days = end_date - start_date

        if num_days.days <= 61:

            if args['sym'] in pos_syms:
                open = []
                high = []
                low = []
                close = []
                adjclose = []
                volume = []
                date = []

                if args['sym'] == 'gspc':

                    results = GSPC.query.filter(GSPC.date >= start_date).filter(GSPC.date <= end_date).all()
                    for r in results:
                        open.append(r.open)
                        high.append(r.high)
                        low.append(r.low)
                        close.append(r.close)
                        adjclose.append(r.adjclose)
                        volume.append(r.volume)
                        date.append(r.date.strftime('%Y-%m-%d'))
                    answer = {'gspc':
                            {'open':open,
                              'high':high,
                              'low':low,
                              'close':close,
                              'adjclose':adjclose,
                              'volume':volume,
                              'date':date
                        }}
                    answer = json.dumps(answer)
                    return answer

                if args['sym'] == 'ixic':
                    results = IXIC.query.filter(IXIC.date >= start_date).filter(IXIC.date <= end_date).all()
                    for r in results:
                        open.append(r.open)
                        high.append(r.high)
                        low.append(r.low)
                        close.append(r.close)
                        adjclose.append(r.adjclose)
                        volume.append(r.volume)
                        date.append(r.date.strftime('%Y-%m-%d'))
                    answer = {'ixix':
                            {'open':open,
                              'high':high,
                              'low':low,
                              'close':close,
                              'adjclose':adjclose,
                              'volume':volume,
                              'date':date
                        }}
                    answer = json.dumps(answer)
                    return answer

                if args['sym'] == 'dji':
                    results = DJI.query.filter(DJI.date >= start_date).filter(DJI.date <= end_date).all()
                    for r in results:
                        open.append(r.open)
                        high.append(r.high)
                        low.append(r.low)
                        close.append(r.close)
                        adjclose.append(r.adjclose)
                        volume.append(r.volume)
                        date.append(r.date.strftime('%Y-%m-%d'))
                    answer = {'dji':
                            {'open':open,
                              'high':high,
                              'low':low,
                              'close':close,
                              'adjclose':adjclose,
                              'volume':volume,
                              'date':date
                        }}
                    answer = json.dumps(answer)
                    return answer

                if args['sym'] == 'crude_oil':
                    results = CRUDE_OIL.query.filter(DJI.date >= start_date).filter(CRUDE_OIL.date <= end_date).all()
                    for r in results:
                        open.append(r.open)
                        high.append(r.high)
                        low.append(r.low)
                        close.append(r.close)
                        adjclose.append(r.adjclose)
                        volume.append(r.volume)
                        date.append(r.date.strftime('%Y-%m-%d'))
                    answer ={'crude_oil':
                            {'open':open,
                              'high':high,
                              'low':low,
                              'close':close,
                              'adjclose':adjclose,
                              'volume':volume,
                              'date':date
                        }}
                    answer = json.dumps(answer)
                    return answer
            else:
                return "Please use a sym in (gspc, ixic, dji, crude_oil)"
        else:
            return "Please enter a date range of <=60"

class Total_Wealth(Resource):
    decorators = [limiter().limit("6/minute;1/10 seconds", methods=["GET"])]

    def get(self):

        bot50 = []
        f50to90 = []
        f90to99 = []
        f99to100 = []
        sum = []
        bot50_per = []
        f50to90_per = []
        f90to99_per = []
        f99to100_per = []
        date = []
        results = TOTAL_WEALTH_DIST.query.all()
        for r in results:
            bot50.append(r.bot50)
            f50to90.append(r.f50to90)
            f90to99.append(r.f90to99)
            f99to100.append(r.f99to100)
            sum.append(r.sum)
            bot50_per.append(r.bot50_per)
            f50to90_per.append(r.f50to90_per)
            f90to99_per.append(r.f90to99_per)
            f99to100_per.append(r.f99to100_per)
            date.append(r.date.strftime('%Y-%m-%d'))
        answer = {'total_wealth':{
                'bot50': bot50,
                'f50to90': f50to90,
                'f90to99': f90to99,
                'f99to100':f99to100,
                'sum': sum,
                'bot50_per':bot50_per,
                'f50to90_per':f50to90_per,
                'f90to99_per':f90to99_per,
                'f99to100_per':f99to100_per,
                'date':date
                    }}
        answer = json.dumps(answer)
        return answer


