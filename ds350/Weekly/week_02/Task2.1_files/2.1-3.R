library(tidyverse)

#2.1

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy))

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = class))

# Left
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, alpha = class))

# Right
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, shape = class))

#2.2


library(readr)
library(ggplot2)

rcw <- read_csv("https://byuistats.github.io/M335/data/rcw.csv", 
                col_types = cols(Semester_Date = col_date(format = "%m/%d/%y"), 
                                 Semester = col_factor(levels = c("Winter", "Spring", "Fall"))))
head(rcw)

#2.3

#install.packages("gapminder") #uncomment and run once. 
library(gapminder)
library(tidyverse)

gapminder %>% 
  ggplot(aes(x = continent)) +
  geom_bar() 
