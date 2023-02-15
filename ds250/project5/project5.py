#%%
# IMPORTS
import altair as alt
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn import metrics
from sklearn.ensemble           import RandomForestClassifier
from sklearn.metrics            import accuracy_score
from sklearn.model_selection    import train_test_split

url = 'https://github.com/fivethirtyeight/data/raw/master/star-wars-survey/StarWars.csv'
dat = pd.read_csv(url, encoding_errors ='ignore', skiprows=2, header=None)

#### GRAND QUESTION ONE ####

dat = (dat.rename(columns = {
    0:'respondent_id',  1:'seen_any',       2:'fan_sw',         3:'seen_m1',
    4:'seen_m2',        5:'seen_m3',        6:'seen_m4',        7:'seen_m5',
    8:'seen_m6',        9:'rate_m1',        10:'rate_m2',       11:'rate_m3',
    12:'rate_m4',       13:'rate_m5',       14:'rate_m6',       15:'rate_han',
    16:'rate_luke',     17:'rate_leia',     18:'rate_anakin',   19:'rate_obiwan',
    20:'rate_palpatine',21:'rate_vader',    22:'rate_lando',    23:'rate_boba',
    24:'rate_c3p0',     25:'rate_r2d2',     26:'rate_jarjar',   27:'rate_padme',
    28:'rate_yoda',     29:'shot_first',    30:'know_eu',       31:'fan_eu',
    32:'fan_st',        33:'gender',        34:'age',           35:'house_income',
    36:'edu',           37:'region'}))

dat_charts = dat

dat_charts.iloc[:,list(range(3,9))] = np.where((dat_charts.iloc[:,list(range(3,9))].isnull()==False),1,dat_charts.iloc[:,list(range(3,9))])
dat_charts.iloc[:,list(range(3,9))] = np.where((dat_charts.iloc[:,list(range(3,9))].isnull()==True),0,dat_charts.iloc[:,list(range(3,9))])

#### GRAND QUESTION THREE ####
#CHART 1
# --- Prepares data
dat1 = (dat_charts.loc[
        (dat_charts['seen_m1'] == 1) | (dat_charts['seen_m2'] == 1) |
        (dat_charts['seen_m3'] == 1) | (dat_charts['seen_m4'] == 1) |
        (dat_charts['seen_m5'] == 1) | (dat_charts['seen_m6'] == 1)
    ].iloc[:,list(range(3,9))]
    .sum()
    .reset_index()
    .rename(columns={0: "raw_val"})
    ).replace({
        'seen_m1': "The Phantom Menace",        'seen_m2': "Attack of the Clones",
        'seen_m3': "Revenge of the Sith",       'seen_m4': "A New Hope",
        'seen_m5': "The Empire Strikes Back",   'seen_m6': "Return of the Jedi"
         })

dat1['percents'] = round(dat1['raw_val']/(len(dat_charts))*100)

movie_sort = dat1['index'].to_numpy() #List of movies in categorical order

# --- Prepares chart
source = dat1

chart1 = alt.Chart(source).mark_bar().encode(
    alt.Y('index',sort = movie_sort,title=''),
    alt.X("percents",axis = None)
)

chart1_text = chart1.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(text=('percents'))
chart1_full = (chart1 + chart1_text).properties(title={
      "text": ["Which 'Star Wars' Movies Have You Seen?"],
      "subtitle": ["Of 835 respondents who have seen any film"],
      "color": "black",
      "subtitleColor": "black"
    }
).configure_title(
    fontSize=21, subtitleFontSize=17, anchor='start')

chart1_full.save('chart1.svg')

# CHART 2
# --- Prepares data
dat2 = dat_charts.loc[
    (dat_charts['seen_m1'] == 1) & (dat_charts['seen_m2'] == 1) &
    (dat_charts['seen_m3'] == 1) & (dat_charts['seen_m4'] == 1) &
    (dat_charts['seen_m5'] == 1) & (dat_charts['seen_m6'] == 1)
    ]

dat2 = pd.DataFrame(data={
    'raw_val': [len(dat2[dat2.rate_m1 == 6]), len(dat2[dat2.rate_m2 == 1]),
        len(dat2[dat2.rate_m3 == 1]), len(dat2[dat2.rate_m4 == 1]),
        len(dat2[dat2.rate_m5 == 1]), len(dat2[dat2.rate_m6 == 1])]},
    index = movie_sort
        ).reset_index()

dat2['percents'] = round(dat2['raw_val']/(dat2['raw_val'].sum())*100)

# --- Prepares chart
source = dat2

chart2 = alt.Chart(source).mark_bar().encode(
    alt.Y('index',sort = movie_sort,title=''),
    alt.X("percents",axis = None)
)

chart2_text = chart2.mark_text(
    align='left',
    baseline='middle',
    dx=3
).encode(text=('percents'))

chart2_full = (chart2 + chart2_text).properties(title={
      "text": ["What's the Best 'Star Wars' Movie?"],
      "subtitle": ["Of 471 respondents who have seen all six films"],
      "color": "black",
      "subtitleColor": "black"
    }, width = 300
).configure_title(
    fontSize=21, subtitleFontSize=14, anchor='start')

