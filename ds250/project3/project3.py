#%%

import pandas as pd
import numpy as np
import datadotworld as dw
import altair as alt

#%%

#GRAND QUESTION ONE
#%%
#Find the BYUI id
gq1_1 = '''
SELECT DISTINCT *
FROM schools
WHERE state = "ID"
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_1_1 = dw.query(baseball_path, gq1_1)
gq1_1 = grand_table_1_1.dataframe

#%%
#Find the player id
gq1_2 = '''
SELECT DISTINCT playerid
FROM CollegePlaying
WHERE schoolid = "idbyuid"
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_1_2 = dw.query(baseball_path, gq1_2)
gq1_2 = grand_table_1_2.dataframe

#%%
#Make the table from GQ1
gq1_3 = '''
SELECT table1.playerID AS `Player ID`,
    table1.namegiven AS `Player Name`,
    table1.schoolID AS `School ID`, 
    table1.name_full AS `University`,
    s.salary AS Salary,
    s.yearid AS Year
FROM
        (SELECT cp.playerID,
            cp.schoolID, 
            cp.yearID,
            p.namegiven,
            s.name_full
        FROM CollegePlaying as cp
        JOIN people as p ON p.playerid = cp.playerid 
        JOIN Schools as s ON cp.schoolid = s.schoolid
        WHERE s.schoolid = "idbyuid") AS table1

JOIN Salaries as s ON s.playerid = table1.playerid
ORDER BY Year, "Player ID"
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_1_3 = dw.query(baseball_path, gq1_3)
gq1_3 = grand_table_1_3.dataframe
#%%
#print(gq1_3.to_markdown())

#%%
#GRAND QUESTION TWO
#part a
gq2_1 = '''
SELECT 
    p.namegiven AS Name,
    b.yearID AS `Year`,
    b.h AS `Hits`,
    b.ab AS `At Bats`,
    (b.h/b.ab) AS `Batting Average`
FROM batting as b
JOIN people as p ON b.playerid = p.playerid
WHERE b.ab > 0
ORDER BY `Batting Average` DESC, yearID
LIMIT 5
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_2_1 = dw.query(baseball_path, gq2_1)
gq2_1 = grand_table_2_1.dataframe
#%%
print(gq2_1.to_markdown())

#%%
#part b
gq2_2 = '''
SELECT 
    p.namegiven AS Name,
    b.yearID AS `Year`,
    b.h AS `Hits`,
    b.ab AS `At Bats`,
    (b.h/b.ab) AS `Batting Average`
FROM batting as b
JOIN people as p ON b.playerid = p.playerid
WHERE b.ab > 10
ORDER BY `Batting Average` DESC, yearID
LIMIT 5
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_2_2 = dw.query(baseball_path, gq2_2)
gq2_2 = grand_table_2_2.dataframe
#%%
#part c
gq2_3 = '''
SELECT 
    p.namegiven AS Name,
    `Hits`,
    `At Bats`,
    `Batting Average`     
FROM
    (SELECT 
        playerid,
        SUM(b.h) AS `Hits`,
        SUM(b.ab) AS `At Bats`,
        (SUM(b.h)/SUM(b.ab)) AS `Batting Average`
    FROM batting as b
    GROUP BY playerID
    HAVING SUM(b.ab) > 100 
    ORDER BY `Batting Average` DESC, yearID
    LIMIT 5
    ) AS table1
JOIN people as p ON table1.playerid = p.playerid
'''
baseball_path = "byuidss/cse-250-baseball-database"
grand_table_2_3 = dw.query(baseball_path, gq2_3)
gq2_3 = grand_table_2_3.dataframe
#%%



# %%
#GRAND QUESTION THREE

# QUERIES
############
query3_allstar = '''
SELECT t.name AS `Team`,
    SUM(a.gamenum) AS `AllStar Games`
FROM AllstarFull as a 
JOIN teams as t ON a.teamid = t.teamid
GROUP BY a.teamid
HAVING SUM(a.gamenum) > 0
ORDER BY SUM(a.gamenum) DESC
LIMIT 16
'''

query3_salary = '''
SELECT t.name AS `Team`,
    SUM(s.salary) AS `Overall Combined Salary`
