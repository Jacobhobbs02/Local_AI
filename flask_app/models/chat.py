from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = 'ai_app'

class Conversation:
    def __init__(self,data):
        self.id = data['id']
        self.prompt = data['prompt']
        self.response = data['response']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.group = None


#Saving Conversations
    @classmethod
    def save_chat(cls, data):
        query = "INSERT INTO conversations (prompt,response,created_at,user_id,group_id) VALUES (%(prompt)s,%(response)s,NOW(),%(user_id)s,%(group_id)s);"
        print("Data to insert:", data)
        results = connectToMySQL(db).query_db(query,data)
        if results is False:
            print("Error occurred while saving user data.")
        return results

    #Get All Books linked to a Specific User
    @classmethod
    def get_all_by_user(cls, user_id):
        query = "SELECT * FROM conversations JOIN users ON conversations.user_id = users.id WHERE users.id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL(db).query_db(query, data)
        all_chats = []
        for row in results:
            one_chat = cls(row)
            user_info = { 
                "id": row['users.id'], 
                "full_name": row['full_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            user = User(user_info)
            one_chat.user = user
            all_chats.append(one_chat)
        return all_chats
    
    @classmethod
    def get_all_by_group(cls,group_id):
        query = "SELECT * FROM conversations where group_id = %(group_id)s;"
        data = {
            "group_id": group_id
        }
        results = connectToMySQL(db).query_db(query, data)

        all_chats = []
        for row in results:
            one_chat = cls(row)
            all_chats.append(one_chat)
        
        return all_chats