from flask import Blueprint, render_template,request,redirect,Flask
from extensions import db
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
import time
#from tracker.models import ID,log,tracker
#from flask_alchemy import SQLAlchemy
#from models.py import log,ID,tracker
#db.Table
from sqlalchemy.sql import func
from flask import url_for  

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

mainnn = Blueprint('main',__name__)

global current_user

@mainnn.route('/',methods=['GET','POST'])
def index():
    flag="False"
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        data=ID.query.all()
        username2=request.form["ID"]
        password2=request.form["Password"]
        
        a=ID.query.filter_by(username=username2,password=password2).all()
        if a:
            #current_user=username2
            return redirect(f"/dashboard/{username2}")
        else:#render_template("/404")
            return redirect("/")
            #return 'hello world'
        #What should I write here ?

@mainnn.route('/add_user',methods=['GET','POST'])
def add_user():
    if request.method == "GET":
        return render_template('add_user.html')
    elif request.method == "POST":
        #s_record = Student.query.filter_by(roll_number=roll).one()
        try:
            username1=request.form["ID"]
            password1=request.form["Password"]
            x=ID(username=username1, password=password1)
            db.session.add(x)
            db.session.commit() 
            return redirect('/') 
        except:
            return redirect('/add_user')
            
    

@mainnn.route('/dashboard/<string:username>')
def dashboard_view(username):
    trackers=Tracker.query.filter_by(e_username=username).all()
    dictionary={}
    if(not(trackers)):
        return render_template("empty_dashboard.html",username=username)    
    # try:
    for i in trackers:
        dictionary[i.tracker_id]=Log.query.filter_by(e_tracker_id=i.tracker_id).order_by(Log.datetime.desc()).first()#Should it be first or last datetime
    return render_template("dashboard.html",trackers=trackers,dictionary=dictionary,username=username)
    # except:
    #     return render_template('empty_dashboard.html',username=username) 
        

@mainnn.route('/view/<string:username>/<int:tracker_id>')
def view_2(username,tracker_id):
    trackers=Tracker.query.filter_by(e_username=username).all()
    logs=Log.query.filter_by(e_tracker_id=tracker_id).all()
    name_tracker=Tracker.query.filter_by(e_username=username).first()
    a=[]
    temp=[]
    for i in logs:
        a.append(i.datetime)
        temp.append(i.text)
    #date_time=pd.to_datetime(temp).date
    
    DF = pd.DataFrame({'temp' : temp}, index=[i for i in a])
    ax = DF.plot(x_compat=True,rot=90, figsize=(7,5))
    plt.xlabel("Datetime")
    plt.ylabel("Value")
    url_for('static',filename='myplot.png')
    fig = ax.get_figure()
    fig.savefig('static/myplot.png')
    return render_template('view.html',trackers=trackers,logs=logs,username=username,name_tracker=name_tracker,tracker_id=tracker_id)

@mainnn.route('/tracker/<string:username>',methods=['GET','POST'])
def view_1(username):
    if request.method == "GET":
        return render_template('tracker.html',username=username)
    elif request.method == "POST":
        # try:
        tracker_name = request.form["name"]
        tracker_description = request.form["description"]
        tracker_repeat=request.form.get("repeat")
        if tracker_repeat:
            tracker_post_0=Tracker(e_username=username,tracker_name=tracker_name,tracker_description=tracker_description,tracker_repeat=1)
            db.session.add(tracker_post_0)
            db.session.commit()
            
            return redirect(f"/dashboard/{username}")
        else:
            tracker_post=Tracker(e_username=username,tracker_name=tracker_name,tracker_description=tracker_description,tracker_repeat=0)
        
            db.session.add(tracker_post)
            db.session.commit()
            return redirect(f"/dashboard/{username}")
        # except:
        #     return render_template('tracker.html',username=username)
            


