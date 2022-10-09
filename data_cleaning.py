# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 22:24:07 2022

@author: jdaul
"""

import pandas as pd
import numpy as np
from datetime import date

path_df = "C:/Users/jdaul/Documents/Machine Learning Deep Learning/Machine Learning projects/ds_salary_proj-master/glassdoor_jobs.csv"

df = pd.read_csv(path_df)


#infos from job description (impact of python required for instance)





columns = df.columns


#Remove because need labeled examples
df = df[df['Salary Estimate'] != '-1']

values_salary = df['Salary Estimate'].value_counts()


#Salary column parsing
df['Hourly'] = df['Salary Estimate'].apply(lambda x : 1 if 'per hour' in x.lower() else 0)
df['Glassdoor estimates'] = df['Salary Estimate'].apply(lambda x : 1 if 'glassdoor est.' in x.lower() else 0)
df['Employer estimates'] = df['Salary Estimate'].apply(lambda x : 1 if 'employer est.' in x.lower() else 0)
df['Employer provided'] = df['Salary Estimate'].apply(lambda x : 1 if 'employer provided salary' in x.lower() else 0)

df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.replace('(Glassdoor est.)',''))
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.replace('(Employer est.)',''))
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.replace('Employer Provided Salary:',''))
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.replace('Per Hour',''))
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.replace('$','').replace('K',''))

df[['Min Salary Estimate','Max Salary Estimate']] = df['Salary Estimate'].str.split('-', 1, expand = True).astype(float)
df['Average Salary Estimate'] = (df['Min Salary Estimate'] + df['Max Salary Estimate']) / 2 #will check later if this is important or not

#Company name parsing : split number and name
df['Company Name'] = df['Company Name'].str.split('\n').str[0]

#location and headquarters parsing : split state and city
df[['Location City','Location State']] = df['Location'].str.rsplit(',', 1, expand = True)
df[['Headquarters City','Headquarters State']] = df['Headquarters'].str.rsplit(',', 1, expand = True) #rsplit = right to left
df['Same state'] = np.where(df['Location State'] == df['Headquarters State'], 1, 0)
df['Same city'] = np.where(df['Location City'] == df['Headquarters City'], 1, 0)

#One hot encoding size
df['Size'] = df['Size'].replace('-1', 'Unknown')

dict_size = {'Unknown' : 0, 
             '1 to 50 employees ' : 1,
             '51 to 200 employees' : 2,
             '201 to 500 employees' : 3,
             '501 to 1000 employees' : 4,
             '1001 to 5000 employees' : 5,
             '5001 to 10000 employees' : 6,
             '10000+ employees' : 7}

df['Size Ordinal Encoding'] = df['Size'].map(dict_size)

#Type of ownership
df['Type of ownership'] = df['Type of ownership'].replace('-1', 'Unknown')
print(df['Industry'].value_counts())

#Age of the company instead of founded field (better logic ?)
df['Age Company'] = df['Founded'].apply(lambda x : date.today().year - x if x != -1 else -1)

#Job description
print(df['Job Description'][0])

#aws
df['AWS'] = df['Job Description'].apply(lambda x : 1 if "aws" in x.lower() else 0)

print(df['Job Description'].apply(lambda x : 1 if "aws" in x.lower() else 0).value_counts())
#python
df['Python'] = df['Job Description'].apply(lambda x : 1 if "python" in x.lower() else 0)

#master
df['Master degree'] = df['Job Description'].apply(lambda x : 1 if "master's degree" in x.lower() else 0)
print(df['Job Description'].apply(lambda x : 1 if "master's degree" in x.lower() else 0).value_counts())

#bachelor
df['Bachelor degree'] = df['Job Description'].apply(lambda x : 1 if "bachelor's degree" in x.lower() else 0)
print(df['Job Description'].apply(lambda x : 1 if "bachelor's degree" in x.lower() else 0).value_counts())

#phd
df['PHD'] = df['Job Description'].apply(lambda x : 1 if "phd" in x.lower() else 0)
print(df['Job Description'].apply(lambda x : 1 if "phd" in x.lower() else 0).value_counts())


columns = ['Job Title', 'Rating', 'Company Name', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'Competitors',
'Hourly', 'Glassdoor estimates', 'Employer estimates',
'Employer provided', 'Min Salary Estimate', 'Max Salary Estimate',
'Average Salary Estimate', 'Location City', 'Location State',
'Headquarters City', 'Headquarters State', 'Same state', 'Same city',
'Size Ordinal Encoding', 'Age Company', 'AWS', 'Python',
'Master degree', 'Bachelor degree', 'PHD']

df_out = df[columns]

df_out.to_csv('salary_data_cleaned.csv', index = False, sep=';')









