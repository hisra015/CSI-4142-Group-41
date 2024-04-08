#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database remotely
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')


#get table names and data from the database
#returns a tuple with the table names and data in the form of dataframes
def get_tables():
    cursor = conn.cursor()

    # Fetch the list of tables in the database
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()

    # A dictionary to store DataFrames, with table names as keys
    data = {}

    # Iterate over each table and load its data into a DataFrame
    for table in tables:
        table_name = table[0]
        data[table_name] = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    # Close the cursor and connection
    cursor.close()
    print(tables[0])
    return table_name, data

#preprocesses the data if not already
def preprocess_data(tables, data):
    return data


def main():
    tables, data = get_tables()
    
if __name__ == "__main__":
    main()