@mainnn.route('/log/<string:username>/<int:tracker_id>/add',methods=['GET','POST'])
def add(username,tracker_id):
    if request.method == "GET":
        tracker_select=Tracker.query.filter_by(e_username=username,tracker_id=tracker_id)
        return render_template('log.html', username=username, tracker_select=tracker_select,tracker_id=tracker_id)
    elif request.method == "POST":
        #log_datetime = request.form["datetime"]
        scale = request.form["scale"]
        notes=request.form["notes"]
        y=Log(e_tracker_id=tracker_id,text=scale,notes=notes)
        try:
            db.session.add(y)
            db.session.commit()
            return redirect(f"/dashboard/{username}")
        except:
            return redirect(f"/log/{username}/{tracker_id}/add")
            
@mainnn.route('/tracker/<string:username>/delete/<int:tracker_id>')
def tracker_delete(username,tracker_id):
    delete_data=Tracker.query.filter_by(e_username=username,tracker_id=tracker_id).first()
    db.session.delete(delete_data)
    db.session.commit()

    return redirect(f"/dashboard/{username}")

@mainnn.route('/tracker/<string:username>/update/<int:tracker_id>', methods=['GET','POST'])
def tracker_update(username,tracker_id):
    if request.method == "GET":
        update_data=Tracker.query.filter_by(e_username=username,tracker_id=tracker_id)
        l=[]
        l.append(update_data)
        return render_template("update_tracker.html",update_data=update_data,username=username,tracker_id=tracker_id,l=l)

    elif request.method == "POST":
        tracker_name = request.form["name"]
        tracker_description=request.form["description"]
        #tracker_repeat=0
        tracker_repeat=request.form.get("repeat")
        print(tracker_repeat)
        if tracker_repeat:
            #y=Tracker(e_username=username,tracker_id=tracker_id,tracker_name=tracker_name,tracker_description=tracker_description,tracker_repeat=1)
            Tracker.query.filter_by(tracker_id=tracker_id).update({Tracker.tracker_name : tracker_name, Tracker.tracker_description : tracker_description, Tracker.tracker_repeat : 1, Tracker.e_username : username})
        else:
            Tracker.query.filter_by(tracker_id=tracker_id).update({Tracker.tracker_name : tracker_name, Tracker.tracker_description : tracker_description, Tracker.tracker_repeat : 0, Tracker.e_username : username})
        
        # # try:
        #     db.session.add(y)
        db.session.commit()
        return redirect(f"/dashboard/{username}")
        # except:
        #     return redirect(f"/tracker/{username}/update/{tracker_id}")



@mainnn.route('/log/<string:username>/<int:tracker_id>/edit',methods=['GET','POST'])
def edit(username,tracker_id):
    if request.method == "GET":
        update_log_data=Log.query.filter_by(e_tracker_id=tracker_id)
        return render_template('edit_log.html', username=username, update_log_data=update_log_data,tracker_id=tracker_id)
    elif request.method == "POST":
        scale = request.form["scale"]
        notes=request.form["notes"]
        #y=Log(e_tracker_id=tracker_id,text=scale,notes=notes)
        # try:
        Log.query.filter_by(e_tracker_id=tracker_id).update({Log.text : scale, Log.notes : notes})
        db.session.commit()
        return redirect(f"/dashboard/{username}")
        # except:
        #     return redirect(f"/log/{username}/{tracker_id}/edit")


@mainnn.route('/log/<string:username>/<int:tracker_id>/delete/<string:datetimes>')
def log_delete(username,tracker_id, datetimes):
    a=datetimes.split()
    b=datetime.strptime(a[0],'%Y-%m-%d')
    c=datetime.strptime(a[1],'%H:%M:%S').time()
    d=datetime.combine(b,c)
    delete_log_data=Log.query.filter_by(datetime=d,e_tracker_id=tracker_id).first()
    db.session.delete(delete_log_data)
    db.session.commit()

    return redirect(f"/dashboard/{username}")
