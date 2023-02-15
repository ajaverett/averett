data(package = "nycflights13")
library(nycflights13)
library(tidyverse)

#Join the flights and planes tibbles.

flights %>% View()
airlines %>% View()

flights %>% 
  rename(year1 = year) %>% 
  full_join(planes) %>% 
  mutate(age = year1 - year) %>% 
  drop_na(age) %>% 
  mutate(
    agerange = case_when(
      age %in% 0:9 ~ "0-10",
      age %in% 10:19 ~ "10-20",
      age %in% 20:29 ~ "20-30",
      age %in% 30:39 ~ "30-40",
      age %in% 40:100 ~ "40+"
    )
  ) %>% 
  group_by(agerange) %>% 
  summarise(depdelay = mean(dep_delay, na.rm = TRUE)) %>% 
  ggplot(aes(x = agerange, y = depdelay, fill = "red")) +
  geom_col()


flights %>% 
  rename(year1 = year) %>% 
  full_join(planes) %>% 
  mutate(age = year1 - year) %>% 
  drop_na(age) %>% 
  mutate(
    agerange = case_when(
      age %in% 0:9 ~ "0-10",
      age %in% 10:19 ~ "10-20",
      age %in% 20:29 ~ "20-30",
      age %in% 30:39 ~ "30-40",
      age %in% 40:100 ~ "40+"
    )
  ) %>% 
  # ggplot(aes(x = (agerange), y = dep_delay, fill = "red")) + #makes a boxplot
  # geom_boxplot() +theme_test() + coord_cartesian(ylim = c(-20,35))
  
  # filter(carrier %in% c("AA","DL", "WN", "UA")) %>% 
  left_join(airlines) %>% 
  select(arr_delay, agerange, name) %>%
  ggplot(aes(x = arr_delay, color = name)) +
  geom_density() +
  coord_cartesian(xlim = c(-60,65))

  # group_by(agerange) %>% 
  # summarise(arrdelay = mean(arr_delay, na.rm = TRUE))  %>% 
  # ggplot(aes(x = agerange, y = arrdelay, fill = "red")) +
  # geom_col() 

  
  # ggplot(aes(x = (agerange), y = dep_delay, fill = "red")) +
  # geom_boxplot() +theme_test() + coord_cartesian(ylim = c(-20,35))
  
  # age %in% 0:4 ~ "0",
  # age %in% 5:9 ~ "05",
  # age %in% 10:14 ~ "10",
  # age %in% 15:19 ~ "15",
  # age %in% 20:24 ~ "20",
  # age %in% 25:29 ~ "25",
  # age %in% 30:34 ~ "30",
  # age %in% 35:39 ~ "35",
  # age %in% 40:44 ~ "40",
  # age %in% 45:49 ~ "45",
  # age %in% 50:54 ~ "50",
  # age %in% 55:600 ~ "55"
  
  