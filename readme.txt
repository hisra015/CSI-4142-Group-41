Group 41
	
Michael Quach: 300177284
Aleana Wright: 300196531
Hamza Israr: 300168510


Functions of main.py
- Creates the tables in the database
- Extracts data from Canada Data and US Data into pandas dataframe.
- Cleans Canada and US Data.
- Transforms Canada and US Data into compatible format.
- Saves all data into a singled csv named Staged_data.csv.

Functions of load.py
- Prepares data for load into the database.
- Loads data from Staged_data.csv into the database.

Run instructions:
- Install latest version of python.
- Install psycopg2 and sqlalchemy:
	- In the command line:
		'pip install pandas' if you haven't already.
		'pip install psycopg2'
		'pip install sqlalchemy'

The database is a postgres database hosted remotely on Railway. To view please use the invite link:
https://railway.app/invite/sb56zXbcSYw

If there are any issues, please contact me at mquac089@uottawa.ca 

