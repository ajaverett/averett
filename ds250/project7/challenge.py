import pandas as pd
import altair as alt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics

dat = pd.read_csv('https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.csv')

# :Q quantitative: a continuous real-valued quantity
# :O ordinal: a discrete ordered quantity
# :N nominal: a discrete unordered category
# :T temporal: a time or date value

chart = (
alt.Chart(dat)
.mark_circle(size=60, color = 'red')
.encode(
    x = alt.X('hp:Q', 
        title = 'Horse Power', 
        axis=alt.Axis(labelExpr='"pre" + datum.value + "suf"')),

    y = alt.Y('mpg', 
        title = 'Miles per Gallon')))


line_plot_1 = (
alt.Chart(pd.DataFrame
    ({'x': [1980]}))
.mark_rule()
.encode(x='x'))


line_plot_2 = (
alt.Chart(pd.DataFrame
    ({'x': [160]}))
.mark_rule()
.encode(x='x')
)


text1 = (
alt.Chart
    ({'values':[{'x': 70, 'y': 25}]})
.mark_text(text='Big')
.encode(x='x:Q', y='y:Q'))


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


dat1 = dat

dat1 = dat1[['cyl','carb']]


