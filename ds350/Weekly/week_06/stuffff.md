---
title: "YOUR TITLE"
author: "YOUR NAME"
date: "May 26, 2022"
output:
 html_document:
  keep_md: true
  toc: true
  toc_float: true
  code_folding: hide
  fig_height: 6
  fig_width: 12
  fig_align: 'center'
---




```r
library(Lahman)
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
library(pander)


bob <- People %>% #View()
  filter(nameLast == "Cox",
         nameFirst == "Bobby") 

bob.id <- bob$playerID


temp1 <- AwardsManagers %>% 
group_by(playerID, lgID) %>% 
summarise(countawards = n()) %>% 
ungroup %>% 
pivot_wider(names_from = "lgID", values_from = "countawards") %>% 
select(-AL) %>% 
drop_na() %>% 
left_join(People %>% select(nameGiven, playerID)) %>% 
select(nameGiven, NL, ML)
```

```
## `summarise()` has grouped output by 'playerID'. You can override using the
## `.groups` argument.
```

```
## Joining, by = "playerID"
```

```r
pander(temp1)
```


--------------------------------
      nameGiven         NL   ML 
---------------------- ---- ----
      Robert Joe        10   1  

   James Gottfried      1    1  

 Dorrel Norman Elvert   1    1  

       Anthony          1    1  
--------------------------------

```r
# totalawards <- AwardsManagers %>% 
#   group_by(playerID) %>% 
#   summarise(countawards = n()) %>% 
#   left_join(People) %>% 
#   select(c(playerID, countawards))
```



```r
# Managers %>% 
#   group_by(playerID) %>% 
#   summarize(totalgames = sum(G),
#             totalwins = sum(W)) %>% 
#   mutate(winpercentage = round(totalwins/totalgames*100)) %>% 
#   filter(totalgames >= 300) %>% 
#   left_join(People) %>% 
#   select(c(nameGiven, nameFirst, nameLast, winpercentage, totalgames, playerID)) %>% 
#   arrange(desc(winpercentage)) %>%
#   left_join(totalawards) %>% 
#   replace_na(list(countawards = 0)) %>%
#   ggplot(aes(y = winpercentage, x = as.factor(countawards), group = countawards, fill = countawards)) +
#   geom_boxplot()
```

tempoemptemptmelorknj


```r
# temp2 <- AwardsManagers %>% 
#   group_by(playerID, awardID) %>% 
#   summarise(countawards = n()) %>% 
#   arrange(desc(countawards)) %>% 
#   filter(countawards >= 4) %>% 
#   left_join(People) %>% 
#   ungroup() %>% 
#   select(c(nameGiven, awardID, countawards)) %>% 
#   pivot_longer(names_to = "income", values_to = "count")
# 
# pander(temp1)
```

