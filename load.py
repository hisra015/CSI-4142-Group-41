#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import pandas as pd
from sqlalchemy import create_engine

#Note: DO NOT RUN THIS A SECOND TIME OR THE RECORDS WILL BE REPEATED -Michael


#connect to database remotely
conn = create_engine('postgresql://postgres:EYndBSqLdilpjZfzdWFAOiNTdRrozMko@viaduct.proxy.rlwy.net:41102/railway')

#check the database connection
try:
    with conn.connect() as connection:
        print("Connection successful.")
except:
    print("Error connecting to the database.")

staged_data = pd.read_csv("Staged_data.csv")
print()

#get dataframe columns for each dimension
cause_table = staged_data[['death_description', 'mortality_code']]
demographic_table = staged_data[['sex', 'age_range']]
geography_table = staged_data[['country', 'state']]
year_table = staged_data['year']

#insert dataframes into dimension tables
cause_table.to_sql('cause_of_death_dimension', con=conn, if_exists='append', index=False)
demographic_table.to_sql('demographic_dimension', con=conn, if_exists='append', index=False)
geography_table.to_sql('geography_dimension', con=conn, if_exists='append', index=False)
year_table.to_sql('year_dimension', con=conn, if_exists='append', index=False)

#get fact table columns
fact_table= staged_data[['surrogate', 'death_number', 'death_percentage', 'death_rank', 'age_mortality']]
fact_table['demographic_key'] = staged_data['surrogate']
fact_table['geographic_key'] = staged_data['surrogate']
fact_table['year_key'] = staged_data['surrogate']
fact_table['cause_key'] = staged_data['surrogate']

#insert dataframe into fact table
fact_table.to_sql('fact_table', con=conn, if_exists='append', index=False)