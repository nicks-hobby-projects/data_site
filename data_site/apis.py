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


class CustomAPIMixin:
    def api_response(self, content):
        return content



class Markets(Resource):
    decorators = [limiter().limit("1/minute", methods=["GET"])]

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

