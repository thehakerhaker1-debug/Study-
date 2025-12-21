from flask import Flask, request, redirect, render_template_string, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_secret_key_123"   # change later

# 🔐 ADMIN PASSWORD
ADMIN_PASSWORD = "admin123"   # <<< CHANGE THIS

# 📦 DATA STORAGE (Render free me temporary hota hai)
updates = [
    {
        "id": 1,
        "title": "🔥 SSC GD Exam Update",
        "content": "SSC GD 2025 notification expected soon.",
        "date": "Today"
    },
    {
        "id": 2,
        "title": "📢 Railway Group D",
        "content": "Railway Group D form date announced.",
        "date": "Yesterday"
    }
]

# 🌐 PUBLIC PAGE
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Study Updates</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#f2f2f2;margin:0}
header{background:#1e90ff;color:white;padding:15px;text-align:center}
.container{padding:15px}
.card{background:white;padding:15px;margin-bottom:10px;border-radius:8px}
.date{font-size:12px;color:gray}
a{color:white;text-decoration:none}
</style>
</head>
<body>

<header>
<h2>📚 Study & Exam Updates</h2>
<p>Latest jobs • exams • results</p>
<a href="/admin">Admin Login</a>
</header>

<div class="container">
{% for u in updates %}
<div class="card">
<h3>{{u.title}}</h3>
<p>{{u.content}}</p>
<span class="date">Updated: {{u.date}}</span>
</div>
{% endfor %}
</div>

</body>
</html>
""", updates=updates)

# 🔐 ADMIN LOGIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/dashboard")
        else:
            return "Wrong Password ❌"

    return """
    <h2>Admin Login</h2>
    <form method="post">
        <input type="password" name="password" placeholder="Password">
        <button>Login</button>
    </form>
    """

# 📊 ADMIN DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    return render_template_string("""
<h2>Admin Dashboard</h2>

<form method="post" action="/add">
<input name="title" placeholder="Title"><br><br>
<textarea name="content" placeholder="Update content"></textarea><br><br>
<button>Add Update</button>
</form>

<hr>

<h3>All Updates</h3>
{% for u in updates %}
<p>
<b>{{u.title}}</b>
<a href="/delete/{{u.id}}">❌ Delete</a>
</p>
{% endfor %}

<a href="/logout">Logout</a>
""", updates=updates)

# ➕ ADD UPDATE
@app.route("/add", methods=["POST"])
def add():
    if not session.get("admin"):
        return redirect("/admin")

    new_id = updates[-1]["id"] + 1 if updates else 1
    updates.insert(0, {
        "id": new_id,
        "title": request.form["title"],
        "content": request.form["content"],
        "date": datetime.now().strftime("%d %b %Y")
    })
    return redirect("/dashboard")

# ❌ DELETE UPDATE
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect("/admin")

    global updates
    updates = [u for u in updates if u["id"] != id]
    return redirect("/dashboard")

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
