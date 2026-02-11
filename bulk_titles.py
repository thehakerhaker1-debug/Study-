# bulk_titles.py

def generate_titles():
    dept = ["SSC", "Railway", "Police", "Army", "Teacher", "Post Office", "Anganwadi"]
    type_ = ["Bharti", "Vacancy", "Recruitment", "Form", "Job", "Notification"]
    year = "2025"

    titles = []
    for d in dept:
        for t in type_:
            titles.append(f"{d} {t} {year} Apply Online")
    return titles

# Optional: test run
if __name__ == "__main__":
    titles = generate_titles()
    print("\n====== BULK SEO TITLES ======\n")
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
