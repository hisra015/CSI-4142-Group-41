# Group 41
# Michael Quach: 300177284
# Aleana Wright: 300196531
# Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')
cursor = conn.cursor()

# Function to execute and print results of a query
def execute_and_print_query(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

#iceberg query: find the five years with highest total number of deaths
iceberg_query = """
SELECT "REF_DATE", SUM("VALUE") AS total_deaths
FROM staged_data
WHERE "Characteristics" = 'Number of deaths'
GROUP BY "REF_DATE"
ORDER BY total_deaths DESC
LIMIT 5;
"""
execute_and_print_query(cursor, iceberg_query)

#windowing query: rank leading causes of death by number of deaths for the most recent year
windowing_query = """
SELECT "REF_DATE", "Leading causes of death (ICD-10)", "VALUE",
RANK() OVER (PARTITION BY "REF_DATE" ORDER BY "VALUE" DESC) AS rank
FROM staged_data
WHERE "Characteristics" = 'Number of deaths' AND "REF_DATE" = (SELECT MAX("REF_DATE") FROM staged_data)
ORDER BY "REF_DATE", rank;
"""
execute_and_print_query(cursor, windowing_query)

#window clause: compare number of deaths in a year to previous and next years
window_clause_query = """
SELECT "REF_DATE",
"VALUE" AS deaths,
LAG("VALUE", 1) OVER (ORDER BY "REF_DATE") AS previous_year_deaths,
LEAD("VALUE", 1) OVER (ORDER BY "REF_DATE") AS next_year_deaths
FROM (
  SELECT "REF_DATE", SUM("VALUE") AS "VALUE"
  FROM staged_data
  WHERE "Characteristics" = 'Number of deaths'
  GROUP BY "REF_DATE"
) AS yearly_deaths
ORDER BY "REF_DATE";
"""
execute_and_print_query(cursor, window_clause_query)

#close connection
conn.close()
