
import pandas as pd
import altair as alt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics

dat = pd.read_csv('https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.csv')

df = dat[['cyl','carb']]
dat.groupby('cyl')['mpg'].agg({'min'})


(df.groupby(['cyl','carb'])
    .size()
    .reset_index()
    .rename(columns={0:'count',1:'min',2:'count'})
    .pivot_table(index = 'cyl', values = 'count', columns = 'carb')
    .fillna(0)
)


dat.pivot_table(index = 'cyl', columns = 'carb',aggfunc = 'size').fillna(0)

dat1 = pd.read_excel('https://github.com/datagy/pivot_table_pandas/raw/master/sample_pivot.xlsx')

dat1.pivot_table(index = 'Region', aggfunc = 'size').reset_index()

dat1.pivot_table(index = 'Region', columns = 'Type',aggfunc = 'size')

dat1.rename(columns={'The sales':'Sales'})

dat1.query("Region == 'East'")


dat2= pd.read_csv('test.csv').set_index('index').reset_index(drop = True)

dat2.pivot_table(index = 'Region', columns = 'gadget_type',aggfunc = 'size').fillna(0)

dat2.pivot_table(index = 'Region', columns = 'gadget_type',aggfunc = 'mean').fillna(0)


dat2.count().reset_index()