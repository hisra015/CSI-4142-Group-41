#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import pandas as pd
import sklearn as sk
from sklearn.preprocessing import MinMaxScaler

#retrieve data from csv
data = pd.read_csv("Staged_data.csv", low_memory=False)



# function tonormalize numerical data
def normalize_data():
    normlizer = MinMaxScaler()
    columns = ['year','age_mortality', 'death_number', 'death_percentage', 'death_rank']
    data[columns] = normlizer.fit_transform(data[columns])
    print(data[:10])    


def main():
   normalize_data()

    
if __name__ == "__main__":
    main()
