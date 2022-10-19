import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_app.models.purchase import Purchase
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def display():
    if session['user'] > 0:
        user_id = session['user']
        return redirect(f'/welcome/{user_id}')
    else:
        return render_template("login.html")

@app.route('/create', methods=['POST'])
def create_user():
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "password2" : request.form['password2']
    }
    if not User.validate_user(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "fname" : request.form['fname'],
        "lname" : request.form['lname'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.createuser(data)
    session['user'] = user_id
    return redirect(f'/welcome/{user_id}')

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/')
    user = user_in_db.id
    session['user']= user_in_db.id
    return redirect(f'/welcome/{user}')

@app.route('/welcome/<int:id>')
def welcome(id):
    if session['user'] != id:
        return redirect('/logout')
    user = User.getuser(id)
    cars = Car.getcarpurchase()
    print(cars)
    # cars = Car.getcars()
    # purchases = Purchase.purchases()
    # print(purchases)
    return render_template("homepage.html",user = user, cars = cars)

@app.route('/logout')
def logout():
    session['user'] = 0
    return redirect('/')

@app.route('/add')
def add():
    return render_template("listcar.html")

@app.route('/purchase/<int:id>')
def purchasecar(id):
    data = {"id":id, "user_id":session['user']}
    User.purchase(data)
    return redirect('/')

@app.route('/purchases')
def mypurchases():
    user_id = session['user']
    purchases = Purchase.mypurchases(user_id)
    user = User.getuser(user_id)
    return render_template("purchases.html", purchases = purchases, user = user)