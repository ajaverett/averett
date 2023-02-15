# %%
from math import ceil
import pandas as pd
import altair as alt
import numpy as np
from scipy import stats
 # %%
url = 'https://github.com/byuidatascience/data4missing/raw/master/data-raw/flights_missing/flights_missing.json'
flights = pd.read_json(url)
# %%
clean_flights = (flights
       .replace(-999, 0)
       .replace('1500+', 1500)
       .replace('Febuary', 'February')
       .query('month != "n/a"')
)


# %%
true_weather_delays = (clean_flights
       .assign(
              weather_delays_aircraft = clean_flights.num_of_delays_late_aircraft * .3,
              weather_delays_nas = np.where(clean_flights.month.isin(['April', 'May', 'June', 'July', 'August']), 
              clean_flights.num_of_delays_nas * .4, 
              clean_flights.num_of_delays_nas *.65),
              weather_delays_total = lambda x: x.weather_delays_aircraft + x.weather_delays_nas + clean_flights.num_of_delays_weather,
       )
       .groupby(['airport_code'])
       .sum()
       .reset_index()
       .filter(['airport_code', 'month', 'num_of_flights_total', 'num_of_delays_weather', 'weather_delays_aircraft', 'weather_delays_nas', 'weather_delays_total', 'num_of_delays_total', 'percent_weather_delays'])

)
true_weather_delays


true_weather_delays_percent = (true_weather_delays
       .assign(
              percent_weather_delays = (
                  true_weather_delays.weather_delays_total / true_weather_delays.num_of_flights_total) * 100
       )
)
true_weather_delays_percent


# %%

