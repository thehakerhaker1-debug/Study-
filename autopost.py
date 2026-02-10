from datetime import datetime
import random

# Job categories
jobs = [
    "SSC GD Bharti 2025",
    "Railway Group D Vacancy 2025",
    "Police Constable Recruitment 2025",
    "Post Office Recruitment 2025",
    "Army Rally Bharti 2025",
    "Teacher Vacancy 2025",
    "Anganwadi Bharti 2025",
    "10th Pass Govt Job 2025",
    "12th Pass Govt Job 2025"
]

# Extra lines to make content look different
lines = [
    "Online application form shuru ho chuka hai.",
    "Interested candidates official website par apply kar sakte hain.",
    "Last date jald hi announce ki jayegi.",
    "Selection process me exam aur document verification hoga.",
    "Form bharne se pehle official notification jarur padhe."
]

def generate_post():
    job = random.choice(jobs)
    title = job + " Apply Online"

    # 2–3 random lines se content banega
    content = f"{job} ke liye notification release ho gaya hai. " + " ".join(random.sample(lines, 3))
    date = datetime.now().strftime("%d %b %Y")

    return title, content, date

print("\n====== AUTO POSTS READY ======\n")

# Roz ke liye 5 posts generate
for i in range(5):
    t, c, d = generate_post()
    print("TITLE:", t)
    print("CONTENT:", c)
    print("DATE:", d)
    print("------------------------------")
