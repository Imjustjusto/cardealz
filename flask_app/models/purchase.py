from flask_app.config.mysqlconnection import connectToMySQL

class Purchase:
    def __init__(self, data):
        self.id = data['id']
        self.car_id = data['car_id']
        self.user_id = data['user_id']

    @classmethod
    def purchases(cls):
        query = "SELECT car_id FROM purchases;"
        result = connectToMySQL('cardealz_schema').query_db(query)
        return result

    @classmethod
    def mypurchases(cls, id):
        data = {"id":id}
        query = "SELECT * FROM purchases LEFT JOIN cars ON cars.id = purchases.car_id WHERE purchases.user_id = %(id)s;"
        result = connectToMySQL('cardealz_schema').query_db(query, data)
        return result