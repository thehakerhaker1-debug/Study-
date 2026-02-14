from flask import Flask, request, redirect, render_template_string, session
from datetime import datetime
import sqlite3
import threading
import time
import os

app = Flask(__name__)
app.secret_key = "secret123"

ADMIN_PASSWORD = "admin123"
DB = "site.db"
visitor_count = 0

# ===============================
# HTML TEMPLATE
# ===============================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VNHHFJC5FN"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-VNHHFJC5FN');
</script>

<title>Latest Govt Job Updates 2025 | SSC Railway Police</title>
<meta name="description" content="Daily govt job updates SSC Railway Police Admit Card Result">
<meta name="keywords" content="govt job 2025, SSC GD, Railway Bharti, Police Bharti">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Arial;background:#f2f2f2;margin:0}
header{background:#1e90ff;color:white;padding:15px;text-align:center}
.menu{background:#333;padding:10px;text-align:center}
.menu a{color:white;margin:12px;text-decoration:none;font-weight:bold}
.container{padding:15px}
.card{background:white;padding:15px;margin-bottom:12px;border-radius:10px;box-shadow:0 0 5px #ccc}
.date{font-size:12px;color:gray}
.ad{text-align:center;margin:15px 0;background:#fff;padding:10px;border-radius:8px}
.counter{text-align:center;font-size:14px;color:#444;margin:10px}
footer{background:#222;color:white;text-align:center;padding:15px;margin-top:20px;font-size:14px}
footer a{color:#ddd;margin:0 10px;text-decoration:none}
</style>
</head>
<body>
<header>
<h2>📚 Govt Job & Exam Updates</h2>
<p>SSC • Railway • Police • UPSC • Post Office • Results</p>
</header>
<div class="menu">
<a href="/">Home</a>
<a href="/about">About</a>
<a href="/privacy">Privacy</a>
<a href="/contact">Contact</a>
<a href="/admin">Admin</a>
</div>
<div class="counter">
👀 Total Visitors: {{visitors}}
</div>
<div class="container">
<div class="ad">Top Ad Space</div>
{% for u in updates %}
<div class="card">
<h3>{{u.title}}</h3>
<p>Apply Here: <a href="{{u.link}}" target="_blank">{{u.link}}</a></p>
<span class="date">Updated: {{u.date}}</span>
</div>
{% endfor %}
<div class="ad">Middle Ad Space</div>
<div class="ad">Bottom Ad Space</div>
</div>
<footer>
<p>
<a href="/">Home</a> |
<a href="/about">About</a> |
<a href="/privacy">Privacy</a> |
<a href="/contact">Contact</a>
</p>
<p>© 2025 Study Updates. All Rights Reserved.</p>
</footer>
</body>
</html>
"""


# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def home():
    global visitor_count
    visitor_count += 1

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, link TEXT, date TEXT)")
    cur.execute("SELECT title, link, date FROM posts ORDER BY id DESC")
    updates = [{"title": t[0], "link": t[1], "date": t[2]} for t in cur.fetchall()]
    conn.close()

    return render_template_string(HTML_TEMPLATE, updates=updates, visitors=visitor_count)

# ===============================
# ABOUT PAGE
# ===============================
@app.route("/about")
def about():
    return "<h2>About Us</h2><p>We provide latest government job updates, exam news, admit cards and results daily.</p><a href='/'>Back</a>"

# ===============================
# PRIVACY PAGE
# ===============================
@app.route("/privacy")
def privacy():
    return "<h2>Privacy Policy</h2><p>This site may use cookies and third-party ads like Google AdSense.</p><a href='/'>Back</a>"

# ===============================
# CONTACT PAGE
# ===============================
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        return f"<h3>Thank you {name}, your message received!</h3><a href='/'>Go Back</a>"
    return """
    <h2>Contact Us</h2>
    <form method="post">
        <input name="name" placeholder="Your Name" required><br><br>
        <textarea name="message" placeholder="Your Message" required></textarea><br><br>
        <button>Send Message</button>
    </form>
    <br><a href="/">Back</a>
    """

# ===============================
# ADMIN LOGIN
# ===============================
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method=="POST":
        if request.form["p"]==ADMIN_PASSWORD:
            session["a"]=True
            return redirect("/dash")
        else:
            return "Wrong Password"
    return '<h2>Admin Login</h2><form method=post><input type=password name=p placeholder=password><button>Login</button></form>'

# ===============================
# DASHBOARD
# ===============================
@app.route("/dash")
def dash():
    if not session.get("a"):
        return redirect("/admin")
    return '<h2>Add New Update</h2><form method=post action=/add><input name=title placeholder=Title><br><br><textarea name=content placeholder="Full Update"></textarea><br><br><button>Add</button></form><br><a href="/logout">Logout</a>'

# ===============================
# ADD POST
# ===============================
@app.route("/add", methods=["POST"])
def add():
    if not session.get("a"):
        return redirect("/admin")

    title = request.form["title"]
    content = request.form["content"]
    date = datetime.now().strftime("%d %b %Y")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, link TEXT, date TEXT)")

    try:
        cur.execute("INSERT INTO posts(title, link, date) VALUES(?,?,?)", (title, content, date))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Duplicate post skipped")
    conn.close()
    return redirect("/")

# ===============================
# LOGOUT
# ===============================
@app.route("/logout")
def logout():
    session.pop("a",None)
    return redirect("/")

# ===============================
# AUTO CONTENT SYSTEM
# ===============================
def auto_worker():
    from autopost import fetch_real_jobs, save_jobs

    while True:
        print("Fetching real government jobs...")
        try:
            jobs = fetch_real_jobs()
            save_jobs(jobs)
            print(f"{len(jobs)} new posts saved.")
        except Exception as e:
            print(f"Error in auto fetch: {e}")
        print("Next run after 6 hours...")
        time.sleep(21600)  # 6 hours

t = threading.Thread(target=auto_worker)
t.daemon = True
t.start()

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
