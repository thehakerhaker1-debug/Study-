import sqlite3
from real_jobs import fetch_jobs

DB = "site.db"

def save_post(title, link, date):
conn = sqlite3.connect(DB)
cur = conn.cursor()

```
cur.execute("""
CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE,
    link TEXT,
    date TEXT
)
""")

try:
    cur.execute(
        "INSERT INTO posts(title, link, date) VALUES(?,?,?)",
        (title, link, date)
    )
    print("POST ADDED:", title)

except:
    print("DUPLICATE SKIPPED:", title)

conn.commit()
conn.close()
```

def run():
jobs = fetch_jobs()

```
for job in jobs:
    save_post(job["title"], job["link"], job["date"])
```

if **name** == "**main**":
run()
