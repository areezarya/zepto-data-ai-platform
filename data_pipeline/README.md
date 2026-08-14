# Data Pipeline Module

## Fixed Conversion Rate

1 GBP = 105.50 INR

## Run Instructions

pip install -r requirements.txt
python scrape\_and\_load.py

## Cleaning Decisions

* Removed currency symbols from prices.
* Converted ratings from text to integers.
* Converted availability to boolean.
* Numeric parsing issues handled using median imputation.
* Dataset scraped from 3 categories and contains more than 60 books.

## Database Schema

categories(category\_id, category\_name)

books(
book\_id,
title,
price\_gbp,
price\_inr,
rating,
in\_stock,
category\_id
)





\## Repository History



Feature branch workflow completed.

