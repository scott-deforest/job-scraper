# Job Scraper

A Python-based job scraper that pulls listings from public Greenhouse job board APIs, filters for relevant product roles, tracks newly posted jobs, and automatically delivers results via CSV and email notifications.

## Overview
This project was built as a practical way to monitor product management job postings across multiple companies without manually checking each careers page.

The script pulls live job data, filters it based on role relevance and location, and identifies only newly posted jobs since the last run.

## Features
- Pulls job listings from multiple Greenhouse company boards
- Filters for product-focused roles such as:
  - Product Manager
  - Product Lead
  - Product Management
- Excludes irrelevant roles (sales, marketing, recruiting, design, etc.)
- Filters for:
  - US remote roles
  - Greater Philadelphia area roles
- Tracks previously seen jobs to detect new postings
- Exports results to CSV:
  - `product_jobs.csv` — all current matching jobs
  - `new_jobs.csv` — only newly detected jobs since last run
- Sorts output by company and title for easier review
- Automated daily execution using `launchd`
- Email notifications for newly detected jobs
- Includes scaffolded support for Lever job boards (future expansion)

## Automation
This scraper is configured to run automatically each day using macOS `launchd`.
- Runs daily at 8:00 AM
- Wakes the system if needed
- Updates job listings and detects new postings
- Sends an email notification when new roles are found

## How It Works
1. Fetch job listings from company job boards via API
2. Parse JSON responses into structured data
3. Apply role-based and location-based filtering
4. Compare results against previously seen job IDs
5. Output results to CSV files

## Tech Stack
- Python
- urllib (API requests)
- JSON (data parsing)
- CSV (data export)

## How to Run
Run the main script:

```bash
python job_scraper.py
```
After running:
- New jobs will be printed to the console
- CSV files will be created/updated in the project directory
- New jobs will be sent as an email notification

## Why I Built This
This project was built to create a lightweight, customizable way to monitor product management roles across multiple companies without relying on traditional job boards or alerts.

Rather than building a complex system upfront, this was developed iteratively:
- start with a single company
- expand to multiple sources
- layer in filtering, persistence, and automation
- add notifications

This project also serves as a hands-on way to build practical Python skills, including:
- API interaction
- data parsing
- filtering logic
- file handling
- state tracking

## Future Improvements
- Expand support to additional job board platforms
- Improve location parsing and normalization
- Add job posting timestamps
- Attach CSV results to email notifications
- Automatically track invalid company tokens
- Support more flexible configuration as the project grows

## Author
Scott DeForest