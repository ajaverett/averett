library(tidyverse)
library(dplyr)
library(gapminder)


gapminder %>%
  
  #REMOVES KUWAIT AND EUROPEAN/AUSTRALIAN COUNTRIES
  
  filter(country != "Kuwait") %>% 
  filter(continent %in% c('Africa','Americas','Asia')) %>% 
  
  #CREATES AND SORTS BY LIFE EXP GAIN, SLICES TOP AND BOTTOM 3
  
  
  group_by(country) %>% 
  mutate(lowest = case_when(year == 1952 ~lifeExp)) %>% 
  fill(lowest) %>% 
  mutate(highest = case_when(year == 2007 ~lifeExp)) %>% 
  fill(highest, .direction = "up") %>%
  mutate(increase = highest - lowest) %>% 
  select(-c(lowest,highest)) %>% 
  ungroup(country) %>%
  arrange(increase) %>%
  group_by(year) %>% 
  slice(-(4:(n() - 3))) %>% 
  mutate(Three = if_else(increase > 2, 'Top Three', 'Bottom Three')) %>%
  arrange(country) %>% 
  
  #PLOT
  
  ggplot(aes(x = year, y  = lifeExp, group = country, color = country)) +
    geom_line(size = 2) +
    theme_bw() +
    facet_wrap(.~Three) +
    #scale_color_manual(values = c("red","#bda862",'#bb73ff','#b33f09','blue','purple')) +
  
  #LABELS
    
    labs(x = 'Year', y = 'Life Expectancy') +
    ggtitle('Comparison of the top and bottom countries \n with regards to change in life expectancy from 1952 to 2007') + 
    theme(plot.title = element_text(size = 20, face = "bold", hjust = 0.5))













