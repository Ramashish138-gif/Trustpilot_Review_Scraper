# Trustpilot Review Scraper

Scrapes reviews from Trustpilot using Playwright + Next.js internal API.

## Features
- Extracts reviews, ratings, author, date, location
- Single browser session (fast + efficient)
- Auto-pagination through all available pages
- Saves all data to CSV using Pandas
- Works for any company on Trustpilot

## Important Note
Trustpilot allows maximum 10 pages (200 reviews) 
without login. Page 11+ requires authentication.
Login support coming soon.

## Tech Stack
- Python, Playwright, Requests, Pandas

## Usage
pip install playwright pandas requests
playwright install chromium
python TrustpilotReviewScraper.py

## Output
Creates CSV: {sku}_all_reviews.csv
Example: lendingclub.com_all_reviews.csv