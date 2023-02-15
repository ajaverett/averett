library(tidyverse)
library(readr)
library(pander)
rawstonks <- read_rds("https://github.com/byuistats/data/blob/master/Dart_Expert_Dow_6month_anova/Dart_Expert_Dow_6month_anova.RDS?raw=true") 

rawstonks %>% View()

stonks <- rawstonks %>% 
  separate(contest_period, c('date1','date2') ,sep = '-') %>% 
  separate(date2, c('month','year2') ,sep = -4) %>% 
  select(-date1) %>% 
  filter(variable == 'DJIA') %>% 
  mutate(month = recode(month, "Dec." = 'December', "Febuary" = 'February')) %>% 
  pivot_wider(names_from = year2,
              values_from = value)# %>% View()

stonks$month = factor(stonks$month, levels = month.name)

pander(stonks)





stonks1 <- stonks %>% 
  pivot_wider(names_from = variable,
              values_from = value)

stonks %>% 
  ggplot(aes(x = contest_period, value )) +
  geom_line()
