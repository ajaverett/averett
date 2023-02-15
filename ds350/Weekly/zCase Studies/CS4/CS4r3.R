library(Lahman)
library(tidyverse)
library(priceR)

# Find four to five different data sets that
# you will need to show full college and player names
# as well as their annual earnings.

utahrows <- Schools %>% 
  filter(state == 'UT')

utahplayers <- CollegePlaying %>% 
  filter(schoolID %in% utahrows$schoolID) %>% 
  filter(schoolID != "byu") %>% 
  mutate(school = 'utah') %>% 
  select(-c(schoolID,yearID)) %>% 
  distinct() %>% 
  left_join(Salaries) %>% 
  filter(!is.na(salary)) %>% 
  select(playerID, school, yearID, salary)

byuplayers <- CollegePlaying %>% 
  filter(schoolID == "byu") %>% 
  select(-yearID) %>% 
  rename(school = schoolID) %>% 
  distinct() %>% 
  inner_join(Salaries) %>% 
  select(playerID, school, yearID, salary)

allplayers <- bind_rows(utahplayers, byuplayers) %>% 
  mutate(adjsal = adjust_for_inflation
            (price = salary,
              from_date = yearID,
              country = "US", to_date = 2020)) 

allsalary <- allplayers %>% 
  group_by(playerID) %>% 
  mutate(adjsal = mean(salary)) %>% 
  left_join(People) %>% 
  ungroup() %>% 
  select(nameGiven, school, yearID, adjsal) %>%  #View() #row = year obs of player
  group_by(nameGiven) %>% 
  mutate(adjavgsalperyr = mean(adjsal)) %>% 
  distinct(nameGiven, school, adjavgsalperyr) #%>% View() #row = avg yr salary/player

allsalary %>% 
  group_by(school) %>% 
  summarize(meansal = mean(adjavgsalperyr)) %>% #View()
ggplot(aes(x = school, y = meansal, fill = school)) +
  geom_col() +
  scale_y_continuous(labels=scales::dollar_format())+
  labs(title = "Comparison of professional baseball players",
       subtitle = "Based on players who attended a Utah university",
       x = "Professional baseball players from a Utah university",
       y = "Average yearly salary adjusted for inflation") +
  theme_test() 

# aes(x = fct_reorder(drv, hwy, .fun=median))

allsalary %>% 
  ggplot(aes(x = fct_rev(fct_reorder(nameGiven, adjavgsalperyr, .fun=median)), y = adjavgsalperyr, fill = school)) +
  geom_col() +
  scale_y_continuous(labels=scales::dollar_format())+
  labs(title = "Comparison of professional baseball players",
       subtitle = "Based on players who attended a Utah university",
       x = "Professional baseball players from a Utah university",
       y = "Average yearly salary adjusted for inflation") +
  theme_test() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

w.var <- .3

allsalary %>% 
  ggplot(aes(x = school, y = adjavgsalperyr, color = school)) +
  geom_point(position = position_jitter(seed = 5, w = w.var),
             color = 'black',
             size = 3,
             alpha = .9) +
  geom_point(position = position_jitter(seed = 5, w = w.var),
             size = 2.5,
             alpha = .9) +
  scale_y_continuous(labels=scales::dollar_format())+
  labs(title = "Comparison of professional baseball players",
       subtitle = "Based on players who attended a Utah university",
       x = "Professional baseball players from a Utah university",
       y = "Average yearly salary adjusted for inflation") +
  theme_test() 



