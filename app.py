from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import time
from datetime import datetime, timedelta, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators,SubmitField
from wtforms.validators import DataRequired

# App initialisation
app=Flask(__name__)
app.config['SECRET_KEY']="todo"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime=timedelta(minutes=5)

# Initialize the database
db = SQLAlchemy(app)

class Data(db.Model):
    
    _s_no=db.Column("s_no", db.Integer , primary_key=True, autoincrement=True)
    dat=db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    task=db.Column(db.String(200), nullable=False)
    


    def __init__(self, task):
        
       
        self.task=task


# WTForm to enter new task
     
class Taskform(FlaskForm):
    task=StringField("The task", validators=[DataRequired()])
    submit=SubmitField("ADD")

    
class updateform(FlaskForm):
    updated_task=StringField("Updated_task", validators=[DataRequired()]) 
    submit= SubmitField("UPDATE")


#Home Page that shows all previously added tasks, a textbox to enter new task, 
#a ADD button to add it to table/database,
##an update link which directs to the update page where you can enter the upadtes task 
#and hit update to reflect it in table/databse



@app.route("/", methods=['GET', 'POST'])
def home():

    task=None
    form=Taskform()

    #Verifies if anu data is entered in the textbox by the user.

    """If a task is entered, the task entered is stored in a variabel called task 
    and then the form-textbox is again set to none for new task entry"""

    if form.validate_on_submit():
        task= form.task.data
        form.task.data=None
        


        #Here the task is being added to database/table
        if task:
            
            print(task)
            record=Data(task=task)
            print(record)
            
            db.session.add(record)
            db.session.commit()
            print("record added")
            flash("Task added!", "info")
            print(record)
            print(record.dat)
            print(record.task)
            
            
            
           

            return redirect(url_for("home")) #redirects to home page via get request  to reflect change and 
                                             # cancelled out duplication of data which might occurs during 
                                             # refresh due to the previous request methods beingpost.

    else:

        
 
        data_records = Data.query.all()
        print(data_records)

        

        return render_template("index.html", data_record=data_records, form=form,task=task)



# update page with a textbox box with pre-texted task to overwrite and an upadte button to reflect change

@app.route("/update/<s_no>", methods=['GET','POST'])
def update(s_no):
    updated_task=None
    update_form=updateform()

    
    record_to_update=Data.query.get_or_404(s_no)# Checks for record with s_no as id else returns 404
    print("Record found!")

    if update_form.validate_on_submit():
        updated_task= update_form.updated_task.data
        print(updated_task)
        record_to_update.task=updated_task
        update_form.updated_task.data=None
        
        db.session.commit()
        
        return redirect(url_for("home"))
    
    else:

        print("Into else")
        return render_template("update.html", record_to_update=record_to_update, form=update_form, 
                               updated_task=updated_task)

@app.route("/delete/<s_no>", methods=['GET','POST']) 
def delete(s_no):

    record_to_delete=Data.query.get_or_404(s_no)
    print("Record found!")
    db.session.delete(record_to_delete)
    db.session.commit()

    return redirect(url_for("home"))

    


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)