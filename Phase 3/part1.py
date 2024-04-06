#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database remotely
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')

cursor = conn.cursor()

#PART A
#------------------------------------------------------------------
#Drill Down (From Country to State) Query
sql = """ 
SELECT year, country, state, COUNT(*) as death_count
FROM staged_data
WHERE country = 'Canada'
GROUP BY year, country, state
ORDER BY year, state;
""" 
cursor.execute(sql)
conn.commit()

#Roll Up (From State to Country) Query
sql = """ 
SELECT year, country, SUM(death_number) as total_deaths
FROM staged_data
GROUP BY year, country
ORDER BY year, country;
""" 
cursor.execute(sql)
conn.commit()
#------------------------------------------------------------------

#PART B
#------------------------------------------------------------------
#Slice (Selecting one year) Query
sql = """ 
SELECT *
FROM staged_data
WHERE year = 2020;
""" 
cursor.execute(sql)
conn.commit()
#------------------------------------------------------------------

#PART C
#------------------------------------------------------------------
#Dice (Sub-cube by Year and Country for two specific causes) Query
sql = """ 
SELECT year, country, mortality_code, SUM(death_number) as total_deaths
FROM staged_data
WHERE year BETWEEN 2019 AND 2021 AND country IN ('Canada', 'United States') AND mortality_code IN ('A37', 'X85-Y09')
GROUP BY year, country, mortality_code;
""" 
cursor.execute(sql)
conn.commit()

#Dice (Sub-cube for a specific Age Range across all years) Query
sql = """ 
SELECT year, age_range, SUM(death_percentage) as total_death_percentage
FROM staged_data
WHERE age_range = '65-74'
GROUP BY year, age_range
ORDER BY year;
""" 
cursor.execute(sql)
conn.commit()
#------------------------------------------------------------------

#PART D
#------------------------------------------------------------------
#Drill Down within a Slice (Year and Country) Query
sql = """ 
SELECT year, country, state, death_description, SUM(death_number) as total_deaths
FROM staged_data
WHERE year = 2020 AND country = 'Canada'
GROUP BY year, country, state, death_description
ORDER BY state, death_description;
""" 
cursor.execute(sql)
conn.commit()

#Dice and Roll Up (Specific cause of death across countries) Query
sql = """ 
SELECT year, SUM(death_number) as total_deaths
FROM staged_data
WHERE country = 'Canada' AND mortality_code = 'A37'
GROUP BY year
ORDER BY year;
""" 
cursor.execute(sql)
conn.commit()

#Slice and Dice (Specific demographics across countries) Query
sql = """ 
SELECT year, country, sex, age_range, SUM(death_number) as total_deaths
FROM staged_data
WHERE sex = 'Both' AND age_range IN ('0-14', '15-24')
GROUP BY year, country, sex, age_range
ORDER BY year, country;
""" 
cursor.execute(sql)
conn.commit()

#Drill Down and Dice (States and Causes in a Year) Query
sql = """ 
SELECT year, state, mortality_code, SUM(death_number) as total_deaths
FROM staged_data
WHERE year = 2021 AND country = 'United States'
GROUP BY year, state, mortality_code
ORDER BY state, mortality_code;
""" 
cursor.execute(sql)
conn.commit()
#------------------------------------------------------------------

