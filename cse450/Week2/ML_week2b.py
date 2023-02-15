

# IMPORTS
#%% Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics            import accuracy_score
from sklearn.model_selection    import train_test_split
from imblearn.over_sampling     import RandomOverSampler
from sklearn.ensemble           import RandomForestClassifier

# df = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/bank_holdout_test.csv")

df = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/bank_holdout_test_mini.csv")

#%% Clean Data Set

### JOB
df['job'] = df['job'].replace(
    ['housemaid',   'services', 
    'admin.',       'blue-collar', 
    'technician',   'retired', 
    'unemployed',   'self-employed', 
    'unknown',      'management',
    'entrepreneur', 'student'],
    [26410,         30045,
    78109,          52987,
    44390,          47620,
    46819,          84305,
    np.nan,         56987,
    48113,          3838])

df['job'] = df['job'].fillna(df['job'].mean())

### MARITAL
df['marital'] = df['marital'].replace(
    ['married', 'single', 'divorced', 'unknown'],
    [1,0,-1,0])

### EDUCATION 
df['education'] = df['education'].replace(
    ['basic.4y',            'high.school', 
    'basic.6y',             'basic.9y',
    'professional.course',  'unknown', 
    'university.degree',    'illiterate'],
    [16,                    12, 
     18,                    21,
     14,                    np.nan,
     17,                    5])

df['education'] = df['education'].fillna(df['education'].mean())

### DEFAULT
df['default'] = df['default'].replace(['no','unknown','yes'],[0,.5,1])

### HOUSING
df['housing'] = df['housing'].replace(['no','unknown','yes'],[0,.5,1])

### LOAN
df['loan'] = df['loan'].replace(['no','unknown','yes'],[0,.5,1])

### CONTACT
df['contact'] = df['contact'].replace(['telephone', 'cellular'],[0,1])

### PDAYS
df['pdays'] = df['pdays'].replace([999],[30])

### POUTCOME
df['poutcome'] = df['poutcome'].replace(['nonexistent', 'failure', 'success'],[0,-1,1])

dat = pd.get_dummies(df)

#%% Select Best Features
best_features_list = ['age',
 'euribor3m',
 'campaign',
 'job',
 'education',
 'nr.employed',
 'emp.var.rate',
 'marital',
 'housing',
 'cons.conf.idx',
 'loan',
 'pdays',
 'poutcome',
 'default',
 'cons.price.idx',
 'contact']

dat = dat.filter(items = best_features_list)


#%% Load and run model
filename = 'bank_model.sav'

clf = pickle.load(open(filename, 'rb'))

Y_pred = clf.predict(dat)

pred_df = pd.DataFrame(Y_pred, columns = ['predictions'])

pred_df.to_csv("predictions.csv", index=False)