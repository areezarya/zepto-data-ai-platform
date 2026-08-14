# Data Pipeline Module

## Fixed Conversion Rate

1 GBP = 105.50 INR

## Run Instructions

pip install -r requirements.txt
python scrape_and_load.py

## Cleaning Decisions

- Removed currency symbols from prices.
- Converted ratings from text to integers.
- Converted availability to boolean.
- Numeric parsing issues handled using median imputation.
- Dataset scraped from 3 categories and contains more than 60 books.

## Database Schema

categories(category_id, category_name)

books(
 book_id,
 title,
 price_gbp,
 price_inr,
 rating,
 in_stock,
 category_id
)
