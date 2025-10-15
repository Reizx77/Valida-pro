import os
import json
from flask import Flask, render_template, request, redirect, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
DB_PATH = "uploads.db.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================
# Banco JSON
# ======================
def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ======================
# Rotas
# ======================
@app.route("/")
def home():
    files = load_db()
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    author = request.form.get("author", "Anônimo")

    if not file:
        return redirect("/")

    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    data = load_db()
    data.append({
        "name": filename,
        "author": author,
        "status": "Pendente"
    })
    save_db(data)
    return redirect("/")

@app.route("/update/<name>/<status>")
def update_status(name, status):
    data = load_db()
    for f in data:
        if f["name"] == name:
            f["status"] = status.capitalize()
    save_db(data)
    return redirect("/")

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ======================
# Inicialização do app
# ======================
if __name__ == "__main__":
    app.run(debug=True)
