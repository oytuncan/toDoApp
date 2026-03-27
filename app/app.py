from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

todos = []
counter = 1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    global counter
    data = request.get_json()
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "Boş todo eklenemez"}), 400
    todo = {
        "id": counter,
        "text": data["text"].strip(),
        "done": False,
        "created_at": datetime.now().strftime("%H:%M")
    }
    todos.append(todo)
    counter += 1
    return jsonify(todo), 201

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"ok": True})

@app.route("/todos/<int:todo_id>/toggle", methods=["PATCH"])
def toggle_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            return jsonify(todo)
    return jsonify({"error": "Bulunamadı"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)