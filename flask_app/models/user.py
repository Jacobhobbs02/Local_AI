from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

db = 'ai_app'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.conversations = []
        self.groups = []

#Saving User Information 
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users(full_name,email,password,created_at) VALUES (%(full_name)s,%(email)s,%(password)s,NOW());"
        print("Data to insert:", data)
        results = connectToMySQL(db).query_db(query,data)
        if results is False:
            print("Error occurred while saving user data.")
        return results

#User Validation    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["full_name"]) == 0 or len(user["email"]) == 0:
            is_valid = False
            flash("All fields required!",'danger')

        if len(user['full_name']) <=0:
            flash(" First Name must be longer than 0 letters!",'danger')
            is_valid = False
        if len(user["email"]) >= 0 and not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format!", 'danger')
            is_valid = False
        return is_valid


#Password Validation for resetting passwords    
    @staticmethod
    def validate_password(user):
        is_valid = True
        if len(user['password']) < 14:
            flash("Password must be at least 14 characters!","danger")
            is_valid = False

        if user['password'] != user['confirm']:
            flash("Passwords don't match","danger")
            is_valid = False

        return is_valid

#Get One User for logging in and updating user information    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

#Grab User's account by Email    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

# Updating User Information
    @classmethod
    def update_user(cls, data, id):
        # Get the current password if not provided
        if not data.get('password'):
            data['password'] = User.get_current_password(id)

        query = """
                UPDATE users 
                SET full_name = %(full_name)s, 
                email = %(email)s, 
                password = %(password)s, 
                updated_at = NOW()
                WHERE id = %(id)s;
                """
        data['id'] = id
        connectToMySQL(db).query_db(query, data)
        results = connectToMySQL(db).query_db(query, data)
        return results
        
    @classmethod
    def get_current_password(cls, user_id):
        query = "SELECT password FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        result = connectToMySQL(db).query_db(query, data)

        if result:  # If user is found, return the password
            return result[0]['password']
        else:
            return None  # Handle case where user is not found

#Updating User Password    
    @classmethod
    def update_password(cls, data):
        query = "UPDATE users SET password = %(password)s WHERE email = %(email)s;"
        return connectToMySQL(db).query_db(query, data)

#Deleting User Account    
    @classmethod
    def delete_account(cls, user_id):
        query = "DELETE from users WHERE id = %(id)s;"
        data = {
            "id": user_id
        }
        connectToMySQL(db).query_db(query,data)
        return user_id