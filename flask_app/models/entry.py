from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


DB = "calorie_counter"

class Entry:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.qty = data['qty']
        self.calories = data['calories']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        self.user = None

    @classmethod
    def create_valid_entry(cls, entry_dict):
        if not cls.is_valid(entry_dict):
            return False

        query = """
                INSERT INTO entries (name, qty, calories, user_id)
                VALUES (%(name)s, %(qty)s, %(calories)s, %(user_id)s);"""
        entry_id = connectToMySQL(DB).query_db(query, entry_dict)
        entry = cls.get_by_id(entry_id)

        return entry
    
    @classmethod
    def get_by_id(cls, entry_id):
        data = {"id": entry_id}

        query = """SELECT * FROM entries WHERE id = %(id)s;"""
        
        result = connectToMySQL(DB).query_db(query,data)
        return result[0]

    @staticmethod
    def total_calories(user_id):
        query = """SELECT SUM(calories) AS total_calories FROM entries WHERE user_id = %(user_id)s"""
        data = {'user_id': user_id}
        result = connectToMySQL(DB).query_db(query, data)
        total_calories = result[0]['total_calories']
        return total_calories

    @classmethod
    def delete_by_id(cls,entry_id):
        data = { "id": entry_id}
        query = """DELETE from entries WHERE id = %(id)s;"""
        connectToMySQL(DB).query_db(query,data)

        return entry_id
    
    @classmethod
    def update_entry(cls,entry_dict):
        entry = cls.get_by_id(entry_dict["id"])
        query = """ UPDATE entries
                    SET name = %(name)s, qty = %(qty)s, calories = %(calories)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(DB).query_db(query,entry_dict)
        print (entry)
        # result = result[0]
        return entry
    
    
    @classmethod
    def get_all(cls,entry_id):
        data = { "id": entry_id}
        query = """ SELECT *,entries.id as entid FROM users
                    LEFT JOIN entries ON entries.user_id = users.id
                    WHERE users.id = %(id)s;
                """
        
        result = connectToMySQL(DB).query_db(query,data)

        user_obj = user.User(result[0])

        for entry in result:

            entry_data ={
                    "id": entry["entid"],
                    "name": entry["name"],
                    "qty": entry["qty"],
                    "calories": entry["calories"],
                    "created_at": entry["created_at"],
                    "update_at": entry["update_at"]
                }
            user_obj.entries.append(cls(entry_data))
        return user_obj
        
    @staticmethod
    def is_valid(entry_dict):
        valid = True
        flash_string = "field is required and must be at least 3 characters."
        if len(entry_dict["name"]) < 3:
            flash("name" + flash_string)
            valid = False

        if len(entry_dict["qty"]) <= 0:
            flash("qty" + flash_string)
            valid = False

        if len(entry_dict["calories"]) <= 0:
            flash("calories" + flash_string)
            valid = False

        return valid