#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import psycopg2
import pandas as pd

#connect to database remotely
conn = psycopg2.connect(dbname='railway', user='postgres', password='EYndBSqLdilpjZfzdWFAOiNTdRrozMko', host='viaduct.proxy.rlwy.net', port='41102', sslmode='require')

cursor = conn.cursor()