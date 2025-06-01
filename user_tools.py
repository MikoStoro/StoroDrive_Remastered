from tinydb import TinyDB, Query
import os
import uuid
import file_tools as FTools
users_db_path = os.path.abspath("./databases/users.json")

db = TinyDB(users_db_path)

def user_exists(username):
    User = Query()
    return db.contains(User.username == username)

def check_password(username, password):
    db = TinyDB(users_db_path)
    return get_user(username)['pswd_hash'] == password

def get_user(username):
    User = Query()
    return db.get(User.username == username)

def create_user(username, password):
    user_entry = {
        'username': username, 
        'pswd_hash': password, 
        'catalogue': str(uuid.uuid1()), 
        'user_id': str(uuid.uuid1())
    }
    db.insert(user_entry)
    catalogue_name = username
    FTools.create_catalogue(user_entry['catalogue'], catalogue_name)
    return user_entry