chart2_full.save('chart2.svg')


#### GRAND QUESTION TWO ####

dat= dat[(dat.seen_any == "Yes")]
temp = dat.dropna(subset = ['house_income','age'])

dat.iloc[:,list(range(3,9))] = np.where((dat.iloc[:,list(range(3,9))].notnull()==True),1,dat.iloc[:,list(range(3,9))])  # 3-8 VALUE FIX
dat.iloc[:,list(range(3,9))] = np.where((dat.iloc[:,list(range(3,9))].isnull()==True),0,dat.iloc[:,list(range(3,9))])
dat.iloc[:,list(range(9,15))] = np.where((dat.iloc[:,list(range(9,15))].isnull()==True),3.5,dat.iloc[:,list(range(9,15))])  # 9-14 VALUE FIX
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Very favorably'),2,dat.iloc[:,list(range(15,29))])  # 15-28 VALUE FIX
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Somewhat favorably'),1,dat.iloc[:,list(range(15,29))])
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Neither favorably nor unfavorably (neutral)'),0,dat.iloc[:,list(range(15,29))])
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Somewhat unfavorably'),-1,dat.iloc[:,list(range(15,29))])
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Very unfavorably'),-2,dat.iloc[:,list(range(15,29))])
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))].isnull()==True),0,dat.iloc[:,list(range(15,29))])
dat.iloc[:,list(range(15,29))] = np.where((dat.iloc[:,list(range(15,29))]=='Unfamiliar (N/A)'),0,dat.iloc[:,list(range(15,29))])

dat = pd.get_dummies(data=dat, columns=['seen_any', 'fan_sw','shot_first', 'know_eu','fan_eu','fan_st','gender','region'])
dat = (dat.rename(columns = {
    "shot_first_I don't understand this question":'shot_first_idk', 'region_East North Central':'region_1',
    'region_East South Central':'region_2',                         'region_Middle Atlantic':'region_3',
    'region_Mountain':'region_4',                                   'region_New England':'region_5',
    'region_Pacific':'region_6',                                    'region_South Atlantic':'region_7',
    'region_West North Central':'region_8',                         'region_West South Central':'region_9'}))

i = 28          #income HOT-ENCODE
dat.iloc[:,[i]] = np.where((dat.iloc[:,[i]] == '$0 - $24,999'),0,dat.iloc[:,[i]])
dat.iloc[:,[i]] = np.where((dat.iloc[:,[i]] == '$25,000 - $49,999'),0,dat.iloc[:,[i]])
dat.iloc[:,[i]] = np.where((dat.iloc[:,[i]] == '$50,000 - $99,999'),1,dat.iloc[:,[i]])
dat.iloc[:,[i]] = np.where((dat.iloc[:,[i]] == '$100,000 - $149,999'),1,dat.iloc[:,[i]])
dat.iloc[:,[i]] = np.where((dat.iloc[:,[i]] == '$150,000+'),1,dat.iloc[:,[i]])

j = 29          #education VALUE FIX
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]] == 'Less than high school degree'),9,dat.iloc[:,[j]])
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]] == 'High school degree'),12,dat.iloc[:,[j]])
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]] == 'Some college or Associate degree'),14,dat.iloc[:,[j]])
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]] == 'Bachelor degree'),16,dat.iloc[:,[j]])
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]] == 'Graduate degree'),19,dat.iloc[:,[j]])
dat.iloc[:,[j]] = np.where((dat.iloc[:,[j]].isnull()==True),12,dat.iloc[:,[j]])

temp_age = (temp.age
    .str.split('-',expand = True)
    .rename({0:'age_min'},axis=1)
    .age_min.str.replace(",|\$|\+| |\>",'')
    .astype('int'))

dat = pd.concat([dat,temp_age], axis=1)
dat=dat.drop(columns=['respondent_id','age',], axis = 1)
dat.reset_index(drop=True)
dat=dat.dropna()
dat.to_csv('dat.csv')

#%%
X_pred = dat.drop(columns = ['house_income'])   # SET FILTERED VARIABLES
y_pred = dat['house_income']
X_pred=X_pred.astype('int')
y_pred=y_pred.astype('int')

X_train, X_test, y_train, y_test = train_test_split(X_pred,y_pred,test_size=.26,random_state = 22)    # SPLIT VARIABLES

clf = RandomForestClassifier(random_state=10).fit(X_train, y_train)  # CREATE MODEL WITH TRAINING DATA

y_pred = clf.predict(X_test)    # TEST MODEL AND REPORT ACCURACY
score = accuracy_score(y_test, y_pred)
print(score)

#%%
# GIVE FEATURE IMPORTANCE
feature_df = pd.DataFrame(
    {'features': X_train.columns,
    'importance': clf.feature_importances_})

best_features = feature_df.sort_values(['importance'],ascending = False).head(6).reset_index(drop=True)

best_features['importance'] = (round(best_features['importance']*100,2)).astype(str) + ' %'

# print(best_features.to_markdown())

metrics.plot_roc_curve(clf,X_test,y_test)
