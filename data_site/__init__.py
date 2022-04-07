from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_restful import Api
db_name = os.getenv("PA_DB_NAME")
db_username = os.getenv('PA_DB_U')
db_password = os.getenv('PA_DB_PW')
db_host = os.getenv("PA_DB_URL")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(db_username,db_password,db_host,db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
api = Api(app)
from data_site import routes