FROM Salaries as s 
JOIN teams as t ON s.teamid = t.teamid
GROUP BY s.teamid
HAVING SUM(s.salary) > 0
ORDER BY SUM(s.salary) DESC
LIMIT 16
'''



# TABLES
############
baseball_path = "byuidss/cse-250-baseball-database"
pulled3_allstar = dw.query(baseball_path, query3_allstar)
pulled3_salary = dw.query(baseball_path, query3_salary)

table3_allstar = pulled3_allstar.dataframe
table3_salary = pulled3_salary.dataframe

# table3_allstar1 = pulled3_allstar.dataframe.sort_values('Team')
# table3_salary1 = pulled3_salary.dataframe.sort_values('Team')

table3_full = table3_allstar.merge(table3_salary)
pd.concat([table3_allstar, table3_salary], axis=1)

# table3_full = (table3_allstar
#     .assign(Overall_Combined_salary = lambda x: ((
#         table3_salary['Overall Combined Salary']
#     ))).reset_index()
# )

table3_allstar.Team = table3_allstar.Team.astype('category')
table3_salary.Team = table3_salary.Team.astype('category')
table3_full.Team = table3_full.Team.astype('category')

table3_allstar_filtered = table3_allstar.query('Team in ["New York Yankees","Baltimore Orioles"]')
table3_salary_filtered = table3_salary.query('Team in ["New York Yankees","Baltimore Orioles"]')



#%% CHARTS
############
allstar_order = ['New York Yankees','Pittsburgh Pirates','St. Louis Cardinals','Chicago White Sox','Cleveland Indians','Cincinnati Reds','Detroit Tigers','Boston Red Sox','Chicago Cubs','Baltimore rioles','San Francisco Giants','Los Angeles Dodgers','Philadelphia Phillies','Washington Senators','Minnesota Twins','Kansas City Athletics']

#%% CHARTS- Allstar
############
chart3_allstar_full = alt.Chart(table3_allstar).encode(
    alt.X('Team',sort='-y'),
    alt.Y('AllStar Games'),
    tooltip='AllStar Games'
     ).mark_circle(size=50, color = '#7B536D')

chart3_allstar_filtered = alt.Chart(table3_allstar_filtered).encode(
    alt.X('Team'),
    alt.Y('AllStar Games'),
    tooltip='AllStar Games',
     ).mark_circle(size=80,color = '#ff6961')

chart3_allstar_highlight =(alt
.layer(
    chart3_allstar_full,
    chart3_allstar_filtered)
).encode(alt.X(sort = '-y'))

#%% CHARTS- Salary
############
chart3_salary_full = alt.Chart(table3_salary).encode(
    alt.X('Team',sort= ['New York Yankees','Pittsburgh Pirates','St. Louis Cardinals','Chicago White Sox','Cleveland Indians','Cincinnati Reds','Detroit Tigers','Boston Red Sox','Chicago Cubs','Baltimore rioles','San Francisco Giants','Los Angeles Dodgers','Philadelphia Phillies','Washington Senators','Minnesota Twins','Kansas City Athletics']),
    alt.Y('Overall Combined Salary'),
    tooltip='Overall Combined Salary'
     ).mark_circle(size=50, color = '#4D5371')

chart3_salary_filtered = alt.Chart(table3_salary_filtered).encode(
    alt.X('Team'),
    alt.Y('Overall Combined Salary'),
    tooltip='Overall Combined Salary',
     ).mark_circle(size=80 ,color = '#336CE7')

chart3_salary_highlight =(alt
.layer(
    chart3_salary_full,
    chart3_salary_filtered)
.encode(alt.X(sort = ['New York Yankees','Pittsburgh Pirates','St. Louis Cardinals','Chicago White Sox','Cleveland Indians','Cincinnati Reds','Detroit Tigers','Boston Red Sox','Chicago Cubs','Baltimore rioles','San Francisco Giants','Los Angeles Dodgers','Philadelphia Phillies','Washington Senators','Minnesota Twins','Kansas City Athletics'])))

#%% CHARTS- combined
############
chart3_allstar_highlight | chart3_salary_highlight

#%% STATS- combined
############
corr_test = (table3_full
.reset_index()
.drop(columns=['index','Team'])
.reset_index(drop = True)
)

corr_test.corr(method='spearman', min_periods=1)

