from bson import ObjectId
from database.db import db

def add(task_data: dict):
    return db.tasks.insert_one(task_data).inserted_id

def get_for_user_date(username: str, date: str) -> list[dict]:
    cursor = db.tasks.find({"user": username, "date": date}).sort(
        [("done", 1), ("_id", 1)]
    )
    return [{**task, "_id": str(task["_id"])} for task in cursor]

def set_done(task_id: str, is_done: bool) -> bool:
    result = db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": {"done": bool(is_done)}},
    )
    return bool(result.matched_count)
