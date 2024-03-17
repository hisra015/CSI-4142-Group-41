#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database remotely
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')

cursor = conn.cursor()


#------------------Create all the tables here--------------------------

#Create Time Dimension table if it doesn't exist
sql = """ 
CREATE TABLE IF NOT EXISTS time_dimension (  
    id SERIAL PRIMARY KEY, 
    year INT NOT NULL
);
""" 
cursor.execute(sql)
conn.commit()

#create Geography Dimension if it doesn't exist
sql = """ 
CREATE TABLE IF NOT EXISTS geography_dimension (  
    geography_key SERIAL PRIMARY KEY, 
    country TEXT,
    state TEXT
);
""" 
cursor.execute(sql)
conn.commit()

#create demopgrahic dimension if it doesn't exist
sql = """ 
CREATE TABLE IF NOT EXISTS demopgrahic_dimension (  
    demographic_key SERIAL PRIMARY KEY, 
    sex TEXT,
    age_range TEXT
);
""" 
cursor.execute(sql)
conn.commit()

#create death dimension if it doesn't exist
sql = """ 
CREATE TABLE IF NOT EXISTS death_dimension (  
    death_key SERIAL PRIMARY KEY, 
    death_desription TEXT,
    mortality_id TEXT
);
""" 

#create cause table if it doesn't exist
#table to hold ids ofr ICD-10 causes of death
sql = """ 
CREATE TABLE IF NOT EXISTS cause_table (  
    code_key SERIAL PRIMARY KEY, 
    description TEXT
);
""" 






