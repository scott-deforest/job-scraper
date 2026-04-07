# Job Scraper

A Python-based job scraper that pulls listings from public Greenhouse job board APIs, filters for relevant product roles, tracks newly posted jobs, and exports results to CSV.

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
- Includes scaffolded support for Lever job boards (future expansion)

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

## Why I Built This
This project was built to create a lightweight, customizable way to monitor product management roles across multiple companies without relying on job boards or alerts.

This project also serves as a hands-on way to build practical Python skills, including:
- API interaction
- data parsing
- filtering logic
- file handling
- state tracking

## Future Improvements
- Expand support beyond Greenhouse (Lever, etc.)
- Improve location parsing and normalization
- Add job posting timestamps
- Add email or scheduled alerts
- Externalize configuration (company lists, filters)

---

## Author
Scott DeForest
