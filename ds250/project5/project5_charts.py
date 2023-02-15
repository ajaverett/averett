#%%
# IMPORTS
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

url = 'https://github.com/fivethirtyeight/data/raw/master/star-wars-survey/StarWars.csv'
dat = pd.read_csv(url, encoding_errors ='ignore', skiprows=2, header=None)

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

#CHART ONE
# --- Prepares data
dat1 = (dat_charts.loc[
    (dat_charts['seen_m1'] == 1) | 
    (dat_charts['seen_m2'] == 1) |
    (dat_charts['seen_m3'] == 1) | 
    (dat_charts['seen_m4'] == 1) |    
    (dat_charts['seen_m5'] == 1) | 
    (dat_charts['seen_m6'] == 1) 
    ].iloc[:,list(range(3,9))]
    .sum()
    .reset_index()
    .rename(columns={0: "raw_val"})
    ).replace({
        'seen_m1': "The Phantom Menace",
        'seen_m2': "Attack of the Clones",
        'seen_m3': "Revenge of the Sith",
        'seen_m4': "A New Hope",
        'seen_m5': "The Empire Strikes Back",
        'seen_m6': "Return of the Jedi"
         })

dat1['percents'] = round(dat1['raw_val']/(len(dat_charts))*100)

movie_sort = dat1['index'].to_numpy()

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
    fontSize=21,
    subtitleFontSize=17,
    anchor='start')

chart1_full.save('chart1.svg')

# CHART TWO
# --- Prepares data
dat2 = dat_charts.loc[
    (dat_charts['seen_m1'] == 1) & 
    (dat_charts['seen_m2'] == 1) &
    (dat_charts['seen_m3'] == 1) & 
    (dat_charts['seen_m4'] == 1) &    
    (dat_charts['seen_m5'] == 1) & 
    (dat_charts['seen_m6'] == 1) 
    ] 

dat2 = pd.DataFrame(data={
    'raw_val': [len(dat2[dat2.rate_m1 == 6]),
        len(dat2[dat2.rate_m2 == 1]),
        len(dat2[dat2.rate_m3 == 1]),
        len(dat2[dat2.rate_m4 == 1]),
        len(dat2[dat2.rate_m5 == 1]),
        len(dat2[dat2.rate_m6 == 1])]},
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
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(text=('percents'))

chart2_full = (chart2 + chart2_text).properties(title={
      "text": ["What's the Best 'Star Wars' Movie?"], 
      "subtitle": ["Of 471 respondents who have seen all six films"],
      "color": "black",
      "subtitleColor": "black"
    }, width = 300
).configure_title(
    fontSize=21,
    subtitleFontSize=14,
    anchor='start')

chart2_full.save('chart2.svg')
