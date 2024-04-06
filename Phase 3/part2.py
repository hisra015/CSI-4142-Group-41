# Group 41
# Michael Quach: 300177284
# Aleana Wright: 300196531
# Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')
cursor = conn.cursor()

#function to execute and print results of a query
def execute_and_print_query(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Check if 'staged_data' table exists, create if not
cursor.execute("SELECT to_regclass('public.staged_data')")
if cursor.fetchone()[0] is None:
    cursor.execute("""
        CREATE TABLE staged_data (
            ref_date INT,
            characteristics VARCHAR(255),
            value INT,
            "leading causes of death (ICD-10)" VARCHAR(255)
            -- Add other necessary columns as per your CSV file or requirements
        );
    """)
    conn.commit()
    print("Table 'staged_data' created.")
else:
    print("Table 'staged_data' exists.")

#iceberg query: find the five years with highest total number of deaths
iceberg_query = """
SELECT ref_date, SUM(value) AS total_deaths
FROM staged_data
WHERE characteristics = 'Number of deaths'
GROUP BY ref_date
ORDER BY total_deaths DESC
LIMIT 5;
"""
execute_and_print_query(cursor, iceberg_query)

#windowing query: rank leading causes of death by number of deaths for the most recent year
windowing_query = """
SELECT ref_date, "Leading causes of death (ICD-10)", value,
RANK() OVER (PARTITION BY ref_date ORDER BY value DESC) AS rank
FROM staged_data
WHERE characteristics = 'Number of deaths' AND ref_date = (SELECT MAX(ref_date) FROM staged_data)
ORDER BY ref_date, rank;
"""
execute_and_print_query(cursor, windowing_query)

#window clause: compare number of deaths in a year to previous and next years
window_clause_query = """
SELECT ref_date,
value AS deaths,
LAG(value, 1) OVER (ORDER BY ref_date) AS previous_year_deaths,
LEAD(value, 1) OVER (ORDER BY ref_date) AS next_year_deaths
FROM (
  SELECT ref_date, SUM(value) AS value
  FROM staged_data
  WHERE characteristics = 'Number of deaths'
  GROUP BY ref_date
) AS yearly_deaths
ORDER BY ref_date;
"""
execute_and_print_query(cursor, window_clause_query)

#close connection
conn.close()
