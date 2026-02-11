import sqlite3
from datetime import datetime, timedelta

DB = "site.db"
DAYS_TO_KEEP = 30  # 30 din se purani posts delete

def delete_old_posts():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT UNIQUE, link TEXT, date TEXT)")

    # Purani date calculate
    cutoff = datetime.now() - timedelta(days=DAYS_TO_KEEP)
    cutoff_str = cutoff.strftime("%d %b %Y")

    # SQLite me date comparison ke liye string ko datetime me convert karenge
    cur.execute("SELECT id, date FROM posts")
    to_delete = []
    for row in cur.fetchall():
        post_id, date_str = row
        try:
            post_date = datetime.strptime(date_str, "%d %b %Y")
            if post_date < cutoff:
                to_delete.append(post_id)
        except:
            continue

    for post_id in to_delete:
        cur.execute("DELETE FROM posts WHERE id=?", (post_id,))
        print(f"Deleted old post ID {post_id}")

    conn.commit()
    conn.close()
    print(f"{len(to_delete)} old posts deleted.")

if __name__ == "__main__":
    delete_old_posts()
