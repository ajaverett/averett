#Q1
import pandas as pd
import altair as alt

url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"

names_raw = pd.read_csv(url)

alan_freq_table = (names_raw
    .query("name == 'Alan' and Total > 0")
)

alan_freq_chart = (alt.Chart(
    alan_freq_table,
    title = "Frequency of the name Alan from 1910 to 2015")
    .encode(
        x = alt.X(
            'year',
            axis=alt.Axis(format='.4'),
            title = "Birth year"),
        y = alt.Y(
            'Total',
            scale = alt.Scale(domain=[0, 10000]),
            title = "Frequency of name")
    )
    .mark_line()
)

alan_filter = (alan_freq_table
    .query('year == 2000')
    .assign(
        tlabel = "Alan's birth year ->"
        )
)

alan_mark = (alt.Chart(alan_filter)
    .encode(
        x = 'year',
        y = "Total", 
        text = 'tlabel'))

alan_full_chart = alt.layer(
    alan_freq_chart, 
    alan_mark.mark_rule(),
    alan_mark.mark_text(dx = -50, dy = 10)).configure_title(
)

alan_full_chart.save('alan_full_chart.png')

#Q2
import pandas as pd
import altair as alt
 
url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
 
names_raw = pd.read_csv(url)
 
brittany_freq_table = (names_raw
    .query("name == 'Brittany' and Total > 0")
)
 
brittany_freq_chart = (alt.Chart(
    brittany_freq_table,
    title = "Frequency of the name Brittany from 1910 to 2015")
    .encode(
        x = alt.X(
            'year',
            axis=alt.Axis(format='.4'),
            title = "Birth year"),
        y = alt.Y(
            'Total',
            title = "Frequency of name")
    )
    .mark_line()
)
 
brittany_freq_chart.save('brittany_freq_chart.png')

#Q2.5
brittany_freq_table = brittany_freq_table.set_index('year')
brittany_freq_table['Total'].idxmax() #output is 1990
brittany_freq_table['Total'].idxmin() #output is 1968

#Q3
import pandas as pd
import altair as alt
 
url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
 
names_raw = pd.read_csv(url)

christian_names_table_raw = names_raw.query(
    'name == ["Mary","Martha","Peter","Paul"] and year >= 1920 and year <= 2000'
)
christian_names_table = christian_names_table_raw.filter(
    ['name','year','Total']
)
christian_chart = (alt.Chart(
    christian_names_table, 
    title = 'Comparison of the Christian names, Mary, Martha, Peter, and Paul from 1920 to 2000' ) 
    .mark_line()
    .encode(
        x= alt.X(
                'year',
                #scale = alt.Scale(domain = [1920,2000]),
                axis=alt.Axis(format='.4'),
                title = "Birth year"),
        y= alt.Y(
                'Total',
                scale = alt.Scale(domain = [0,60000]),
                title = "Frequency of name"              
                ),
        color = 'name'
    )
)

christian_chart.save('christian_chart.png')

#Q4
import pandas as pd
import altair as alt
 
url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
 
names_raw = pd.read_csv(url)

elliott_names_table_raw = names_raw.query(
    'name == "Elliott" or name == "Elliot" or name == "Eliot"'
)
elliott_names_table = elliott_names_table_raw.filter(
    ['name','year','Total']
)
elliott_chart = (alt.Chart(
    elliott_names_table, 
    title = 'Comparison of the names, Elliott, Eliott, and Eliot from 1910 to 2010' ) 
    .mark_line()
    .encode(
        x= alt.X(
                'year',
                axis=alt.Axis(format='.4'),
                title = "Birth year"),
        y= alt.Y(
                'Total',
                title = "Frequency of name"),
        color = 'name'
    )
)

elliott_filter = (elliott_names_table_raw
    .query('year == 1982 and name == "Elliott"')
    .assign(
        tlabel = " Release of E.T. (1982) -->"
        )
)

elliott_mark = (alt.Chart(elliott_filter)
    .encode(
        x = 'year',
        y = "Total", 
        text = 'tlabel'))

elliott_chart_full = alt.layer(
    elliott_chart, 
    elliott_mark.mark_rule(),
    elliott_mark.mark_text(dx = -75, dy = 10)).configure_title(
)

elliott_chart_full.save('elliott_chart_full.png')