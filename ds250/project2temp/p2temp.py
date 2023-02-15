import pandas as pd
import numpy as np
import altair as alt

flights = pd.read_json('https://raw.githubusercontent.com/byuidatascience/data4missing/master/data-raw/flights_missing/flights_missing.json')


########

flights.head()
flights.isnull().sum()

########

flights = (flights
    .replace(['n/a', -999], np.nan))

flights[['year', 'month']] = (
    flights[['year', 'month']]
    .fillna(method='ffill'))


# no lambda

flights['minutes_delayed_carrier'] = (
    flights['minutes_delayed_carrier']
    .fillna(flights.groupby('month')['minutes_delayed_carrier']
    .transform('mean')))

# Sort Altair by month

flights1 = (flights
    .groupby('month').mean()
    .filter(['minutes_delayed_total'])
    .reset_index()
    .replace('n/a', np.nan)
    .replace('Febuary','February')
    .dropna(subset=['month']))

new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

alt.Chart(flights1).mark_line().encode(
    x=alt.X('month', sort=new_order),
    y='minutes_delayed_total'
)

flights_3a = flights.assign(
	num_of_delays_weather = lambda x: x.num_of_delays_weather,
	num_of_delays_late_aircraft_weather = lambda x: x.num_of_delays_late_aircraft*.3,
	num_of_delays_nas_weather = lambda x: np.where(
		x.month.isin(['April','May','June','July','August']),
		x.num_of_delays_nas*0.4,
		x.num_of_delays_nas*0.65))


true_weather_delays = (flights1
       .assign(
              weather_delays_aircraft = flights1.num_of_delays_late_aircraft * .3,
              weather_delays_nas = np.where(
                flights1.month.isin(['April', 'May', 'June', 'July', 'August']),
                flights1.num_of_delays_nas * .4,
                flights1.num_of_delays_nas *.65),
              weather_delays_total = lambda x: x.weather_delays_aircraft + x.weather_delays_nas + flights1.num_of_delays_weather,
       )
       .groupby(['airport_code'])
       .sum()
       .reset_index()
       .filter(['airport_code', 'month', 'num_of_delays_weather', 'weather_delays_aircraft', 'weather_delays_nas', 'weather_delays_total', 'num_of_delays_total', 'percent_weather_delays'])
)

true_weather_delays

true_weather_delays = (flights1
       .assign(
              weather_delays_aircraft = flights1.num_of_delays_late_aircraft * .3,
              weather_delays_nas = np.where(flights1.month.isin(['April', 'May', 'June', 'July', 'August']), flights1.num_of_delays_nas * .4, flights1.num_of_delays_nas *.65),
              weather_delays_total = lambda x: x.weather_delays_aircraft + x.weather_delays_nas + flights1.num_of_delays_weather,
       ))