import json
import urllib.request
import csv

company = "stripe"
url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

with urllib.request.urlopen(url) as response:
    data = json.load(response)

jobs = data["jobs"]

include_keywords = ["product manager", "product lead", "product management"]
exclude_keywords = [
    "sales",
    "account executive",
    "marketing",
    "recruiter",
    "partner",
    "designer",
    "design",
    "counsel",
    "accounting",
    "support",
    "operations",
]

print("Total jobs found:", len(jobs))
print()

matches = 0
matching_jobs = []

for job in jobs:
    title = job["title"]
    location = job["location"]["name"]
    link = job["absolute_url"]

    title_lower = title.lower()

    include_match = any(word in title_lower for word in include_keywords)
    exclude_match = any(word in title_lower for word in exclude_keywords)

    if include_match and not exclude_match:
        matches += 1
        matching_jobs.append([title, location, link])

        print("Title:", title)
        print("Location:", location)
        print("Link:", link)
        print("-" * 40)

print()
print("Matching jobs found:", matches)

with open("stripe_product_jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Location", "Link"])
    writer.writerows(matching_jobs)

print("CSV file created: stripe_product_jobs.csv")