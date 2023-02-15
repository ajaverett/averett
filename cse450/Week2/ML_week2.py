# IMPORTS
#%% Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pickle
from sklearn import metrics
from sklearn.metrics            import accuracy_score
from sklearn.model_selection    import train_test_split
from imblearn.over_sampling     import RandomOverSampler
from sklearn.ensemble           import RandomForestClassifier

df = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/bank.csv")

#%% Clean Data Set

### TARGET
df['y'] = df['y'].replace(["yes","no"],[1,0])

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
 'contact',
 'y']

dat = dat.filter(items = best_features_list)

X = dat.drop(columns=['y'])
y = dat['y']

#%% Oversample for balance
ro = RandomOverSampler()

X_pred, y_pred = ro.fit_resample(X, y)

#%% Split and train data
X_train, X_test, y_train, y_test = train_test_split(X_pred,y_pred,test_size=.1, random_state=0)    # SPLIT VARIABLES

clf = RandomForestClassifier(random_state=0).fit(X_train, y_train)  

y_pred = clf.predict(X_test)  

#%% Report Accuracy
score = accuracy_score(y_test, y_pred)
print(score)

#%% SAVE MODEL
filename = 'bank_model.sav'
pickle.dump(clf, open(filename, 'wb'))


#%% Report feature importance, ROC, Confusion Matrix
#Feature Importance
feature_df = pd.DataFrame(
    {'features': X_train.columns,
    'importance': clf.feature_importances_})

data_dictionary = {
"age" : "age",
"job" : "job",
"marital" : "marital status",
"education" : "education",
"default" : "default",
"housing" : "housing loan",
"loan" : "personal loan",
"contact" : "contact type",
"month" : "last contact month",
"dayofweek" : "last contact day",
"campaign" : "no. of contacts",
"pdays" : "days since last contact",
"previous" : "no. of contacts before",
"poutcome" : "prev. campaign outcome",
"emp.var.rate" : "employment variation rate",
"cons.price.idx" : "consumer price index",
"cons.conf.idx" : "consumer confidence index",
"euribor3m" : "euribor 3 month rate",
"nr.employed" : "no. of employees",
"y" : "subscribed for term deposit"
}

data_dictionary_df = pd.DataFrame(list(data_dictionary.items()), columns=['Attribute', 'description'])

cool_df = data_dictionary_df.merge(feature_df, left_on='Attribute', right_on='features').drop(columns = ['Attribute','features'])



sns.barplot(
    data=cool_df, 
    x="importance", 
    y="description", 
    order=cool_df.sort_values('importance', ascending = False).description)
plt.xlabel('Importance for the Random Forest Model') 
plt.ylabel('Features')
plt.title("Most Important Variables for\nPredicting a Bank Subscription")

#ROC-AUC
metrics.plot_roc_curve(clf,X_test,y_test)

#CM
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = clf.classes_)
cm_display.plot(cmap=plt.cm.Purples)

tp = confusion_matrix[0][0]
fp = confusion_matrix[0][1]
tn = confusion_matrix[1][1]
fn = confusion_matrix[1][0]

accuracy = (tp + tn) / (tp + fp + tn + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1_score = 2*(precision*recall)/(precision+recall)
specificity = tn / (tn + fp)
npv = tn / (tn + fn)


ML_metrics = {'accuracy': accuracy, 
             'precision': precision, 
             'recall': recall, 
             'f1_score': f1_score, 
             'specificity': specificity, 
             'npv': npv}

metrics_df = pd.DataFrame(
    {'metric': list(ML_metrics.keys()), 
    'value': list(ML_metrics.values())})


sns.barplot(x='value', y="metric", data=metrics_df)
plt.xlim(.85,1.05)
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))


