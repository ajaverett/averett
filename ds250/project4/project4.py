# IMPORTS
import imp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.api.types import CategoricalDtype
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import metrics

# DATA IMPORT
dwellings_denver = pd.read_csv("https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_denver/dwellings_denver.csv")
dwellings_ml = pd.read_csv("https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_ml/dwellings_ml.csv")
dwellings_neighborhoods_ml = pd.read_csv("https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_neighborhoods_ml/dwellings_neighborhoods_ml.csv")   

# DATA DEFINE
dwellings_complete = dwellings_ml.merge(dwellings_neighborhoods_ml)

# GRAND QUESTION ONE
# %%
# VAR 1
fig, ax = plt.subplots()
gq_1a = sns.histplot(
    data=dwellings_complete,
    ax = ax,
    x="livearea", 
    hue="before1980",
    element="step",
#    log_scale=True
)
ax.set_xlim(0,4000)
ax.set_xlabel("Living Area", fontsize = 15)
ax.set_ylabel("Number of Houses", fontsize = 15)
ax.set_title("Comparison of living area between \n houses before and after 1980", fontsize = 15)
plt.tight_layout()
#plt.savefig('gq1a.jpg', dpi=600)

# %%
# VAR 2 (UNUSED)
fig, ax = plt.subplots()
sns.histplot(data=dwellings_complete, 
    x="sprice", 
    hue="before1980",
    element="step",
    #log_scale=True
)
ax.set_xlim(0,700000)
ax.set_xlabel("Selling Price", fontsize = 15)
ax.set_ylabel("Number of Houses", fontsize = 15)
ax.set_title("Comparison of selling price between \n houses before and after 1980", fontsize = 15)
plt.tight_layout()
#plt.savefig('gq1b.jpg', dpi=600)

# %%
# VAR 3
gq1d_raw = dwellings_complete.filter(['stories','before1980'])
gq1d_raw['stories'] = gq1d_raw['stories'].astype(str)
x_labels = ['1','2','3','4']
x_cat_order = CategoricalDtype(categories = x_labels, ordered = True)
gq1d_raw['stories'] = gq1d_raw['stories'].astype(x_cat_order)
fig, ax = plt.subplots()
sns.histplot(data= gq1d_raw, 
    x="stories", 
    hue="before1980",
    element="bars",
    discrete=True,
    kde = False
)
ax.set_xlabel("Number of Stories", fontsize = 10)
ax.set_ylabel("Number of Houses", fontsize = 10)
ax.set_title("Comparison of story amount between \n houses before and after 1980", fontsize = 15)
plt.tight_layout()
#plt.savefig('gq1c.jpg', dpi=600)

# %%
#VAR 4
gq1d_raw = dwellings_complete.filter(['nbhd_101','before1980'])
gq1d_raw['nbhd_101'] = gq1d_raw['nbhd_101'].astype(str)
fig, ax = plt.subplots()
sns.histplot(data= gq1d_raw, 
    x="nbhd_101", 
    hue="before1980",
    element="bars",
    discrete=True,
    kde = False,
)
ax.set_xlabel("If in Neighborhood One (1 for yes, 0 for no)", fontsize = 10)
ax.set_ylabel("Number of Houses", fontsize = 10)
ax.set_title("Neighborhood One houses by year", fontsize = 15)
plt.tight_layout()
#plt.savefig('gq1d.jpg', dpi=600)

# %%
#GRAND QUESTION TWO

# SET FILTERED VARIABLES 
X_pred = dwellings_complete.drop(columns = ['before1980','yrbuilt','parcel'])
y_pred = dwellings_complete['before1980']

# SPLIT VARIABLES
X_train, X_test, y_train, y_test = train_test_split(X_pred,y_pred,test_size=.25,random_state = 1)

# CREATE MODEL WITH TRAINING DATA
clf = tree.DecisionTreeClassifier(random_state = 420).fit(X_train, y_train)

# TEST MODEL AND REPORT ACCURACY
y_pred = clf.predict(X_test)
y_probs = clf.predict_proba(X_test)
score = accuracy_score(y_test, y_pred)

# GIVE FEATURE IMPORTANCE
feature_df = pd.DataFrame(
    {'features': X_train.columns, 
    'importance': clf.feature_importances_})

#feature_df

# TABULATE FEATURE IMPORTANCE
gq3a = (feature_df
    .sort_values(['importance'], ascending=False)
    .head(6)
    .reset_index(drop=True)
    .drop(columns=['importance'])    
    )

gq3a1 = (feature_df
    .sort_values(['importance'], ascending=False)
    .head(12)
    .reset_index(drop=True)
    #.drop(columns=['importance'])    
    )

#MAKE PLOT FOR MOST IMPORTANT FEATURES
f, ax = plt.subplots()
sns.barplot(x="importance", y="features", data=gq3a1, color = 'darkblue')
ax.set_ylabel('Importance', fontsize = 10)
ax.set_xlabel('Feature Type', fontsize = 10)
ax.set_title('Top 12 Most Important Features \n in Determining Target', fontsize = 15)
plt.tight_layout()
plt.savefig('gq3.jpg', dpi=600)


# GRAND QUESTION THREE
gq3b = dwellings_complete.filter(['arcstyle_ONE-STORY', 'gartype_Att', 
    'quality_C', 'livearea', 'stories', 'basement', 'before1980']).sample(500)

gq3c = sns.pairplot(gq3b, hue = 'before1980')

# %%
gq3d = gq3b.corr().abs()
gq3e = sns.heatmap(gq3d, center = 1)
plt.tight_layout()
get_figure = gq3e.get_figure()    
#get_figure.savefig('gq3e.jpg', dpi=600)

#%%
print(metrics.confusion_matrix(y_test, y_pred))
matrixpng_raw = metrics.plot_confusion_matrix(clf, X_test, y_test)
# plt.savefig('matrix.jpg', dpi=600)

# GRAND QUESTION FOUR

#%%
metrics.plot_roc_curve(clf,X_test,y_test)
# plt.savefig('roc.jpg', dpi=600)


