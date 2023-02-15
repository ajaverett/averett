library(tidyverse)

library(nycflights13)

# 5.2.4 Exercises

#1
flights %>%  
  filter(arr_delay >= 2) 

#2
flights %>%  
  filter(dest %in% c('HOU','IAH'))

#3
flights %>%  
  filter(carrier %in% c('UA','AA','DL'))

#4
flights %>%  
  filter(month %in% c(7,8,9))

#5
flights %>%  
  filter(arr_delay >= 120 & dep_delay <= 0) 

#6
flights %>%  
  filter(dep_delay >= 60 & arr_delay <= -30) %>% 
  View()

#7
flights %>%  
  filter(dep_time <= 600 | dep_time == 2400) %>% 
  View()

 
# 5.3.1 Exercises

#2
arrange(flights, desc(dep_delay))

#3
arrange(flights, dep_time) %>% head()

#4
flights %>% 
  mutate(speed = distance / air_time) %>% 
  arrange(desc(speed)) %>% 
  head()

#5
arrange(flights, distance) 
arrange(flights, desc(distance)) 
