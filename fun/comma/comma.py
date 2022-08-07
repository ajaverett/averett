# IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# READ IN DATA
raw_comma = pd.read_csv(
    'https://raw.githubusercontent.com/fivethirtyeight/data/master/comma-survey/comma-survey.csv',
    skiprows=1, 
    header=None)

# SELECT AND RENAME COLUMNS
comma = (raw_comma
    .dropna(subset = [8])
    .drop([0,9,10,11,12], axis=1)
    .rename(columns = {
        1:'write_comma',
        2:'heard_comma',
        3:'care_comma',
        4:'write_data',
        5:'heard_data',
        6:'care_data',
        7:'care_grammar',
        8:'gender',
        }))

# RECODE VALUES FOR MODELING
def yn_recode(input):
    if input == "Yes": return 1
    elif input == "No": return -1
    else: return np.nan

def scale_recode(input):
    if input == "A lot" or input == "Very important" : return 2
    elif input == "Some" or input == "Somewhat important": return 1
    elif input == "Not much" or input == "Somewhat unimportant": return -1
    elif input == "Not at all" or input == "Very unimportant": return -2
    else: return np.nan

def write_comma_recode(input):
    if input == "It's important for a person to be honest, kind, and loyal.": return 1
    elif input == "It's important for a person to be honest, kind and loyal.": return -1
    else: return np.nan

def write_data_recode(input):
    if input == "Some experts say it's important to drink milk, but the data are inconclusive.": return 1
    elif input == "Some experts say it's important to drink milk, but the data is inconclusive.": return -1
    else: return np.nan

for i in ['care_comma','care_data','care_grammar']:
    comma[i] = comma[i].apply(scale_recode)

for i in ['heard_comma','heard_data']:
    comma[i] = comma[i].apply(yn_recode)

comma["write_comma"] = comma["write_comma"].apply(write_comma_recode)
comma["write_data"] = comma["write_data"].apply(write_data_recode)

# REMOVE NA'S
ml_comma = comma.dropna().reset_index(drop = True)

###

# SET FILTERED VARIABLES 
X_pred = ml_comma.drop(columns = ['gender'])
y_pred = ml_comma['gender'] == 'Male'

# SPLIT VARIABLES
X_train, X_test, y_train, y_test = train_test_split(X_pred,y_pred,test_size=.2,random_state = 1)

# CREATE FITTED MODEL WITH TRAINING DATA
clf = RandomForestClassifier(random_state=1).fit(X_train, y_train)

# TEST MODEL AND REPORT ACCURACY
y_pred = clf.predict(X_test)
y_probs = clf.predict_proba(X_test)
score = accuracy_score(y_test, y_pred)

# GIVE FEATURE IMPORTANCE
feature_raw = pd.DataFrame(
    {'features': X_train.columns, 
    'importance': clf.feature_importances_})

feature_df = (feature_raw
    .sort_values(['importance'], ascending=False)
    .head(12)
    .reset_index(drop=True)
    )

#MAKE PLOT FOR MOST IMPORTANT FEATURES
f, ax = plt.subplots()
sns.barplot(x="importance", y="features", data=feature_df, color = 'darkblue')
ax.set_ylabel('Importance', fontsize = 10)
ax.set_xlabel('Feature Type', fontsize = 10)
ax.set_title('Features by Importance', fontsize = 15)
plt.tight_layout()
# plt.savefig('fi.jpg', dpi=600)


# CONFUSION_MATRIX
print(metrics.confusion_matrix(y_test, y_pred))
matrixpng_raw = metrics.plot_confusion_matrix(clf, X_test, y_test)

TN = metrics.confusion_matrix(y_test, y_pred)[0][0]
FP = metrics.confusion_matrix(y_test, y_pred)[0][1]
FN = metrics.confusion_matrix(y_test, y_pred)[1][0]
TP = metrics.confusion_matrix(y_test, y_pred)[1][1]

accuracy = (TN + TP) / (TN + TP + FN + FP)

sensitivity = (TP) / (TP + FN)
specificity = (TN) / (TN + FP)

precision = (TP) / (TP + FP)
negative_precision = (TN) / (TN + FN)

(sensitivity + specificity) / 2

2*((precision*sensitivity)/(precision+sensitivity))