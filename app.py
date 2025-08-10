from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
#
app = Flask(__name__)
# Add database

# old sqlite dbapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySQL8982@localhost/users'
app.config['SECRET_KEY'] = "127Trellewelyn"
mydb = mysql.connector.connect(
    user="root",
    passwd = "MySQL8982",
    host="localhost",
    auth_plugin='mysql_native_password'
)
my_cursor = mydb.cursor()
# my_cursor.execute("DROP DATABASE users")
my_cursor.execute("CREATE DATABASE IF NOT EXISTS users")


for db in my_cursor:
    print(db)


# # Form Class
db = SQLAlchemy(app)



####
with app.app_context():
    db.create_all()
# model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
#
# Create strimg
#
    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name=StringField("Name?", validators=[DataRequired()])
    email=StringField("Email?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#### Update Record###
# Here is where we update the record...

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form=UserForm()
    name_to_update = Users.query.get_or_404(id)
    
    if request.method=="POST":
        name_to_update.name = request.form['name']
    #    email_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated!")
            return render_template("update.html", 
                form=form, 
                name_to_update = name_to_update, id=id) 
                    
        except:
            flash("Error Looks like there ws a problem... Try again!")
            return render_template("update.html", 
                form=form, 
                name_to_update = name_to_update.name) 
    else:
          return render_template("update.html", 
                form=form, 
                name_to_update = name_to_update,id=id)               

####
#
class NamerForm(FlaskForm):
    name=StringField("Name?", validators=[DataRequired()])
    email=StringField("Email?", validators=[DataRequired()])
    submit = SubmitField("Submit")
def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app
@app.route('/')

# Here is the index page
def index():
    first_name = "Harry"
    stuff = "This is text"
    flash("Welcome to the blog!")
    favourite_pizza=["Pepperoni", "Cheese", "Meatball", "Hawaian", "Ham and Mushroom", 100]
    
    return render_template('index.html', first_name=first_name, stuff=stuff, favourite_pizza=favourite_pizza)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"),500

################
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users=Users.query.order_by(Users.id)
    return render_template("add_user.html",
        form=form,
        name=name,
        our_users=our_users)
################

@app.route('/user/<name>')
def user(name):
    
    return render_template("user.html", name=name)

# Name Page

@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
        # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")
            
    return render_template("name.html", 
        name = name,
        form = form)
    
    

