library(bakeoff)
library(tidyverse)
View(ratings)



only_first_last <- ratings %>%    
  #This assigns the data to a new dataframe
  group_by(series) %>%             
  slice(1, n()) %>%               
  #This retrieves the first and last row of the specified group_by
  mutate(which_episode = ifelse(episode == 1, "First", "Last")) %>%  View()
  #Creates a new column specifying if this was the first episode or last
  ungroup() %>% 
  mutate(series_f = as.factor(series)) %>%# View()
    ggplot(aes(x = series,
               y = viewers_7day,
               group = episode,
               color = episode
    )) +
    geom_line()   

#View(only_first_last)
  
ratings_10  <- ratings %>% 
  group_by(series) %>% 
  mutate(countseries = n()) %>% 
  filter(countseries == 10) %>% 
  select(-countseries) %>% 
  select(series,episode,viewers_7day)# %>% View()


##
ratings_10 %>% glimpse %>% 
  ggplot(aes(x = series,
             y = viewers_7day,
             group = episode,
             color = episode
             )) +
  geom_line() 

ratings_10 %>% glimpse %>% 
  ggplot(aes(x = episode,
             y = viewers_7day,
             group = series,
             color = series
  )) +
  geom_line()

ratings_10 %>% glimpse %>% 
  ggplot(aes(x = series,
             y = viewers_7day,
             #color = episode,
             )) +
  geom_point()


