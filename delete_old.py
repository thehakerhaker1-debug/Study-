import sqlite3
from datetime import datetime, timedelta

DB = "site.db"

def delete_old():
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

# 30 din purani posts delete
limit_date = datetime.now() - timedelta(days=30)
limit_date = limit_date.strftime("%d %b %Y")

cur.execute("DELETE FROM posts WHERE date < ?", (limit_date,))
conn.commit()
conn.close()

print("Old posts deleted")
```

if **name** == "**main**":
delete_old()
