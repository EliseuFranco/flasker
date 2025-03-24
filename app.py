from flask import Flask, request, flash ,render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime
from flask_migrate import Migrate
from time import sleep

#Instancia do flask
app = Flask(__name__, static_folder="static", template_folder="templates")
secret_key = secrets.token_bytes(16)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:%40Samulolo26@localhost:5432/ouruser"

#Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False, unique=True)
    favourite_color = db.Column(db.String(10))
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
    favourite_color = StringField("Favourite color")
    submit = SubmitField("Submit")



@app.route("/user/add", methods=["GET",'POST'])
def add_user():
    form = userDbForm()
    name = ""

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if not user:
            new_user = Users(name=form.name.data,
                              email=form.email.data,
                              favourite_color = form.favourite_color.data)
            db.session.add(new_user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added successfully!")
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

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    form = userDbForm()
    user_to_update = Users.query.get_or_404(id)

    if request.method == 'POST':
       
        print(user_to_update)
        user_to_update.name = request.form["name"]
        user_to_update.email = request.form["email"]
        user_to_update.favourite_color = request.form["favourite_color"]
        try:
            db.session.commit()
            flash("User updated succssesfully")
            return render_template("update.html", form = form, user = user_to_update)
        except:
            flash("There have a problem")
            return render_template("update.html", form = form, user = user_to_update)
    return render_template("update.html", form = form, user = user_to_update)


@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
    form = userDbForm()
    user_to_delete = Users.query.get_or_404(id)

    try:
        if request.method == "POST":
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                flash("User deleted successfully")
                return redirect(url_for("add_user"))
    except:
        flash("There was a problem deleting the user, try again")


    return render_template("delete.html",form = form, user = user_to_delete)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)