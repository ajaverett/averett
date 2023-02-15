---
title: "Untitled"
author: "Aj Averett"
date: '2022-05-12'
output: 
  html_document:
    keep_md: true
---



```r
library(tidyverse)
```

```
## -- Attaching packages --------------------------------------- tidyverse 1.3.1 --
```

```
## v ggplot2 3.3.5     v purrr   0.3.4
## v tibble  3.1.6     v dplyr   1.0.8
## v tidyr   1.2.0     v stringr 1.4.0
## v readr   2.1.2     v forcats 0.5.1
```

```
## -- Conflicts ------------------------------------------ tidyverse_conflicts() --
## x dplyr::filter() masks stats::filter()
## x dplyr::lag()    masks stats::lag()
```

```r
library(readr)
library(pander)
rawstonks <- read_rds("https://github.com/byuistats/data/blob/master/Dart_Expert_Dow_6month_anova/Dart_Expert_Dow_6month_anova.RDS?raw=true") 

stonks <- rawstonks %>% 
  separate(contest_period, c('date1','date2') ,sep = '-') %>% 
  separate(date2, c('month','year2') ,sep = -4) %>% 
  select(-date1) %>% 
  filter(variable == 'DJIA') %>% 
  mutate(month = recode(month, "Dec." = 'December', "Febuary" = 'February')) %>% 
  pivot_wider(names_from = year2,
              values_from = value) %>% 
  mutate(moth = fct_relevel(month, month.name)) #stonks%>% View()

stonks$month = factor(stonks$month, levels = month.name)

pander(stonks)
```


-------------------------------------------------------------------------------
   month     variable   1990    1991   1992   1993   1994   1995   1996   1997 
----------- ---------- ------- ------ ------ ------ ------ ------ ------ ------
   June        DJIA      2.5    17.7   3.6    7.7    -6.2    16    10.2   16.2 

   July        DJIA     11.5    7.6    4.2    3.7    -5.3   19.6   1.3    20.8 

  August       DJIA     -2.3    4.4    -0.3   7.3    1.5    15.3   0.6    8.3  

 September     DJIA     -9.2    3.4    -0.1   5.2    4.4     14    5.8    20.2 

  October      DJIA     -8.5    4.4     -5    5.7    6.9    8.2    7.2     3   

 November      DJIA     -12.8   -3.3   -2.8   4.9    -0.3   13.1   15.1   3.8  

 December      DJIA     -9.3    6.6    0.2     8     3.6    9.3    15.5   -0.7 

  January      DJIA      NA     -0.8   6.5    -0.8   11.2   1.8     15    19.6 

 February      DJIA      NA      11    8.6    2.5    5.5    3.2    15.6   20.1 

   March       DJIA      NA     15.8   7.2     9     1.6    7.3    18.4   9.6  

   April       DJIA      NA     16.2   10.6   5.8    0.5    12.8   14.8   15.3 

    May        DJIA      NA     17.3   17.6   6.7    1.3    19.5    9     13.3 
-------------------------------------------------------------------------------

Table: Table continues below

 
-------------------
 1998      moth    
------- -----------
  15       June    

  7.1      July    

 -13.1    August   

 -11.8   September 

  NA      October  

  NA     November  

  NA     December  

 -0.3     January  

 10.7    February  

  7.6      March   

 22.5      April   

 10.6       May    
-------------------

```r
knitr::kable(stonks)
```



|month     |variable |  1990| 1991| 1992| 1993| 1994| 1995| 1996| 1997|  1998|moth      |
|:---------|:--------|-----:|----:|----:|----:|----:|----:|----:|----:|-----:|:---------|
|June      |DJIA     |   2.5| 17.7|  3.6|  7.7| -6.2| 16.0| 10.2| 16.2|  15.0|June      |
|July      |DJIA     |  11.5|  7.6|  4.2|  3.7| -5.3| 19.6|  1.3| 20.8|   7.1|July      |
|August    |DJIA     |  -2.3|  4.4| -0.3|  7.3|  1.5| 15.3|  0.6|  8.3| -13.1|August    |
|September |DJIA     |  -9.2|  3.4| -0.1|  5.2|  4.4| 14.0|  5.8| 20.2| -11.8|September |
|October   |DJIA     |  -8.5|  4.4| -5.0|  5.7|  6.9|  8.2|  7.2|  3.0|    NA|October   |
|November  |DJIA     | -12.8| -3.3| -2.8|  4.9| -0.3| 13.1| 15.1|  3.8|    NA|November  |
|December  |DJIA     |  -9.3|  6.6|  0.2|  8.0|  3.6|  9.3| 15.5| -0.7|    NA|December  |
|January   |DJIA     |    NA| -0.8|  6.5| -0.8| 11.2|  1.8| 15.0| 19.6|  -0.3|January   |
|February  |DJIA     |    NA| 11.0|  8.6|  2.5|  5.5|  3.2| 15.6| 20.1|  10.7|February  |
|March     |DJIA     |    NA| 15.8|  7.2|  9.0|  1.6|  7.3| 18.4|  9.6|   7.6|March     |
|April     |DJIA     |    NA| 16.2| 10.6|  5.8|  0.5| 12.8| 14.8| 15.3|  22.5|April     |
|May       |DJIA     |    NA| 17.3| 17.6|  6.7|  1.3| 19.5|  9.0| 13.3|  10.6|May       |

