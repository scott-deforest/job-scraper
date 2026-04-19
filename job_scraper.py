from email.quoprimime import quote
import json
import urllib.request
import urllib.error
import csv
from urllib.parse import quote
import os
import smtplib
from email.mime.text import MIMEText

os.makedirs("data", exist_ok=True)

from config import (
    greenhouse_companies,
    lever_companies,
    include_keywords,
    exclude_keywords,
    remote_keywords,
    local_keywords,
    email_enabled,
    email_recipient,
    email_subject,
)

seen_file = "data/seen_jobs.txt"


def load_seen_jobs(filename):
    try:
        with open(filename, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()


def save_seen_jobs(filename, seen_jobs):
    with open(filename, "w") as file:
        for job_id in seen_jobs:
            file.write(job_id + "\n")


def job_matches_filters(title, location):
    title_lower = title.lower()
    location_lower = location.lower()

    include_match = any(word in title_lower for word in include_keywords)
    exclude_match = any(word in title_lower for word in exclude_keywords)

    remote_match = any(word in location_lower for word in remote_keywords)
    local_match = any(word in location_lower for word in local_keywords)
    location_match = remote_match or local_match

    return include_match and not exclude_match and location_match


def write_csv(filename, rows):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Title", "Location", "Link"])
        writer.writerows(rows)

def send_email(rows):
    if not email_enabled or not rows:
        return

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        print("Email skipped: EMAIL_USER or EMAIL_PASS not set.")
        return

    body_lines = ["New product jobs found:", ""]

    for company, title, location, link in rows:
        body_lines.append(f"{company} - {title}")
        body_lines.append(location)
        body_lines.append(link)
        body_lines.append("")

    body = "\n".join(body_lines)

    msg = MIMEText(body)
    msg["Subject"] = email_subject
    msg["From"] = email_user
    msg["To"] = email_recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)

    print(f"Email sent to: {email_recipient}")


seen_jobs = load_seen_jobs(seen_file)

matches = 0
matching_jobs = []
new_jobs = []

for company in greenhouse_companies:
    url = f"https://boards-api.greenhouse.io/v1/boards/{quote(company.strip())}/jobs"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        print(f"Greenhouse - {company}: HTTP Error {e.code}")
        print("-" * 40)
        continue
    except urllib.error.URLError as e:
        print(f"Greenhouse - {company}: URL Error - {e.reason}")
        print("-" * 40)
        continue

    jobs = data["jobs"]
    print(f"Greenhouse - {company}: {len(jobs)} total jobs fetched")

    for job in jobs:
        title = job["title"]
        location = job["location"]["name"]
        link = job["absolute_url"]
        job_id = f"greenhouse_{company}_{job['id']}"

        if job_matches_filters(title, location):
            matches += 1
            matching_jobs.append([company, title, location, link])

            if job_id not in seen_jobs:
                new_jobs.append([company, title, location, link])
                seen_jobs.add(job_id)

                print("NEW JOB:", title)
                print("Location:", location)
                print("Link:", link)
                print("-" * 40)

for company in lever_companies:
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"

    try:
        with urllib.request.urlopen(url) as response:
            jobs = json.load(response)
    except urllib.error.HTTPError as e:
        print(f"Lever - {company}: HTTP Error {e.code}")
        print("-" * 40)
        continue
    except urllib.error.URLError as e:
        print(f"Lever - {company}: URL Error - {e.reason}")
        print("-" * 40)
        continue

    print(f"Lever - {company}: {len(jobs)} total jobs fetched")

    for job in jobs:
        title = job["text"]
        location = job["categories"]["location"]
        link = job["hostedUrl"]
        job_id = f"lever_{company}_{job['id']}"

        if job_matches_filters(title, location):
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

save_seen_jobs(seen_file, seen_jobs)

matching_jobs.sort(key=lambda job: (job[0].lower(), job[1].lower()))
new_jobs.sort(key=lambda job: (job[0].lower(), job[1].lower()))

product_file = "data/product_jobs.csv"
new_file = "data/new_jobs.csv"

write_csv(product_file, matching_jobs)
write_csv(new_file, new_jobs)

print(f"CSV file created: {product_file}")
print(f"CSV file created: {new_file}")

send_email(new_jobs)