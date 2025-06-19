from database.db import db

def insert_user(user_data: dict):
    db.users.insert_one(user_data)

def find_user_by_nick(username: str):
    return db.users.find_one({"nick": username})
