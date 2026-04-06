import json
import urllib.request
import urllib.error
import csv

companies = [
    "stripe",
    "coinbase",
    "airbnb",
    "hubspot",
    "datadog",
    "webflow",
    "mongodb",
    "okta",
    "affirm",
    "reddit",
    "discord",
    "instacart",
]

seen_file = "seen_jobs.txt"

try:
    with open(seen_file, "r") as file:
        seen_jobs = set(file.read().splitlines())
except FileNotFoundError:
    seen_jobs = set()

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

remote_keywords = [
    "us-remote",
    "us remote",
    "remote-us",
    "remote us",
    "united states remote",
    "remote - us",
    "usa remote",
    "remote (us)",
    "remote, us",
]

local_keywords = [
    "philadelphia",
    "king of prussia",
    "conshohocken",
    "malvern",
    "wayne",
    "radnor",
    "newtown square",
    "west chester",
    "plymouth meeting",
    "pennsylvania",
]

matches = 0
matching_jobs = []
new_jobs = []

for company in companies:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        print(f"{company}: HTTP Error {e.code}")
        print("-" * 40)
        continue
    except urllib.error.URLError as e:
        print(f"{company}: URL Error - {e.reason}")
        print("-" * 40)
        continue

    jobs = data["jobs"]
    print(f"{company}: {len(jobs)} total jobs fetched")

    for job in jobs:
        title = job["title"]
        location = job["location"]["name"]
        link = job["absolute_url"]
        job_id = f"{company}_{job['id']}"

        title_lower = title.lower()
        location_lower = location.lower()

        include_match = any(word in title_lower for word in include_keywords)
        exclude_match = any(word in title_lower for word in exclude_keywords)

        remote_match = any(word in location_lower for word in remote_keywords)
        local_match = any(word in location_lower for word in local_keywords)
        location_match = remote_match or local_match

        if include_match and not exclude_match and location_match:
            matches += 1
            matching_jobs.append([company, title, location, link])

            if job_id not in seen_jobs:
                new_jobs.append([company, title, location, link])
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

with open("product_jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Title", "Location", "Link"])
    writer.writerows(matching_jobs)

with open("new_jobs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Title", "Location", "Link"])
    writer.writerows(new_jobs)

print("CSV file created: product_jobs.csv")
print("CSV file created: new_jobs.csv")