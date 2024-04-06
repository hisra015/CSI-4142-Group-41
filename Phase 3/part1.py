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
#Description: Drill Down on Deaths by State within a Country over a Specific Year Range
sql = """ 
SELECT y.year, g.country, g.state, COUNT(f.death_number) as death_count
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
WHERE y.year BETWEEN 2019 AND 2021 AND g.country = 'Canada'
GROUP BY y.year, g.country, g.state
ORDER BY y.year, g.country, g.state;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDrill Down (From Country to State) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")

#Roll Up (From State to Country) Query
#Description: Roll Up to Show Total Deaths by Country over Years
sql = """ 
SELECT y.year, g.country, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
GROUP BY y.year, g.country
ORDER BY y.year, g.country;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nRoll Up (From State to Country) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")
#------------------------------------------------------------------

#PART B
#------------------------------------------------------------------
#Slice (Selecting one year) Query
#Description: Slice to Show Deaths for the Year 2020 across All Countries
sql = """ 
SELECT y.year, g.country, g.state, d.age_range, c.death_description, f.death_number
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
JOIN demographic_dimension d ON f.demographic_key = d.demographic_key
JOIN cause_of_death_dimension c ON f.cause_key = c.death_key
WHERE y.year = 2020;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nSlice (Selecting one year) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")
#------------------------------------------------------------------

#PART C
#------------------------------------------------------------------
#Dice (Sub-cube by Year and Country for two specific causes) Query
#Description: Dice to Analyze Deaths by Cause in Canada and United States for a Range of Years
sql = """ 
SELECT y.year, g.country, d.age_range, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN geography_dimension g ON f.geographic_key = g.geography_key
JOIN demographic_dimension d ON f.demographic_key = d.demographic_key
JOIN year_dimension y ON f.year_key = y.surrogate_pk
GROUP BY y.year, g.country, d.age_range
ORDER BY y.year, g.country, d.age_range;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDice (Sub-cube by Year and Country for two specific causes) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")

#Dice (Sub-cube across all Age Range across all years) Query
#Description: Dice to Analyze Deaths for all Age Ranges Across Countries in a Year
sql = """ 
SELECT y.year, g.country, d.age_range, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN geography_dimension g ON f.geographic_key = g.geography_key
JOIN demographic_dimension d ON f.demographic_key = d.demographic_key
JOIN year_dimension y ON f.year_key = y.surrogate_pk
GROUP BY y.year, g.country, d.age_range
ORDER BY y.year, g.country, d.age_range;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDice (Sub-cube for a specific Age Range across all years) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")
#------------------------------------------------------------------

#PART D
#------------------------------------------------------------------
#Drill Down within a Slice (Year and Country) Query
sql = """ 
SELECT y.year, g.country, g.state, c.death_description, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
JOIN cause_of_death_dimension c ON f.cause_key = c.death_key
WHERE y.year = 2020 AND g.country = 'Canada'
GROUP BY y.year, g.country, g.state, c.death_description
ORDER BY g.state, c.death_description;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDrill Down within a Slice (Year and Country) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")

#Dice and Roll Up (Specific cause of death across countries) Query
sql = """ 
SELECT y.year, g.country, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
GROUP BY y.year, g.country
ORDER BY y.year, g.country;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDice and Roll Up (Specific cause of death across countries) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")

#Slice and Dice (Specific demographics across countries) Query
sql = """ 
SELECT y.year, g.country, d.sex, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
JOIN demographic_dimension d ON f.demographic_key = d.demographic_key
GROUP BY y.year, g.country, d.sex
ORDER BY y.year, g.country, d.sex;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nSlice and Dice (Specific demographics across countries) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")

#Drill Down and Dice (States and Causes in a Year) Query
sql = """ 
SELECT y.year, g.state, SUM(f.death_number) as total_deaths
FROM fact_table f
JOIN year_dimension y ON f.year_key = y.surrogate_pk
JOIN geography_dimension g ON f.geographic_key = g.geography_key
WHERE y.year BETWEEN 2019 AND 2021
GROUP BY y.year, g.state
ORDER BY y.year, g.state;
""" 
cursor.execute(sql)
rows = cursor.fetchall()
print("\nDrill Down and Dice (States and Causes in a Year) Query")
if(rows):
    for i in range(3):
        print(rows[i])
else:
    print("No Data :(")
#------------------------------------------------------------------

