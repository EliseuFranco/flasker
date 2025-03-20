from flask import Flask, request, flash ,render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime



#Instancia do flask
app = Flask(__name__, static_folder="static", template_folder="templates")
secret_key = secrets.token_bytes(16)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

#Initialize database
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    #Create string

    def __repr__(self):
        return f"<Name {self.name}"


# Create a form class
class userForm(FlaskForm):
    name = StringField("Whta´s your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class userDbForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")



@app.route("/user/add", methods=["GET",'POST'])
def add_user():
    form = userDbForm()
    name = ""

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if not user:
            new_user = Users(name=form.name.data, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
        form.name.data = ""
        form.email.data = ""
    our_users = Users.query.order_by(Users.date_added)
    if not our_users:
        our_users = "NOTE DATA TO SHOW"

    return render_template("add_user.html", 
                           form = form, name = name,
                           our_users = our_users)

@app.route("/")
def index():
    favorites = ["Pepperoni", "Margarida", 2,5,6]
    stuff = "This is a <strong>bold text</strong>"
    return render_template("index.html", stuff = stuff, lista = favorites)


@app.route("/user/<name>")
def user(name):
   return render_template("user.html", user=name)

# CREATING CUSTOM ERROR PAGE

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error 
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route("/name", methods=["GET","POST"])
def name():
    name = None
    form = userForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted Successful")
        
    return render_template("name.html",
                            form = form, name=name)



if __name__ == "__main__":
    app.run(debug=True)