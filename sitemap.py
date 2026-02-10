site = "https://your-site.onrender.com"

pages = [
    "/",
    "/about",
    "/privacy",
    "/contact"
]

print("\n====== SITEMAP.XML ======\n")
print("<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>")

for p in pages:
    print("  <url>")
    print(f"    <loc>{site}{p}</loc>")
    print("  </url>")

print("</urlset>")
