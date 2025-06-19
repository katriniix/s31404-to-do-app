from database.users import insert_user, find_user_by_nick

def register_user(username: str, password: str):
    if find_user_by_nick(username):
        return False, "User already exists"
    insert_user({"nick": username, "password": password})
    return True, "User created"

def check_credentials(username: str, password: str) -> bool:
    user = find_user_by_nick(username)
    return bool(user and user["password"] == password)
