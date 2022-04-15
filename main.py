from flask import Flask
from mainn.routes import mainnn

#from tracker.extensions import db
#from tracker.models import *
from flask_sqlalchemy import SQLAlchemy
#from tracker.routes import 
from matplotlib import pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)
db = SQLAlchemy(app)

from sqlalchemy.sql import func
class ID(db.Model):
    __tablename__="id"
    username=db.Column(db.String(15),primary_key=True)#Should unique be added ?
    password=db.Column(db.String(15),nullable=False)
    idtrack = db.relationship('Tracker', cascade='all', backref='tracker')

#delete-orphan
class Log(db.Model):
    __tablename__="log"
    #log_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    datetime = db.Column(db.DateTime(timezone=False), default=func.now(),primary_key=True)
    text = db.Column(db.Integer,nullable=False)
    notes = db.Column(db.String(250),nullable=True)
    e_tracker_id=db.Column(db.String(50), db.ForeignKey("tracker.tracker_id"),nullable=False)
class Tracker(db.Model):
    __tablename__="tracker"
    e_username=db.Column(db.String(15), db.ForeignKey("id.username"),nullable=False)
    tracker_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_name=db.Column(db.String(50), nullable=False)
    #tracker_type=db.Column(db.Boolean,nullable=False)
    tracker_description=db.Column(db.String(200),nullable=True)
    tracker_repeat=db.Column(db.Boolean,nullable=True)
    tracklog = db.relationship('Log', cascade='all', backref='log')
db.create_all()#Should I create function create_app (30:53)?
app.register_blueprint(mainnn)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)
    app.debug()