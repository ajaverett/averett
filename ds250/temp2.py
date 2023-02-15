import pandas as pd
import numpy as np
import altair as alt


dat = pd.read_csv('https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.csv')

df2 = (dat
    .pivot_table(columns = 'carb',
                index = ['cyl'],
                aggfunc='size')
    .fillna(0)
    .astype(int)
    .reset_index(drop=True)
)

# Note that hp has missing values, and you will have to replace them with the mean.
# Please drop all cars with a missing name.

df = dat.dropna(subset = ['car'])

df['hp'] = (df['hp']
    .fillna(round(
        df['hp'].mean()
        )))


chart = (
alt.Chart(df)
.mark_circle(size=60, color = 'red')
.encode(
    x = alt.X('hp:Q', 
        title = 'Horse Power', 
        axis=alt.Axis(labelExpr='"pre" + datum.value + "suf"')),

    y = alt.Y('mpg', 
        title = 'Miles per Gallon')))


line_plot_1 = (
alt.Chart(pd.DataFrame
    ({'x': [80]}))
.mark_rule()
.encode(x='x'))


line_plot_2 = (
alt.Chart(pd.DataFrame
    ({'x': [160]}))
.mark_rule()
.encode(x='x')
)


text2 = (
alt.Chart
    ({'values':[{'x': 70, 'y': 25}]})
.mark_text(text='Big')
.encode(x='x:Q', y='y:Q'))


text3 = (
alt.Chart
    ({'values':[{'x': 148, 'y': 20}]})
.mark_text(text='Real Big')
.encode(x='x:Q', y='y:Q'))


all = ((chart + line_plot_1 + line_plot_2 + text2 + text3)
.properties(
    title= {
      "text": ["Super cool title"],
      "subtitle": ['Super cool subtitle']
    },
    width = 400)
.configure_title(anchor='start'
))

all