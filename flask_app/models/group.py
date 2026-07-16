from flask_app.config.mysqlconnection import connectToMySQL

db = 'ai_app'

class Group:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.group_number = data['group_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.conversations = []
        self.user = None



   # Saving Groups
    @classmethod
    def save_group(cls, data):
        query = "INSERT INTO `groups` (title, group_number, created_at, user_id) VALUES (%(title)s, %(group_number)s, NOW(), %(user_id)s);"
        results = connectToMySQL(db).query_db(query, data)
        if results is False:
            print("Error occurred while saving group data.")
        return results
    
    @classmethod
    def get_all_by_user(cls, user_id):
        query = "SELECT * FROM `groups` WHERE user_id = %(user_id)s;"
        data = {
            "user_id": user_id
        }

        results = connectToMySQL(db).query_db(query, data)

        all_groups = []

        for row in results:
            one_group = cls(row)
            all_groups.append(one_group)

        return all_groups
    

    #Grabbing one chat   
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM `groups` WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])
    

    @classmethod
    def get_next_group_number(cls, user_id):
        query = "SELECT MAX(group_number) AS group_number FROM `groups` WHERE user_id = %(user_id)s"
        data = {
            "user_id": user_id
        }

        results = connectToMySQL(db).query_db(query, data)
        print("RESELT FROM GROUP NMBER:", results)
        
        if results[0]['group_number'] is None:
            return 1

        return int(results[0]['group_number']) + 1
    

    # Updating User Information
    @classmethod
    def rename_group(cls, data, id):
        query = "UPDATE `groups` SET title = %(title)s, updated_at = NOW() WHERE id = %(id)s;"
        data['id'] = id
        connectToMySQL(db).query_db(query, data)
        results = connectToMySQL(db).query_db(query, data)
        return results
        


    @classmethod
    def delete(cls, group_id):
        query = "DELETE FROM `groups` WHERE id = %(id)s;"
        data = {
            "id": group_id
        }
        return connectToMySQL(db).query_db(query, data)