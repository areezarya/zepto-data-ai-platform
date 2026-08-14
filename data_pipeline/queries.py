"""
Task 5 SQL Queries

Covers:
1. SELECT + WHERE
2. ORDER BY
3. LIMIT
4. DISTINCT
5. BETWEEN
6. JOIN
"""

import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("books.db")

# Query 1 - SELECT + WHERE
query1 = """
SELECT title, rating
FROM books
WHERE rating = 5
"""

# Query 2 - ORDER BY
query2 = """
SELECT title, price_inr
FROM books
ORDER BY price_inr DESC
"""

# Query 3 - LIMIT
query3 = """
SELECT *
FROM books
LIMIT 10
"""

# Query 4 - DISTINCT
query4 = """
SELECT DISTINCT rating
FROM books
"""

# Query 5 - BETWEEN
query5 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 40
"""

# Query 6 - JOIN
query6 = """
SELECT
    b.title,
    b.rating,
    c.category_name
FROM books b
JOIN categories c
ON b.category_id = c.category_id
"""

# Execute Queries

result1 = pd.read_sql(query1, conn)
result2 = pd.read_sql(query2, conn)
result3 = pd.read_sql(query3, conn)
result4 = pd.read_sql(query4, conn)
result5 = pd.read_sql(query5, conn)
result6 = pd.read_sql(query6, conn)

# Print Results

print("\nQUERY 1 - 5 Star Books")
print(result1.head())

print("\nQUERY 2 - Highest Price Books")
print(result2.head())

print("\nQUERY 3 - First 10 Books")
print(result3.head())

print("\nQUERY 4 - Distinct Ratings")
print(result4)

print("\nQUERY 5 - Books Between £20 and £40")
print(result5.head())

print("\nQUERY 6 - JOIN Result")
print(result6.head())

conn.close()