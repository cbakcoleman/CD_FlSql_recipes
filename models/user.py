from recipes_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address!', 'email')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters!', 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters!', 'last_name')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash('Password must be at least 8 characters, include at least one uppercase letter, one lowercase letter, one number, and one special character!', 'password')
        if user['confirm_password'] != user['password']:
            flash('Confirm password does not match password!', 'confirm_password')
            is_valid = False
        return is_valid
        
    @classmethod
    def add_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s , %(email)s , %(password)s );'
        new_user = connectToMySQL('recipes_schema').query_db(query, data)
        return new_user

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s ;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL('recipes_schema').query_db(query, data)

        if len(results) < 1:
                return False

        return cls(results[0])


        