from flask import Flask, render_template, request, redirect, session, jsonify
from engine.auth import register_user, check_credentials
from engine.dotasks import add_task, get_tasks, toggle_done
from dotenv import load_dotenv
import os, threading, webbrowser
from bson import ObjectId
from database import tasks

load_dotenv()
app = Flask(__name__, static_folder="ui", static_url_path="/ui", template_folder="ui")
app.secret_key = os.getenv("SECRET_KEY", "dev")


@app.route("/")
def root():
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["nick"]
        password = request.form["password"]
        success, msg = register_user(username, password)
        if success:
            return redirect("/login")
        return f"Error: {msg}"
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nick"]
        password = request.form["password"]
        if check_credentials(username, password):
            session["user"] = username
            return redirect("/todo")
        return "Wrong username or password"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/todo")
def todo():
    if "user" not in session:
        return redirect("/login")
    return render_template("todo.html", user=session["user"])


@app.route("/api/tasks", methods=["GET", "POST", "PATCH"])
def tasks_api():
    if "user" not in session:
        return {"error": "unauthorized"}, 401
    username = session["user"]

    if request.method == "GET":
        date = request.args.get("date")
        return jsonify(get_tasks(username, date))

    data = request.get_json()

    if request.method == "POST":
        title = data.get("title", "").strip()
        date = data.get("date")
        color = data.get("color", "#33aaff")
        success, msg = add_task(username, title, date, color)
        return {"ok": success, "msg": msg}, (201 if success else 400)

    if request.method == "PATCH":
        task_id = data["_id"]
        is_done = data["done"]
        toggle_done(task_id, is_done)
        return {"ok": True}


@app.get("/api/tasks")
def api_tasks_list():
    if "user" not in session:
        return jsonify(error="unauthorized"), 401
    date = request.args.get("date")
    if not date:
        return jsonify(error="no date"), 400
    data = tasks.get_for_user_date(session["user"], date)
    return jsonify(data)


@app.post("/api/tasks")
def api_tasks_add():
    if "user" not in session:
        return jsonify(error="unauthorized"), 401
    js = request.get_json(force=True, silent=True) or {}
    title = (js.get("title") or "").strip()
    date = js.get("date")
    color = js.get("color", "")
    if not title or not date:
        return jsonify(error="bad data"), 400
    tasks.add({
        "user": session["user"],
        "title": title,
        "date": date,
        "color": color,
        "done": False
    })
    return jsonify(ok=True), 201


@app.patch("/api/tasks/<task_id>/toggle")
def api_tasks_toggle(task_id: str):
    js = request.get_json(force=True, silent=True) or {}
    is_done = bool(js.get("done", False))
    try:
        updated = tasks.set_done(task_id, is_done)
    except Exception:
        return jsonify(error="bad id"), 400
    if not updated:
        return jsonify(error="not found"), 404
    return ("", 204)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/login")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="0.0.0.0", debug=True, use_reloader=False)


