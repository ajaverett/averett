library(rio)
library(tidyverse)


#german soliders 19th century
g19raw <- import('~/GitHub/DS350_SP22_Averett_Aj/Case Studies/CS3/germanconscr.dta')

#german prisoners
b19raw <- import('~/GitHub/DS350_SP22_Averett_Aj/Case Studies/CS3/germanprison.dta')

#german soldiers 18th century
g18raw <- import('~/GitHub/DS350_SP22_Averett_Aj/Case Studies/CS3/Heights_south-east/b6090.dbf')

#bls 20th century
us20raw <- import('https://raw.githubusercontent.com/hadley/r4ds/main/data/heights.csv')

#University of Wisconsin National Survey Data
w20raw <- import('~/GitHub/DS350_SP22_Averett_Aj/Case Studies/CS3/main05022005.sav')



# BLS as standard data set

# Knowing that the average age is 41 and -> mean(bls$age)
# assuming the average birth year is 1950,
# We can add 1950 to 41 to get 1991,
# this would be the estimiated year of recording
# thus given the following, we can mutate a birth year column like so:

us20 <- us20raw %>% 
  filter(race == 'white') %>% 
  mutate(birth_year = 1991 - age) %>% 
  mutate(study = 'us20') %>% 
  rename(edu = ed) %>% 
  rename(income = earn) %>% 
  rename(height.in = height) %>% 
  filter(sex == 'male') %>% 
  select(-c(sex, income, edu, race)) %>% 
  mutate(height.cm = height.in*2.54) %>% 
  select(birth_year, height.in, height.cm, study, age)

  

# Cleaning and combining gc to bls

g19 <- g19raw %>% 
  rename(birth_year = bdec) %>% 
  mutate(study = 'g19') %>% 
  mutate(height.in = height/2.54) %>% 
  select(-c(gebger, co,)) %>% 
  rename(height.cm = height) %>% 
  select(birth_year, height.in, height.cm, study, age)


b19 <- b19raw %>% 
  rename(birth_year = bdec) %>% 
  mutate(study = 'b19') %>% 
  mutate(height.in = height/2.54) %>% 
  select(-co) %>% 
  rename(height.cm = height) %>% 
  select(birth_year, height.in, height.cm, study, age)

g18 <- g18raw %>% 
  select(c(GEBJ, CMETER, SJ)) %>% 
  mutate(study = 'g18') %>% 
  mutate(height.in = CMETER/2.54) %>% 
  rename(birth_year = GEBJ) %>% 
  rename(height.cm = CMETER) %>% 
  mutate(age = SJ - birth_year) %>% 
  select(-SJ) %>% 
  select(birth_year, height.in, height.cm, study, age)

w20 <- w20raw %>% 
  mutate(birth_year = DOBY + 1900) %>% 
  mutate(age = 2002 - birth_year) %>%  #Wave 3 of NSFH was conducted 2001-2003
  select(c(birth_year, age, RT216F, RT216I, RE35)) %>% 
  filter(RE35 == 1) %>% 
  filter(RT216F >= 0) %>% 
  filter(RT216I >= 0) %>% 
  filter(RT216I <= 12) %>% 
  mutate(height.in = (RT216F*12) + RT216I) %>% 
  mutate(study = 'w20') %>% 
  select(-c(RT216F,RT216I)) %>% 
  mutate(height.cm = height.in*2.54) %>% 
  select(birth_year, height.in, height.cm, study, age)

alld <- bind_rows(b19, g18, g19, us20, w20)

alld$study <- factor(alld$study,
              levels = c("g18", "b19", "g19", "us20", "w20"))

alld.2040 <- alld %>% filter(age > 20 & age < 40)

########

ggplot(alld, aes(y = height.in, x = birth_year, color = study)) + 
  geom_jitter(size = 0.4,
              alpha = 0.5,
              width = 3,
              height = 3,) +
  facet_grid(study~.) +
  theme_minimal() +
  theme(plot.subtitle = element_text(lineheight = .5,
                                     size = 8,
                                     face = "italic")) +
  labs(x = "Birth year",
       y = "Height in inches",
       title = "Comparison of height over 1800's-2000's",
       subtitle = "g18 = South-east/west German soldiers born in the 18th century\n
b19 = Bavarian male oldiers, 19th century\n
g19 = German male soldiers in Bavaria, 19th century \n
us20 = US Bureau of Labor Statistics Height Data\n
w20 = National Survey of Families and Households",
  )


#boxplot
ggplot(alld, aes(y = height.in, fill = study)) +
  geom_boxplot(alpha = 0.6) +
  geom_hline(
    data = . %>%
      group_by(study) %>%
      summarise(line = mean(height.in)),
    mapping = aes(yintercept = line)
  ) +
  facet_grid(.~study) +
  theme_minimal() 

# Nose graph!
ggplot(alld, aes(y = height.in, fill = study)) +
  geom_density(alpha = 0.6) +
  geom_hline(
    data = . %>%
      group_by(study) %>%
      summarise(line = mean(height.in)),
    mapping = aes(yintercept = line)
  ) +
  facet_grid(.~study) +
  theme(axis.line = element_line(colour = "white"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_rect(fill = 'white')) 

ggplot(alld.2040, aes(y = height.in, x = age, color = study)) +
  geom_jitter(alpha = 0.6) + theme_classic()


###


alld.range <- alld %>% 
  mutate(age_range = case_when(age %in% c(10:19) ~ "10-20",
                               age %in% c(20:29) ~ "20-30",
                               age %in% c(30:39) ~ "30-40",
                               age %in% c(40:49) ~ "40-50",
                               age %in% c(50:59) ~ "50-60",
                               age %in% c(60:200) ~ "60+",
                               )) %>%
  group_by(study, age_range) %>%
  summarize(average = mean(height.in, na.rm = TRUE)
  ) %>% 
  na.omit()

ggplot(alld.range, aes(x = age_range, y = average, color = study, group = study)) +
  geom_line() + theme_classic()



