import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DB = "site.db"

URL = "https://www.freejobalert.com/latest-notifications/"

def fetch_real_jobs():
    jobs = []

    try:
        r = requests.get(URL, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a"):
            title = a.text.strip()
            link = a.get("href")

            if not title or not link:
                continue

            # Sirf sarkari keywords
            keywords = [
                "Recruitment",
                "Vacancy",
                "Notification",
                "Apply",
                "Posts",
                "Admit Card",
                "Result"
            ]

            if any(k.lower() in title.lower() for k in keywords):

                if link.startswith("/"):
                    link = "https://www.freejobalert.com" + link

                jobs.append({
                    "title": title,
                    "link": link,
                    "date": datetime.now().strftime("%d %b %Y")
                })

    except Exception as e:
        print("Error:", e)

    return jobs


def save_jobs(jobs):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        link TEXT,
        date TEXT
    )
    """)

    count = 0

    for job in jobs:
        try:
            cur.execute(
                "INSERT INTO posts(title, link, date) VALUES(?,?,?)",
                (job["title"], job["link"], job["date"])
            )
            count += 1
        except:
            pass

    conn.commit()
    conn.close()

    print(f"{count} REAL jobs saved.")
