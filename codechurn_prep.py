import pandas as pd
import numpy as np

'''
    Create Excel file with multiple sheets from code chrun metrics.
    - Reads data from data/codechurn.csv
    - CSV file contains churns per year
'''

def project(row):
    if row[4] == 'Subsystems':
        val = 'subsystems'
    elif row[2] == 'Common':
        val = 'common'
    elif row[4] == 'Core':
        val = 'core'
    return val

def group(row):
    if row[4] == 'Subsystems':
        val = row[4]
    elif row[2] == 'Common':
        val = row[4]
    elif row[4] == 'Core':
        if row[5] == 'Opcua':
            val = row[5].upper()
        else:
            val = row[5]
    return val

def folder(row):
    if row[4] == 'Subsystems':
        val = row[5]
    elif row[2] == 'Common':
        val = row[5]
    elif row[4] == 'Core':
        val = row[6]
    return val

def target_env(row):
    cfileExtensions = ('.cpp', '.h', '.c')
    if row['file'].endswith(cfileExtensions):
        return 'C++'
    return 'C#'

def test_project(row):
    return "yes" if ".Test" in row['file'] else "no"

def unique_filename(row):
    val = row['file'].replace("$/ASW/AutomationStudio/Trunk/", "");

    prefix, match, suffix = val.partition("/")
    return suffix.replace("/", "\\")


df = pd.read_csv('C:/Users/rolandgerm/projects/BuR/python/data/codechurn.csv', sep=',')

new = df.join(df["file"].str.split('/', n=10, expand=True))

# filter only important rows
new = new[(new[2] == "Common") | (new[2] == "AutomationStudio")] 
new = new[new[3] != "Versions"] 
new = new[new[4] != "WorkingVersions"]

# create columns applying the grouping functions
new['Project'] = new.apply(project, axis=1)
new['Group'] = new.apply(group, axis=1)
new['Folder'] = new.apply(folder, axis=1)
new['File Name'] = new.apply(unique_filename, axis=1)
new['Test'] = new.apply(test_project, axis=1)
new['Target'] = new.apply(target_env, axis=1)

# remove bad data and cleanup temporary columns
new = new.drop(new[new['Group'] == 'exp'].index)
new = new.drop(0, axis=1)
new = new.drop(1, axis=1)
new = new.drop(2, axis=1)
new = new.drop(3, axis=1)
new = new.drop(4, axis=1)
new = new.drop(5, axis=1)
new = new.drop(6, axis=1)
new = new.drop(7, axis=1)
new = new.drop(8, axis=1)
new = new.drop(9, axis=1)
new = new.drop(10, axis=1)

# create new dataframe with sum of churns
g = new.groupby(['File Name'])['count'].sum().reset_index()
g = g.rename(columns={"count": "churn"})
g = g.set_index('File Name').join(new.set_index('File Name')).reset_index()
g = g.drop('year', axis=1).drop('count', axis=1).drop_duplicates(subset='File Name')

# add pivots
table = pd.pivot_table(g, values='churn', index=['Project', 'Group', 'Folder'], aggfunc=np.sum).reset_index()
table2 = pd.pivot_table(new, values='count', index=['year', 'Project', 'Group'], aggfunc=np.sum).reset_index()

with pd.ExcelWriter('Code Churn Metrics.xlsx') as writer:  
    new.to_excel(writer, sheet_name='Churn per year')
    g.to_excel(writer, sheet_name='Churn sum')
    table.to_excel(writer, sheet_name='All changes per folder')
    table2.to_excel(writer, sheet_name='Yearly changes per group')