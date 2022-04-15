#from pyexpat import Model
from tracker.extensions import db
from sqlalchemy.sql import func



#db.Table

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