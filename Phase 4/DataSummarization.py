import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your dataset
data = pd.read_csv('Staged_data.csv')
path = "Phase 4/Graphs/"
# Adjusting histogram bins and figure size for better visibility and saving them

# Trend of total deaths over the years
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='year', y='death_number', estimator='sum', ci=None, marker='o')
plt.xticks(data['year'].unique(), rotation=45)  # Ensure all years are shown and rotate labels for better visibility
plt.title('Total Deaths Over Years')
plt.ylabel('Total Deaths')
plt.xlabel('Year')
plt.tight_layout()  # Adjust the layout to make room for the x-axis labels
plt.savefig(path+'total_deaths_over_years.png')
plt.close()

# Top causes of death
# First, let's group the data by 'death_description' and sum the 'death_number'
cause_death_counts = data.groupby('death_description')['death_number'].sum().reset_index()
top_causes = cause_death_counts.sort_values(by='death_number', ascending=False).head(10)

plt.figure(figsize=(12, 8))
sns.barplot(data=top_causes, x='death_number', y='death_description', palette='viridis')
plt.title('Top Causes of Death')
plt.xlabel('Number of Deaths')
plt.ylabel('Cause of Death')
plt.tight_layout()
plt.savefig(path+'top_causes_of_death.png')
plt.close()


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

# Log-transformed Death Number Distribution
data['log_death_number'] = np.log1p(data['death_number'])
plt.figure(figsize=(10, 8))
sns.histplot(data['log_death_number'], bins=40, kde=True)
plt.title('Log-transformed Death Number Distribution')
plt.savefig(path+'log_death_number_distribution.png')
plt.close()
