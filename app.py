from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime, timedelta


app=Flask(__name__)
app.secret_key="todo"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=5)

# Initialize the database
db = SQLAlchemy(app)

class Data(db.Model):
    
    _s_no=db.Column("s_no", db.Integer , primary_key=True, autoincrement=True)
    dat=db.Column(db.DateTime, nullable=False)
    task=db.Column(db.String(200), nullable=False)


    def __init__(self, dat, task):
        
        self.dat=dat
        self.task=task

    





@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        print("Task entered")
        task=request.form.get("task")
        print(task)
        time=datetime.now()
        print(time)
        
        

        record=Data(time,task)
        print(record)
       
        db.session.add(record)
        db.session.commit()
        print("record added")
        print(record)
        print(record.dat)
        print(record.task)
        
        # print(record.task, record.time)
        return redirect(url_for("home"))

    data_records = Data.query.all()
    print(data_records)
    Data.query.filter_by(dat=None).delete()
    return render_template("index.html", data=data_records)

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)