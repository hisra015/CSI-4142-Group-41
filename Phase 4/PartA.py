#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import pandas as pd
import sklearn as sk
from sklearn.preprocessing import MinMaxScaler

#retrieve data from csv
data = pd.read_csv("Staged_data.csv", low_memory=False)
num_columns = ['year','age_mortality', 'death_number', 'death_percentage', 'death_rank']
cat_columns = ['country','state', 'age_range', 'death_description', 'mortality_code']


# function tonormalize numerical data
def normalize_data():
    normlizer = MinMaxScaler()
    columns = ['year','age_mortality', 'death_number', 'death_percentage', 'death_rank']
    data[columns] = normlizer.fit_transform(data[columns])
    print(data[:10])    

#function to one hot encode categorical data
def encode_data():
    return

def feature_selection():
    
    mat = data[num_columns].corr()
    print(mat)
    return


def main():
   feature_selection()
   #normalize_data()

    
if __name__ == "__main__":
    main()
