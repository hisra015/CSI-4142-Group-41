#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import psycopg2
import pandas as pd
import numpy as np

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
    mortality_code TEXT
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

#rename columns in canada dataset
canada_data = canada_data.rename({'REF_DATE':'Year'}, axis='columns') 
canada_data = canada_data.rename({'GEO':'Country'}, axis='columns')
canada_data = canada_data.rename({'Age at time of death':'Age'}, axis='columns')  

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

#drop all uneccessary columns
canada_data = canada_data.drop(columns='DGUID')
canada_data = canada_data.drop(columns='UOM_ID')
canada_data = canada_data.drop(columns='SCALAR_FACTOR')
canada_data = canada_data.drop(columns='SCALAR_ID')
canada_data = canada_data.drop(columns='VECTOR')
canada_data = canada_data.drop(columns='COORDINATE')
canada_data = canada_data.drop(columns='STATUS')
canada_data = canada_data.drop(columns='SYMBOL')
canada_data = canada_data.drop(columns='TERMINATED')
canada_data = canada_data.drop(columns='DECIMALS')

#stuff = canada_data['Leading causes of death (ICD-10)'].str.split('[').astype('string')
#print(stuff[:10])

#split descriptions and codes, transform data
canada_data['Leading causes of death (ICD-10)'] = canada_data['Leading causes of death (ICD-10)'].replace('Other causes of death', 'Other causes of death [Other]')
canada_data[['Description', 'Code']] = canada_data['Leading causes of death (ICD-10)'].str.extract(r'(.*) (\[.*\])', expand=True)
canada_data['Country'] = 'Canada'
canada_data['State'] = 'NA'

columns = ['Year'] + ['Country'] + ['State'] + ['Age'] + ['Sex'] + ['Description'] + ['Code'] + ['Characteristics'] + ['VALUE']
canada_data = canada_data[columns]

#Turn death statistics into columns instead of havingh their own rows
death_counts = canada_data.copy()
death_counts = pd.pivot_table(death_counts, index=['Year', 'Age', 'Sex', 'Code'], columns='Characteristics', values = ['VALUE'], aggfunc='first', sort=False)
#print(death_counts[:10])

death_counts.reset_index(drop=False, inplace=True)
death_counts.reindex(['Year', 'Age', 'Sex', 'Code', 'Age-specific mortality rate per 100,000 population', 'Number of deaths', 'Percentage of deaths', 'Rank of leading causes of death'], axis=1)
death_counts.columns = death_counts.columns.droplevel(0)
death_counts.reset_index(drop=True)

#prepare canada data for new columns
canada_data = canada_data.drop(columns='Characteristics')
canada_data = canada_data.drop(columns='VALUE')
canada_data = canada_data.drop_duplicates()
canada_data.reset_index(drop=False, inplace=True)
canada_data = canada_data.drop(columns='index')

#Re-add the death statistics
canada_data['Age-specific mortality rate per 100,000 population'] = death_counts['Age-specific mortality rate per 100,000 population']
canada_data['Number of deaths'] = death_counts['Number of deaths']
canada_data['Percentage of deaths'] = death_counts['Percentage of deaths']
canada_data['Rank of leading causes of death'] = death_counts['Rank of leading causes of death']
#print(canada_data[:10])

#----------------------------------------

US_data['Country'] = 'United States'
US_data['Sex'] = 'Both sexes'
US_data['Age'] = 'Age at time of death, all ages'
US_data['State'] = US_data['State'].replace('United States', 'NA')

#drop all uneccessary columns 
US_data = US_data.drop(columns='Cause Name')

#rename columns
US_data = US_data.rename({'113 Cause Name':'Leading causes of death (ICD-10)'}, axis='columns') 
US_data = US_data.rename({'Age-adjusted Death Rate':'Age-specific mortality rate per 100,000 population'}, axis='columns') 
US_data = US_data.rename({'Deaths':'Number of deaths'}, axis='columns') 

#change names to make data consistent
US_data.replace('All Causes', 'Total, all causes of death (A00-Y89)', inplace=True)
#split descriptions and codes
pattern = r'([^\(]*)\s*(\([^\)]+\))'
US_data[['Description', 'Code']] = US_data['Leading causes of death (ICD-10)'].str.extract(pattern, expand=True)

#Calculate percentage of deaths and ranks of deaths to keep it consistent with Canadian data
US_data['Percentage of deaths'] = US_data.groupby('State')['Number of deaths'].transform(lambda x: (x / x.sum() * 100).round(1))
# Rank the causes of death within each state based on the number of deaths
US_data['Rank of leading causes of death'] = US_data.groupby('State')['Number of deaths'].rank(ascending=False, method='min')

#fix edge case data
US_data.replace('Accidents', 'Accidents (unintentional injuries)', inplace=True)
US_data.replace('Intentional self-harm ', 'Intentional self-harm (suicide)', inplace=True)
US_data.replace('(unintentional injuries)', '(V01-X59, Y85-Y86)', inplace=True)
US_data.replace('(suicide)', '(X60-X84, Y87.0)', inplace=True)

#reformat data
US_data['Code'] = US_data['Code'].str.replace('(','[', regex=False)
US_data['Code'] = US_data['Code'].str.replace(')',']', regex=False)

#reorder columns
columns = ['Year'] + ['Country'] + ['State'] + ['Age'] + ['Sex'] + ['Description'] + ['Code'] + ['Age-specific mortality rate per 100,000 population'] + ['Number of deaths'] + ['Percentage of deaths'] + ['Rank of leading causes of death']
US_data = US_data[columns] 

#combine both data frames to stage data
staged_data = pd.concat([canada_data, US_data])

#assign surrogate keys to data
staged_data['Surrogate Key'] = range(1, len(staged_data) + 1)

#reorder columns
columns = ['Surrogate Key'] + ['Year'] + ['Country'] + ['State'] + ['Age'] + ['Sex'] + ['Description'] + ['Code'] + ['Age-specific mortality rate per 100,000 population'] + ['Number of deaths'] + ['Percentage of deaths'] + ['Rank of leading causes of death']
staged_data = staged_data[columns]
#print(staged_data[:10])


#rename columns to match database
staged_data = staged_data.rename({'Surrogate Key':'surrogate'}, axis='columns') 
staged_data = staged_data.rename({'Year':'year'}, axis='columns') 
staged_data = staged_data.rename({'Country':'country'}, axis='columns') 
staged_data = staged_data.rename({'State':'state'}, axis='columns')
staged_data = staged_data.rename({'Age':'age_range'}, axis='columns')
staged_data = staged_data.rename({'Sex':'sex'}, axis='columns')
staged_data = staged_data.rename({'Description':'death_description'}, axis='columns')
staged_data = staged_data.rename({'Code':'mortality_code'}, axis='columns')
staged_data = staged_data.rename({'Age-specific mortality rate per 100,000 population':'age_mortality'}, axis='columns')
staged_data = staged_data.rename({'Number of deaths':'death_number'}, axis='columns')
staged_data = staged_data.rename({'Percentage of deaths':'death_percentage'}, axis='columns')
staged_data = staged_data.rename({'Rank of leading causes of death':'death_rank'}, axis='columns')

#fill empty columns, missing values
staged_data[['age_mortality', 'death_number', 'death_percentage', 'death_rank']] = staged_data[['age_mortality', 'death_number', 'death_percentage', 'death_rank']].fillna(-1)
staged_data.replace('', np.nan, inplace=True)
staged_data.fillna('N/A', inplace=True)
print(staged_data[:10])
staged_data.to_csv('Staged_data.csv', index=False)