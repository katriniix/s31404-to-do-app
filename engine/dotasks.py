from database import tasks

def add_task(username: str, title: str, date: str, color: str):
    if not title.strip():
        return False, "Title is empty"
    task_data = {
        "user": username,
        "title": title.strip(),
        "date": date,
        "color": color,
        "done": False,
    }
    tasks.add(task_data)
    return True, "Task added"

def get_tasks(username: str, date: str):
    return tasks.get_for_user_date(username, date)

def toggle_done(task_id: str, is_done: bool):
    tasks.set_done(task_id, is_done)
