# Job Scraper

A Python-based job scraper that pulls listings from Greenhouse APIs, filters for relevant roles, and exports structured job data to CSV.

---

## 🚀 Features

- Pulls job listings from Greenhouse-hosted company boards
- Filters roles based on keyword matching
- Excludes irrelevant job categories (e.g. sales, marketing)
- Displays matching jobs in the console
- Exports results to a CSV file

---

## 🧰 Tech Stack

- Python
- JSON (API responses)
- urllib (API requests)
- CSV (data export)

---

## 📊 Current Functionality

- Fetch jobs from a single company (currently: Stripe)
- Filter for product-related roles:
  - Product Manager
  - Product Lead
  - Product Management
- Export results to:
  stripe_product_jobs.csv
---

## ▶️ How to Run

1. Make sure Python is installed
2. Run the script:

```bash
python main.py
```
 3. View output:
	- Matching jobs will print in the console
	- A CSV file will be created with results

## 🧠 Example Output
```
Title: Product Manager
Location: New York
Link: https://...
----------------------------------------
```
---
## 🔮 Next Steps
- Support multiple companies
- Add job posting date (created_at)
- Detect remote roles
- Improve filtering logic
- Add configuration options

---
## 💡 Purpose
This project is part of my transition into more technical product roles, focusing on:
-	API integration
-	data extraction
-	automation workflows
-	real-world problem solving
---

## 👤 Author
Scott DeForest
