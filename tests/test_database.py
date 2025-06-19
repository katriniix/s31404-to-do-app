from database.users import insert_user, find_user_by_nick
from database.tasks import add, get_for_user_date, set_done

def test_insert_and_find_user_direct():
    db = {"data": []}

    def insert(user_data):
        db["data"].append(user_data)

    def find(nick):
        for u in db["data"]:
            if u["nick"] == nick:
                return u

    user = {"nick": "katy", "password": "123"}
    insert(user)
    result = find("katy")

    assert result is not None
    assert result["nick"] == "katy"
    assert result["password"] == "123"

def test_add_and_get_task_simple():
    db = {"tasks": []}

    def add(title, date, color=""):
        db["tasks"].append({
            "title": title,
            "date": date,
            "done": False,
            "color": color
        })

    def get(date):
        return [t for t in db["tasks"] if t["date"] == date]

    add("do smth", "2025-06-22")
    result = get("2025-06-22")

    assert len(result) == 1
    assert result[0]["title"] == "do smth"
