from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.car import Car


@app.route('/createcar', methods=['POST'])
def createcar():
    data = {
        "price" : request.form['price'],
        "make" : request.form['make'],
        "model" : request.form['model'],
        "year" : request.form['year'],
        "description" : request.form['description'],
        "user_id" : session['user']
    }
    if not Car.validatecar(data):
        return redirect('/')
    Car.createcar(data)
    user_id = session['user']
    return redirect(f'/welcome/{user_id}')

@app.route('/view/<int:id>')
def viewcar(id):
    data = {"id":id}
    car = Car.viewcaruser(data)
    print(car)
    return render_template("viewcar.html", car=car)

@app.route('/delete/<int:id>')
def delete(id):
    Car.delete(id)
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    data={"id":id}
    car = Car.viewcar(data)
    return render_template("editcar.html", car = car)

@app.route('/updatecar/<int:id>', methods=['POST'])
def updatecar(id):
    data ={
        "id" : id,
        "price" : request.form['price'],
        "model" : request.form['model'],
        "make" : request.form['make'],
        "year" : request.form['year'],
        "description" : request.form['description']
    }
    Car.updatecar(data)
    return redirect('/')