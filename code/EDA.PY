import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Image route
image_route = '../images/'
data_route = '../data/input/'
data_output_route = '../data/output/'

# Load the data
df = pd.read_excel(f'{data_route}Salesforce Opportunities export.xlsx', sheet_name='Opportunities Export 2025')

# Basic data exploration
print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())

# Data cleaning and preparation
# Convert date columns to datetime
date_cols = ['opportunity_created_date', 'close_date', 'loi_start_date_c', 
             'selected_property_start_date_c', 'renovation_started_date_c', 
             'listing_start_date_c', 'property_created_at', 'status_updated_at',
             'lead_created_date']

for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

# Basic statistics
print("\nBasic statistics for numeric columns:")
print(df.describe())

# Missing values analysis
print("\nMissing values per column:")
print(df.isnull().sum().sort_values(ascending=False))

# Opportunity stage analysis
print("\nOpportunity stage distribution:")
print(df['latest_stage'].value_counts(normalize=True) * 100)

# Opportunity type analysis
print("\nOpportunity type distribution:")
print(df['type'].value_counts(normalize=True) * 100)

# First property vs expansion analysis
print("\nFirst property vs expansion distribution:")
print(df['first_prop_or_expansion'].value_counts(normalize=True) * 100)

# Metro area analysis
print("\nTop 10 metro areas by opportunity count:")
print(df['metro_area'].value_counts().head(10))

# Owner team analysis
print("\nOwner team distribution:")
print(df['owner_team'].value_counts(normalize=True) * 100)

# Visualization 1: Opportunity stage distribution
plt.figure(figsize=(10, 6))
df['latest_stage'].value_counts().plot(kind='bar')
plt.title('Opportunity Stage Distribution')
plt.xlabel('Stage')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{image_route}opportunity_stage_distribution.png')
plt.close()

# Visualization 2: Opportunity type distribution
plt.figure(figsize=(10, 6))
df['type'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Opportunity Type Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig(f'{image_route}opportunity_type_distribution.png')
plt.close()

# Visualization 3: Metro area distribution
plt.figure(figsize=(12, 6))
df['metro_area'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Metro Areas by Opportunity Count')
plt.xlabel('Metro Area')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{image_route}metro_area_distribution.png')
plt.close()

# Visualization 4: First property vs expansion
plt.figure(figsize=(8, 6))
df['first_prop_or_expansion'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('First Property vs Expansion')
plt.ylabel('')
plt.tight_layout()
plt.savefig(f'{image_route}first_prop_vs_expansion.png')
plt.close()

# Time-based analysis
if 'opportunity_created_date' in df.columns:
    df['created_month'] = df['opportunity_created_date'].dt.to_period('M')
    monthly_trend = df.groupby('created_month').size()[:-1]
    
    plt.figure(figsize=(12, 6))
    monthly_trend.plot(kind='line', marker='o')
    plt.title('Monthly Opportunity Creation Trend')
    plt.xlabel('Month')
    plt.ylabel('Number of Opportunities')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{image_route}monthly_opportunity_trend.png')
    plt.close()

# Conversion rates analysis
total_opportunities = len(df)
closed_won = len(df[df['latest_stage'] == 'Closed Won'])
conversion_rate = (closed_won / total_opportunities) * 100
print(f"\nOverall conversion rate: {conversion_rate:.2f}%")

# Days in pipeline analysis
if 'total_sum_days' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_sum_days'].dropna(), bins=30)
    plt.title('Distribution of Total Days in Pipeline')
    plt.xlabel('Total Days in Pipeline')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(f'{image_route}days_in_pipeline_distribution.png')
    plt.close()

# df['rooms'].value_counts()

# Rooms analysis
if 'rooms' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rooms'].dropna(), bins=3)
    plt.title('Distribution of Number of Rooms per Property')
    plt.xlabel('Number of Rooms')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(f'{image_route}rooms_distribution.png')
    plt.close()

# Market type analysis
if 'market_type' in df.columns:
    plt.figure(figsize=(10, 6))
    df['market_type'].value_counts().plot(kind='bar')
    plt.title('Market Type Distribution')
    plt.xlabel('Market Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{image_route}market_type_distribution.png')
    plt.close()

# Property type analysis
if 'property_type' in df.columns:
    plt.figure(figsize=(10, 6))
    df['property_type'].value_counts().plot(kind='bar')
    plt.title('Property Type Distribution')
    plt.xlabel('Property Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{image_route}property_type_distribution.png')
    plt.close()

# Save summary statistics to a file
with open(f'{data_output_route}data_summary.txt', 'w') as f:
    f.write("Salesforce Opportunities Data Analysis Summary\n")
    f.write("="*50 + "\n\n")
    
    f.write(f"Total opportunities: {len(df)}\n")
    f.write(f"Columns: {len(df.columns)}\n\n")
    
    f.write("Missing values per column:\n")
    f.write(df.isnull().sum().sort_values(ascending=False).to_string())
    f.write("\n\n")
    
    f.write("Opportunity stage distribution:\n")
    f.write(df['latest_stage'].value_counts(normalize=True).to_string())
    f.write("\n\n")
    
    f.write("Opportunity type distribution:\n")
    f.write(df['type'].value_counts(normalize=True).to_string())
    f.write("\n\n")
    
    f.write(f"Overall conversion rate: {conversion_rate:.2f}%\n")
    
    if 'total_sum_days' in df.columns:
        f.write("\nDays in pipeline statistics:\n")
        f.write(df['total_sum_days'].describe().to_string())

print("\nAnalysis complete. Visualizations and summary saved to files.")