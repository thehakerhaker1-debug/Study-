# Different job words
dept = ["SSC", "Railway", "Police", "Army", "Teacher", "Post Office", "Anganwadi"]
type_ = ["Bharti", "Vacancy", "Recruitment", "Form", "Job", "Notification"]
year = "2025"

print("\n====== BULK SEO TITLES ======\n")

count = 1
for d in dept:
    for t in type_:
        print(f"{count}. {d} {t} {year} Apply Online")
        count += 1
