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
  distinct(nameGiven, school, adjavgsalperyr) #View() #row = avg yr salary/player

allsalary %>% 
  group_by(school) %>% 
  summarize(meansal = mean(adjavgsalperyr)) %>% #View()
  ggplot(aes(x = school, y = meansal, color = school)) +
  geom_col()


allsalary

