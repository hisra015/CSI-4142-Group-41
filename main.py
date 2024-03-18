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
CREATE TABLE IF NOT EXISTS year_dimension (  
    surrogate_pk SERIAL PRIMARY KEY, 
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
CREATE TABLE IF NOT EXISTS demographic_dimension (  
    demographic_key SERIAL PRIMARY KEY, 
    sex TEXT,
    age_range TEXT
);
""" 
cursor.execute(sql)
conn.commit()

#create death dimension if it doesn't exist
sql = """ 
CREATE TABLE IF NOT EXISTS cause_of_death_dimension (  
    death_key SERIAL PRIMARY KEY, 
    death_description TEXT,
    mortality_id TEXT
);
""" 
cursor.execute(sql)
conn.commit()

#create cause table if it doesn't exist
#table to hold ids ofr ICD-10 causes of death
sql = """ 
CREATE TABLE IF NOT EXISTS code_table (  
    code_key SERIAL PRIMARY KEY, 
    description TEXT
);
""" 
cursor.execute(sql)
conn.commit()

#create fact table if it doesn't exist
#table to hold ids ofr ICD-10 causes of death
sql = """ 
CREATE TABLE IF NOT EXISTS fact_table (  
    surrogate INT PRIMARY KEY,
    demographic_key INT,
    geographic_key INT,
    year_key INT,
    cause_key INT,
    death_number INT,
    death_percentage DECIMAL,
    death_rank INT,
    age_mortality TEXT,
    FOREIGN KEY (demographic_key) REFERENCES demographic_dimension (demographic_key),
    FOREIGN KEY (geographic_key) REFERENCES geography_dimension (geography_key),
    FOREIGN KEY (year_key) REFERENCES year_dimension (surrogate_pk),
    FOREIGN KEY (cause_key) REFERENCES cause_of_death_dimension (death_key)
);
"""
cursor.execute(sql)
conn.commit() 

#load each csv file into a dataframe
canada_data = pd.read_csv("Canada Data.csv", low_memory=False)
US_data = pd.read_csv("US Data.csv")
cause_data = pd.read_csv("cause ids.csv")

canada_data = canada_data.rename({'REF_DATE':'Year'}, axis='columns') 
canada_data = canada_data.rename({'GEO':'Country'}, axis='columns') 

#--------------------Transform Canadian dataset--------------------

#Columns to remove in Canada Data.csv

dguid = 'DGUID'
uomid = 'UOM_ID'
scalar_f = 'SCALAR_FACTOR'
scalar_ID = 'SCALAR_ID'
vector = 'VECTOR'
coord = 'COORDINATE'
status = 'STATUS'
symbol = 'SYMBOL'
terminate = 'TERMINATED'
dec = 'DECIMALS'

#drop all uncessory columns
if dguid in canada_data.columns:
    canada_data = canada_data.drop(columns=dguid)
if uomid in canada_data.columns:
    canada_data = canada_data.drop(columns=uomid)
if scalar_f in canada_data.columns:
    canada_data = canada_data.drop(columns=scalar_f)
if scalar_ID in canada_data.columns:
    canada_data = canada_data.drop(columns=scalar_ID)
if vector in canada_data.columns:
    canada_data = canada_data.drop(columns=vector)
if coord in canada_data.columns:
    canada_data = canada_data.drop(columns=coord)
if status in canada_data.columns:
    canada_data = canada_data.drop(columns=status)
if symbol in canada_data.columns:
    canada_data = canada_data.drop(columns=symbol)
if terminate in canada_data.columns:
    canada_data = canada_data.drop(columns=terminate)
if dec in canada_data.columns:
    canada_data = canada_data.drop(columns=dec)


#stuff = canada_data['Leading causes of death (ICD-10)'].str.split('[').astype('string')
#print(stuff[:10])

#split descriptions and codes
canada_data[['Description', 'Code']] = canada_data['Leading causes of death (ICD-10)'].str.extract(r'(.*) (\[.*\])', expand=True)
canada_data['Country'] = 'Canada'

surrogates, unique = pd.factorize(canada_data['Leading causes of death (ICD-10)'])

canada_data['State'] = 'N/A'
canada_data['Surrogate Keys'] = surrogates
columns = ['Surrogate Keys'] + ['State'] + [col for col in canada_data.columns if col != 'Surrogate Keys']
canada_data = canada_data[columns]

print(canada_data[:10])

#----------------------------------------

US_data['Country'] = 'United States'
US_data['Sex'] = 'Both sexes'
US_data['Age at time of death'] = 'Age at time of death, all ages'




