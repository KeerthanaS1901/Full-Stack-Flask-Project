# This is a sample Python script.
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask import session

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db.init_app(app)
class users(db.Model):
    __tablename__ = "users"
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("user", db.String(100))
    phone = db.Column("mobile", db.Integer())
    area = db.Column("location", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("psw", db.String(100))

    def __init__(self, name, phone, area, email, password):
        self.name = name
        self.phone = phone
        self.area = area
        self.email = email
        self.password = password


@app.route("/", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        user = request.form['user']
        phone = request.form['mobile']
        area = request.form['location']
        email = request.form['email']
        password = request.form['psw']
        repeatpassword = request.form['psw-repeat']

        user = users(name = user, phone = phone, area = area, email = email, password = password)

        db.session.add(user)

        db.session.commit()
        flash("registered succesfully!!!")
        return redirect(url_for('login'))
    return render_template("2.html")



@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['user']
        password = request.form['psw']
        userdata = users.query.filter_by(name = username,password = password).first()


        if userdata:
            return redirect(url_for("index"))
        else:
            flash("invalid credentials, please enter proper credentials")
            return render_template("1.html", message="Invalid Credentials")
    return render_template("1.html",message = "Invalid Credentials")

@app.route("/index")
def index():
    flash("logged in succesfully!!!, credentials have been saved")
    return render_template("index.html")





if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
