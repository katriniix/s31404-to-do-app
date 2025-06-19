
def test_register_user_direct():
    users = []

    def insert_user(user_data):
        users.append(user_data)

    def find_user_by_nick(nick):
        for user in users:
            if user["nick"] == nick:
                return user

    def register_user(username, password):
        if find_user_by_nick(username):
            return False, "User already exists"
        insert_user({"nick": username, "password": password})
        return True, "User created"

    def check_credentials(username, password):
        user = find_user_by_nick(username)
        return bool(user and user["password"] == password)

    ok, msg = register_user("katy", "123")
    assert ok is True
    assert msg == "User created"

    ok, msg = register_user("katy", "123")
    assert ok is False
    assert msg == "User already exists"

    assert check_credentials("katy", "123") is True
    assert check_credentials("katy", "wrong") is False

def test_add_get_toggle_task_direct():
    tasks = []

    def add_task(user, title, date, color):
        if not title.strip():
            return False, "Title is empty"
        task = {
            "user": user,
            "title": title.strip(),
            "date": date,
            "color": color,
            "done": False
        }
        tasks.append(task)
        return True, "Task added"

    def get_tasks(user, date):
        return [t for t in tasks if t["user"] == user and t["date"] == date]

    def toggle_done(index):
        tasks[index]["done"] = not tasks[index]["done"]

    ok, _ = add_task("katy", "do smth", "2025-06-22", "")
    assert ok is True

    ok, _ = add_task("katy", " ", "2025-06-22", "")
    assert ok is False

    result = get_tasks("katy", "2025-06-22")
    assert len(result) == 1
    assert result[0]["title"] == "do smth"
    assert result[0]["done"] is False

    toggle_done(0)
    assert result[0]["done"] is True
