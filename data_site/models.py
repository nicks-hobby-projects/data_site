from data_site import db

class CPIAUCSL(db.Model):
    __tablename__ = "CPIAUCSL".lower()
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
    vals = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
class UNRATE(db.Model):
    __tablename__ = "UNRATE".lower()
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
    vals = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
class GDP(db.Model):
    __tablename__ = "GDP".lower()
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
    vals = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
class UMCSENT(db.Model):
    __tablename__ = "UMCSENT".lower()
    #index = db.Column(db.Integer(),primary_key=True, nullable=False,unique=True)
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
    vals = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
class MICH(db.Model):
    __tablename__ = "MICH".lower()
    #index = db.Column(db.Integer(),primary_key=True, nullable=False,unique=True)
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
    vals = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
class TOTAL_WEALTH_DIST(db.Model):
    __tablename__ =    'TOTAL_WEALTH_DIST'.lower()
    #index = db.Column(db.Integer(), primary_key = True,nullable=False,unique=True)
    bot50 = db.Column(db.Float(),nullable = False)
    f50to90 = db.Column(db.Float(),nullable = False)
    f90to99 = db.Column(db.Float(),nullable = False)
    f99to100 = db.Column(db.Float(),nullable = False)
    sum = db.Column(db.Float(),nullable = False)
    bot50_per = db.Column(db.Float(),nullable = False)
    f50to90_per = db.Column(db.Float(),nullable = False)
    f90to99_per = db.Column(db.Float(),nullable = False)
    f99to100_per = db.Column(db.Float(),nullable = False)
    date_added = db.Column(db.DateTime(timezone = False))
    date = db.Column(db.DateTime(timezone = False),primary_key= True,nullable=False)
class GSPC(db.Model):
    #SP500
    __tablename__ = 'GSPC'.lower()
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float())
    adjclose = db.Column(db.Float())
    volume = db.Column(db.Float())
    date = db.Column(db.DateTime(timezone = False),primary_key= True)
class IXIC(db.Model):
    #NASDAQ
    __tablename__ = 'IXIC'.lower()
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float())
    adjclose = db.Column(db.Float())
    volume = db.Column(db.Float())
    date = db.Column(db.DateTime(timezone = False),primary_key= True)
class DJI(db.Model):
    #DOW30
    __tablename__ = 'DJI'.lower()
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float())
    adjclose = db.Column(db.Float())
    volume = db.Column(db.Float())
    date = db.Column(db.DateTime(timezone = False),primary_key= True)
class CRUDE_OIL(db.Model):
    #CRUDE_OIL
    __tablename__ = 'CRUDE_OIL'.lower()
    open = db.Column(db.Float())
    high = db.Column(db.Float())
    low = db.Column(db.Float())
    close = db.Column(db.Float())
    adjclose = db.Column(db.Float())
    volume = db.Column(db.Float())
    date = db.Column(db.DateTime(timezone = False),primary_key= True)
class BIGGEST_GAINERS_LOSERS_DAILY(db.Model):
    __tablename__ = 'BIGGEST_GAINERS_LOSERS_DAILY'.lower()
    index = db.Column(db.Integer(), primary_key = True)
    symbol = db.Column(db.String())
    name = db.Column(db.String())
    price_intra = db.Column(db.Float())
    change_per = db.Column(db.Float())
    date = db.Column(db.DateTime( timezone = False))
    type = db.Column(db.String())
class EARNINGS_CALANDER(db.Model):
    __tablename__ = 'EARNINGS_CALANDER'.lower()
    index = db.Column(db.Integer(), primary_key = True)
    symbol = db.Column(db.String())
    name = db.Column(db.String())
    reportDate = db.Column(db.DateTime(timezone = False))
    estimate = db.Column(db.Float())


