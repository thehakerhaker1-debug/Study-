import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3

DB = "site.db"

# Official sources list
SOURCES = {
    "SSC": "https://ssc.nic.in/",
    "Railway": "https://indianrailways.gov.in/",
    "UPSC": "https://upsc.gov.in/",
    "Post Office": "https://www.indiapost.gov.in/",
    # Add more official URLs here
}

def fetch_jobs():
    posts = []
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.find_all("a")

            for link in links[:20]:  # top 20 links
                title = link.text.strip()
                href = link.get("href")
                if not title or "2025" not in title:
                    continue

                # Only sarkari keywords
                keywords = ["SSC", "Railway", "Police", "Army", "Teacher", "Post", "Anganwadi", "Recruitment", "Notification", "Form"]
                if any(k.lower() in title.lower() for k in keywords):
                    posts.append({
                        "title": title,
                        "link": href,
                        "date": datetime.now().strftime("%d %b %Y")
                    })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    return posts

def save_to_db(posts):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Table create
    cur.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        link TEXT,
        date TEXT
    )
    """)
    
    for job in posts:
        try:
            cur.execute(
                "INSERT INTO posts(title, link, date) VALUES (?,?,?)",
                (job["title"], job["link"], job["date"])
            )
            print(f"Added: {job['title']}")
        except sqlite3.IntegrityError:
            print(f"Duplicate skipped: {job['title']}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_to_db(jobs)
