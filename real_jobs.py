import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.freejobalert.com/"

def fetch_jobs():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    posts = []

    for link in soup.find_all("a")[:20]:
        title = link.text.strip()
        href = link.get("href")

        if len(title) > 25 and "2025" in title:
            posts.append({
                "title": title,
                "link": href,
                "date": datetime.now().strftime("%d %b %Y")
            })

    return posts

if __name__ == "__main__":
    jobs = fetch_jobs()

    print("\n====== REAL GOVT JOB POSTS ======\n")
    for job in jobs:
        print("TITLE:", job["title"])
        print("LINK:", job["link"])
        print("DATE:", job["date"])
        print("-----------------------------")
