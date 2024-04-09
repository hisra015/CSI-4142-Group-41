#Group 41
#Michael Quach: 300177284
#Aleana Wright: 300196531
#Hamza Israr: 300168510

import pandas as pd
import sklearn as sk
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

#retrieve data from csv
data = pd.read_csv("Staged_data.csv", low_memory=False)
data = data.drop(columns='surrogate') #drop surrogate keys as they are uncessary
num_columns = ['year','age_mortality', 'death_number', 'death_percentage', 'death_rank']
cat_columns = ['country','state', 'age_range', 'death_description', 'mortality_code']


# function to Deals with missing values
def transform_data():
    data['year'] = data['year'].fillna(data['year'].median())
    data['country'] = data['country'].fillna('NA')
    data['state'] = data['state'].fillna('NA')
    data['age_range'] = data['age_range'].fillna('Age at time of death, all ages')    
    data['sex'] = data['sex'].fillna('Both sexes')
    data['death_description'] =  data['death_description'].fillna('Other causes of death') 
    data['death_description'] =  data['death_description'].fillna('Other causes of death') 
    data['mortality_code'] =  data['mortality_code'].fillna('[Other]') 
    data['death_number'] = data['death_number'].fillna(data['death_number'].median())
    data['age_mortality'] = data['age_mortality'].fillna(data['age_mortality'].median())
    data['death_percentage'] = data['death_percentage'].fillna(data['death_percentage'].median())
    data['death_rank'] = data['death_rank'].fillna(data['death_rank'].median())


# function tonormalize numerical data
def normalize_data():
    normlizer = MinMaxScaler()
    data[num_columns] = normlizer.fit_transform(data[num_columns])
    print(data[:10])    

#function to one hot encode categorical data
def encode_data():
    encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_data = encoder.fit_transform(data[cat_columns])
    return encoded_data

def feature_selection():
    mat = data[num_columns].corr()
    print(mat)
    return

def main():
   feature_selection()
   normalize_data()
   encoded_data = encode_data()
   print(encoded_data[:10])

    
if __name__ == "__main__":
    main()
