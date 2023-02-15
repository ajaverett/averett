#%%

import pandas as pd
import numpy as np
import datadotworld as dw
import altair as alt

#%%
query = '''
SELECT *
FROM drinks
'''

alcohol_path = "fivethirtyeight/alcohol-consumption"
sql_query = dw.query(alcohol_path, query)
df = sql_query.dataframe

df2 = pd.read_csv("C:/Users/Aj/Desktop/Stuff/worldpop.csv").rename(columns={"Region, subregion, country or area *": "country"})

df2['2020'] = (df2['2020']
    .replace(' ','', regex=True)
    .astype('int'))

df = df.replace('USA', 'United States of America')

df_temp = df.merge(df2, how='inner', on='country').sort_values('2020', ascending=False)

#df_temp = df_temp[df_temp.beer_servings != 0]#.head(12)

chart = (
alt.Chart(df_temp)
.mark_bar()
.encode(
    y = alt.Y('country', 
        title = 'x val', 
        axis=alt.Axis(labelExpr='"" + datum.value + ""'),
        sort=alt.EncodingSortField(field="beer_servings",
                                    
                                    order='descending')
                                    ),

    x = alt.X('beer_servings', 
        title = 'y val')))






#df.query('country.str.startswith("U")')



# %%
