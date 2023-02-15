import altair as alt
import pandas as pd

source = pd.read_csv('https://gist.githubusercontent.com/omarish/5687264/raw/7e5c814ce6ef33e25d5259c1fe79463c190800d9/mpg.csv')

alt.Chart(source).mark_point().encode(
    x='weight',
    y='mpg',
).properties(
    title = "The Cake is a Lie"
).configure_title(
    fontSize=60,
    font='Comic Sans MS',
    anchor='start',
    color='red'
)