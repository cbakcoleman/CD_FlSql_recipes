from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Name must be at least 3 characters long', 'name')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters long', 'description')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters long', 'instruction')
            is_valid = False
        if len(recipe['created_at']) < 1:
            flash('Date can not be empty', 'created_at')
            is_valid = False
        if len(recipe['under_30']) < 1:
            flash('Under 30 mintues? can not be empy', 'under_30')
            is_valid = False
        return is_valid

    @classmethod
    def add_recipe(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under_30, created_at, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(created_at)s, %(user_id)s );'
        new_recipe_id = connectToMySQL('recipes_schema').query_db(query, data)
        return new_recipe_id