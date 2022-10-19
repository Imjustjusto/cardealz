from operator import methodcaller
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.names = []

    @classmethod
    def getcars(cls):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id = cars.user_id;"
        result = connectToMySQL('cardealz_schema').query_db(query)
        return result

    @classmethod
    def createcar(cls, data):
        query = "INSERT INTO cars (price, make, model, year, description, user_id, created_at, updated_at) VALUES (%(price)s, %(make)s, %(model)s, %(year)s, %(description)s, %(user_id)s, NOW(), NOW());"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        return result

    @classmethod
    def viewcaruser(cls, data):
        query = "SELECT * FROM cars LEFT JOIN users ON users.id = cars.user_id WHERE cars.id = %(id)s;"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        car = cls(result[0])
        for row in result:
            first_name = row['first_name']
            last_name = row['last_name']
            car.names.append(first_name)
            car.names.append(last_name)
        return car

    @classmethod
    def delete(cls,id):
        data={"id":id}
        query= "DELETE FROM cars WHERE id = %(id)s"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        return result

    @classmethod
    def viewcar(cls, data):
        query = "SELECT * FROM cars WHERE cars.id = %(id)s"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def updatecar(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE cars.id = %(id)s;"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        return result

    @classmethod
    def getcarpurchase(cls):
        query = "SELECT * FROM cars LEFT JOIN purchases ON purchases.car_id = cars.id;"
        result = connectToMySQL('cardealz_schema').query_db(query)
        return result

    @classmethod
    def validatecar(cls, data):
        is_valid = True
        if len(data['make']) < 1:
            flash("Car make should be more than 2 characters.")
            is_valid = False
        if len(data['model']) < 3:
            flash("Car model should be more than 2 characters.")
            is_valid = False
        if int(data['year']) < 1:
            flash("Car manufacturing year not allowed.")
            is_valid = False
        if int(data['price']) < 1:
            flash("You can't give out your car for free!!!")
            is_valid = False
        return is_valid