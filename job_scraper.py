import json
import urllib.request
import csv

company = "stripe"
url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

with urllib.request.urlopen(url) as response:
    data = json.load(response)

seen_file = "seen_jobs.txt"

try:
    with open(seen_file, "r") as file:
        seen_jobs = set(file.read().splitlines())
except FileNotFoundError:
    seen_jobs = set()

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
new_jobs = []

for job in jobs:
    title = job["title"]
    location = job["location"]["name"]
    link = job["absolute_url"]
    job_id = str(job["id"])

    title_lower = title.lower()

    include_match = any(word in title_lower for word in include_keywords)
    exclude_match = any(word in title_lower for word in exclude_keywords)

    if include_match and not exclude_match:
        matches += 1
        matching_jobs.append([title, location, link])

        if job_id not in seen_jobs:
            new_jobs.append([title, location, link])
            seen_jobs.add(job_id)

            print("NEW JOB:", title)
            print("Location:", location)
            print("Link:", link)
            print("-" * 40)

print()
print("Matching jobs found:", matches)
print("New jobs found:", len(new_jobs))

with open(seen_file, "w") as file:
    for job_id in seen_jobs:
        file.write(job_id + "\n")

with open("stripe_product_jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Location", "Link"])
    writer.writerows(matching_jobs)

with open("stripe_new_jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Location", "Link"])
    writer.writerows(new_jobs)

print("CSV file created: stripe_product_jobs.csv")
print("CSV file created: stripe_new_jobs.csv")