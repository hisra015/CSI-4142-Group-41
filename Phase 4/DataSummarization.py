import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your dataset
data = pd.read_csv('Staged_data.csv')
path = "Phase 4/Graphs/"
# Adjusting histogram bins and figure size for better visibility and saving them
# Surrogate Distribution
plt.figure(figsize=(8, 6))
sns.histplot(data['surrogate'], bins=20)
plt.title('Surrogate Distribution')
plt.savefig(path+'surrogate_distribution.png')  # Save the figure
plt.close()  # Close the plot to avoid displaying it in the notebook

# Year Distribution
plt.figure(figsize=(8, 6))
sns.histplot(data['year'], bins=10)
plt.title('Year Distribution')
plt.savefig(path+'year_distribution.png')
plt.close()

# Age Mortality Distribution with increased bins
plt.figure(figsize=(10, 8))
sns.histplot(data['age_mortality'], bins=40, kde=True)
plt.title('Age Mortality Distribution')
plt.savefig(path+'age_mortality_distribution.png')
plt.close()

# Death Number Distribution
plt.figure(figsize=(10, 8))
sns.histplot(data['death_number'], bins=40, kde=True)
plt.title('Death Number Distribution')
plt.savefig(path+'death_number_distribution.png')
plt.close()

# Death Percentage Distribution
plt.figure(figsize=(10, 8))
sns.histplot(data['death_percentage'], bins=40, kde=True)
plt.title('Death Percentage Distribution')
plt.savefig(path+'death_percentage_distribution.png')
plt.close()

# Death Rank Distribution
plt.figure(figsize=(10, 8))
sns.histplot(data['death_rank'], bins=40, kde=True)
plt.title('Death Rank Distribution')
plt.savefig(path+'death_rank_distribution.png')
plt.close()

# Age Mortality Boxplot
plt.figure(figsize=(8, 6))
sns.boxplot(data=data, x='age_mortality')
plt.title('Age Mortality Boxplot')
plt.savefig(path+'age_mortality_boxplot.png')
plt.close()

# Log-transformed Death Number Distribution
data['log_death_number'] = np.log1p(data['death_number'])
plt.figure(figsize=(10, 8))
sns.histplot(data['log_death_number'], bins=40, kde=True)
plt.title('Log-transformed Death Number Distribution')
plt.savefig(path+'log_death_number_distribution.png')
plt.close()
